import torch
import numpy as np
from torch.distributions.normal import Normal
from collections import deque
from seqpair_reward_function_torch import get_reward_batch, num_correct_position
import time

device_num = 10
populations = 10**5
max_iter = 1000

for epo in range(1):
    d = deque(maxlen=30)
    if torch.cuda.is_available():
        seqpairs = torch.from_numpy(np.random.randint(0, device_num, (populations, 2, device_num))).float().cuda()
    else:
        seqpairs = torch.from_numpy(np.random.randint(0, device_num, (populations, 2, device_num))).float()
    best_results = {'loss': np.inf, 'pair': None, 'correct_num': 0}
    new_mean = torch.zeros_like(seqpairs[0])
    new_std = torch.ones_like(seqpairs[0])
    print('-'*50)
    stage_flag = 0
    discount_factor = 1
    for it in range(max_iter):
        elite_num = int(populations*0.1*discount_factor)
        m = Normal(new_mean, new_std, validate_args=False)
        new_seqpairs = m.sample(torch.Size((populations, )))
        # new_seqpairs = torch.randn(populations, 2, device_num) * new_std + new_mean
        if stage_flag==0:
            seqpairs[:, 0, :] = 0
            new_seqpairs[:, 1, :] = 0
            candidate_seqpairs = seqpairs + new_seqpairs
        elif stage_flag==1:
            seqpairs[:, 1, :] = 0
            new_seqpairs[:, 0, :] = 0
            candidate_seqpairs = seqpairs + new_seqpairs
        else:
            candidate_seqpairs = new_seqpairs

        loss = get_reward_batch(candidate_seqpairs)
        loss_mean = torch.mean(loss)
        loss_std = torch.std(loss)
        elite_loss_thresh = loss_mean + 2.0 * loss_std
        candidate_sorted_id = torch.flip(torch.argsort(loss), [0, ])
        elite_seqpairs = seqpairs[loss>=elite_loss_thresh]

        print(f'{it:3d}-th stage {stage_flag} loss: {loss[candidate_sorted_id[0]]}, correct num/total num: {num_correct_position(candidate_seqpairs[candidate_sorted_id[0]]):2d}/{device_num*2:2d}')
        max_loss_per_iter = loss[candidate_sorted_id[0]].item()
        d.append(max_loss_per_iter)
        if max_loss_per_iter < best_results['loss']:
            best_results['loss'] = loss[candidate_sorted_id[0]]
            best_results['pair'] = candidate_seqpairs[candidate_sorted_id[0]]
            best_results['correct_num'] = num_correct_position(candidate_seqpairs[candidate_sorted_id[0]])

        discount_factor = max(discount_factor-0.01, 0.01)
        if max_loss_per_iter == 0:
            break
        elif (len(d)==30 and np.std(d)<=0.001) or elite_seqpairs.size(0)==0:
            if stage_flag<1:
                print('----------- change stage -----------')
                stage_flag += 1
                d.clear()
                new_mean = torch.zeros_like(seqpairs[0])
                new_std = torch.ones_like(seqpairs[0])
            else:
                break
        else:
            new_mean = torch.mean(elite_seqpairs, axis=0)
            if elite_seqpairs.size(0)==1:
                new_std = torch.ones_like(seqpairs[0])
            else:
                new_std = torch.std(elite_seqpairs, axis=0)

    print(best_results['pair'])


