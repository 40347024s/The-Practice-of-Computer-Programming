import torch
import numpy as np
from collections import deque

from seqpair_reward_function_torch import get_perfect_data, get_reward, get_reward_batch, num_correct_position, USE_CUDA, device
import time

populations = 10**3
max_iter = 10**6

for epo in range(999, 1000):
    device_num = epo + 1
    ts = time.time()
    max_queue_len = 30
    d = deque(maxlen=max_queue_len)
    max_device_size = 100
    print('max_device_size:', max_device_size)
    seqpairs = torch.randint(0, device_num, size=(populations, 2, device_num), dtype=torch.float32, device=device)
    new_mean = torch.mean(seqpairs)
    new_std = torch.std(seqpairs)

    best_results = {'loss': -np.inf, 'pair': seqpairs[0], 'correct_num': 0}
    print('-'*50)
    stage_flag = 0
    discount_factor = 1
    total_it = 0
    mask = torch.zeros((2, device_num), device=device)
    if stage_flag*max_device_size <= device_num:
        mask[:, stage_flag*max_device_size:(stage_flag+1)*max_device_size] = 1
    mask = mask.bool()
    for it in range(max_iter):
        new_seqpairs = torch.randn(populations, 2, device_num, device=device)
        new_seqpairs = new_seqpairs * new_std + new_mean
        new_seqpairs = torch.round(new_seqpairs)
        new_seqpairs *= mask

        loss = get_reward_batch(new_seqpairs)
        loss_mean = torch.mean(loss)
        loss_std = torch.std(loss)
        elite_loss_thresh = loss_mean + 1.5 * loss_std
        candidate_sorted_id = torch.flip(torch.argsort(loss), [0, ])
        elite_seqpairs = new_seqpairs[loss>=elite_loss_thresh]

        cur_best_seqpair = best_results['pair'] * ~mask + torch.abs(new_seqpairs[candidate_sorted_id[0]])
        max_loss_per_iter = get_reward(cur_best_seqpair)
        if max_loss_per_iter > best_results['loss']:
            best_results['loss'] = max_loss_per_iter
            best_results['pair'] = cur_best_seqpair
            best_results['correct_num'] = num_correct_position(best_results['pair'])
            print(f"[T] {it:3d}-th stage {stage_flag} loss: {best_results['loss']}, correct num/total num: {best_results['correct_num']:2d}/{device_num*2:2d}")

        else:
            correct_num = num_correct_position(cur_best_seqpair)
            # print(f"[F ({np.std(d)})] {it:3d}-th stage {stage_flag} loss: {max_loss_per_iter}, correct num/total num: {correct_num:2d}/{device_num*2:2d}")

        d.append(best_results['loss'].item())

        discount_factor = max(discount_factor-0.01, 0.01)
        if max_loss_per_iter == 0:
            break
        elif (len(d)==max_queue_len and np.std(d)==0.0) or elite_seqpairs.size(0)==0:
            if (stage_flag+1)*max_device_size <= device_num:
                print('----------- change stage -----------')
                stage_flag += 1
                d.clear()
                new_mean = torch.mean(seqpairs)
                new_std = torch.std(seqpairs)
                # best_results = {'loss': -np.inf, 'pair': None, 'correct_num': 0}
                mask = torch.zeros((2, device_num), device=device)
                mask[:, stage_flag*max_device_size:(stage_flag+1)*max_device_size] = 1
                mask = mask.bool()
                cur_seqpair = best_results['pair']
                cur_loss = get_reward(cur_seqpair)
                cur_correct_num = num_correct_position(cur_seqpair)   
                # print(f"[D00] {it:3d}-th stage {stage_flag} loss: {cur_loss}, correct num/total num: {cur_correct_num:2d}/{device_num*2:2d}")
                cur_seqpair = best_results['pair'] * ~mask
                cur_loss = get_reward(cur_seqpair)
                cur_correct_num = num_correct_position(cur_seqpair)
                # print(f"[D01] {it:3d}-th stage {stage_flag} loss: {cur_loss}, correct num/total num: {cur_correct_num:2d}/{device_num*2:2d}")
                cur_seqpair = best_results['pair'] * mask
                cur_loss = get_reward(cur_seqpair)
                cur_correct_num = num_correct_position(cur_seqpair)
                # print(f"[D02] {it:3d}-th stage {stage_flag} loss: {cur_loss}, correct num/total num: {cur_correct_num:2d}/{device_num*2:2d}")
            else:
                print('Error: Result not found.')
                if len(d)==max_queue_len and np.std(d)==0.0:
                    print('np.std(d) == 0.0')
                if elite_seqpairs.size(0)==0:
                    print('elite_seqpairs.size(0)==0')
                time.sleep(2)
                break
        else:
            new_mean = torch.mean(elite_seqpairs, axis=0)
            if elite_seqpairs.size(0)==1:
                new_std = torch.std(seqpairs)
            else:
                new_std = torch.std(elite_seqpairs, axis=0)

    # print('---------- AI solution ----------')
    # print(best_results['pair'])
    # print('---------- Real answer ----------')
    # print(get_perfect_data(device_num)[0])
    print('-------------------- final result -------------------')
    print(f"{it:3d}-th stage {stage_flag} loss: {best_results['loss']}, correct num/total num: {best_results['correct_num']:2d}/{device_num*2:2d}")

    total_it = it + 1

    te = time.time()
    print(f'Total used {round(te-ts, 3)} sec.')
    print(f'Avg. used {round((te-ts)/total_it, 3)} sec.')
    print(f'Avg. {round(total_it/(te-ts))} iters per second')
