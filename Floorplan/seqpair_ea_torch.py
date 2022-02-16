import torch
import numpy as np
from torch.distributions.normal import Normal
from collections import deque
from seqpair_reward_function_torch import get_reward_batch, num_correct_position, USE_CUDA
import time

device_num = 23
populations = 10**5
max_iter = 1000

for epo in range(5):
    ts = time.time()
    d = deque(maxlen=30)
    if USE_CUDA:
        seqpair_probs = torch.from_numpy(np.random.rand(populations, 2, device_num)).cuda()
    else:
        seqpair_probs = torch.from_numpy(np.random.rand(populations, 2, device_num))
    best_results = {'loss': np.inf, 'pair': None, 'correct_num': 0}
    new_mean = torch.zeros_like(seqpair_probs[0])
    new_std = torch.ones_like(seqpair_probs[0])
    print('-'*50)
    stage_flag = 3
    discount_factor = 1
    total_it = 0
    for it in range(max_iter):
        elite_num = int(populations*0.1*discount_factor)
        m = Normal(new_mean, new_std, validate_args=False)
        new_seqpair_probs = m.sample(torch.Size((populations, )))
        if stage_flag==0:
            seqpair_probs[:, 0, :] = 0
            new_seqpair_probs[:, 1, :] = 0
            seqpair_probs = seqpair_probs + new_seqpair_probs
        elif stage_flag==1:
            seqpair_probs[:, 1, :] = 0
            new_seqpair_probs[:, 0, :] = 0
            seqpair_probs = seqpair_probs + new_seqpair_probs
        else:
            seqpair_probs = new_seqpair_probs

        candidate_seqpairs = torch.argsort(seqpair_probs)
        loss = get_reward_batch(candidate_seqpairs)
        loss_mean = torch.mean(loss)
        loss_std = torch.std(loss)
        elite_loss_thresh = loss_mean + 2.0 * loss_std
        candidate_sorted_id = torch.flip(torch.argsort(loss), [0, ])
        elite_seqpairs_probs = seqpair_probs[loss>=elite_loss_thresh]

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
        elif (len(d)==30 and np.std(d)<=0.001) or elite_seqpairs_probs.size(0)==0:
            if stage_flag<1:
                print('----------- change stage -----------')
                stage_flag += 1
                d.clear()
                new_mean = torch.zeros_like(seqpair_probs[0])
                new_std = torch.ones_like(seqpair_probs[0])
            else:
                total_it = it + 1
                break
        else:
            new_mean = torch.mean(elite_seqpairs_probs, axis=0)
            if elite_seqpairs_probs.size(0)==1:
                new_std = torch.ones_like(seqpair_probs[0])
            else:
                new_std = torch.std(elite_seqpairs_probs, axis=0)

    print(best_results['pair'])

    te = time.time()
    print(f'Total used {round(te-ts)} sec.')
    print(f'Avg. used {round((te-ts)/total_it, 3)} sec.')
