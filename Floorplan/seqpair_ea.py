import numpy as np
from collections import deque
from seqpair_reward_generator import get_perfect_data, get_reward_batch, num_correct_position
import time

populations = 10**4
max_iter = 10**6

for epo in range(199, 200):
    device_num = epo + 1
    ts = time.time()
    d = deque(maxlen=30)
    seqpairs = np.random.randint(0, device_num, size=(populations, 2, device_num)).astype(np.float32)
    new_mean = np.mean(seqpairs)
    new_std = np.std(seqpairs)

    best_results = {'loss': -np.inf, 'pair': None, 'correct_num': 0}
    print('-'*50)
    stage_flag = 3
    discount_factor = 1
    total_it = 0
    for it in range(max_iter):
        elite_num = int(populations*0.1*discount_factor)
        new_seqpairs = np.random.randn(populations, 2, device_num)
        new_seqpairs = new_seqpairs * new_std + new_mean
        new_seqpairs = np.round(new_seqpairs)
        if stage_flag==0:
            seqpairs[:, 0, :] = 0
            new_seqpairs[:, 1, :] = 0
            seqpairs = seqpairs + new_seqpairs
        elif stage_flag==1:
            seqpairs[:, 1, :] = 0
            new_seqpairs[:, 0, :] = 0
            seqpairs = seqpairs + new_seqpairs
        else:
            seqpairs = new_seqpairs


        loss = get_reward_batch(seqpairs)
        loss_mean = np.mean(loss)
        loss_std = np.std(loss)
        elite_loss_thresh = loss_mean + 2.0 * loss_std
        candidate_sorted_id = np.argsort(loss)[::-1]
        elite_seqpairs = seqpairs[loss>=elite_loss_thresh]

        # print(f'{it:3d}-th stage {stage_flag} loss: {loss[candidate_sorted_id[0]]}, correct num/total num: {num_correct_position(seqpairs[candidate_sorted_id[0]]):2d}/{device_num*2:2d}')
        max_loss_per_iter = loss[candidate_sorted_id[0]].item()
        d.append(max_loss_per_iter)
        if max_loss_per_iter > best_results['loss']:
            best_results['loss'] = loss[candidate_sorted_id[0]]
            best_results['pair'] = np.abs(seqpairs[candidate_sorted_id[0]])
            best_results['correct_num'] = num_correct_position(best_results['pair'])
            print(f"{it:3d}-th stage {stage_flag} loss: {best_results['loss']}, correct num/total num: {best_results['correct_num']:2d}/{device_num*2:2d}")


        discount_factor = max(discount_factor-0.01, 0.01)
        if max_loss_per_iter == 0:
            break
        elif (len(d)==30 and np.std(d)<=0.001) or elite_seqpairs.shape[0]==0:
            if stage_flag<1:
                print('----------- change stage -----------')
                stage_flag += 1
                d.clear()
                new_mean = np.zeros_like(seqpairs[0])
                new_std = np.ones_like(seqpairs[0])
            else:
                break
        else:
            new_mean = np.mean(elite_seqpairs, axis=0)
            if elite_seqpairs.shape[0]==1:
                new_std = np.ones_like(seqpairs[0])
            else:
                new_std = np.std(elite_seqpairs, axis=0)

    # print('---------- AI solution ----------')
    # print(best_results['pair'])
    # print('---------- Real answer ----------')
    # print(get_perfect_data(device_num)[0])
    print(f"{it:3d}-th stage {stage_flag} loss: {best_results['loss']}, correct num/total num: {best_results['correct_num']:2d}/{device_num*2:2d}")

    total_it = it + 1

    te = time.time()
    print(f'Total used {round(te-ts, 3)} sec.')
    print(f'Avg. used {round((te-ts)/total_it, 3)} sec.')
    print(f'Avg. {round(total_it/(te-ts))} iters per second')
