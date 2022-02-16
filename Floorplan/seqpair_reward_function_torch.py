import numpy as np
import torch
import pickle
import time

USE_CUDA = torch.cuda.is_available()
device = 'cuda:0' if USE_CUDA else 'cpu'

def get_perfect_data(device_num):
    np.random.seed(device_num)
    perfect_seqpair = np.concatenate((np.arange(device_num)[np.newaxis], np.arange(device_num)[np.newaxis])).astype(np.float32)
    for i in range(2):
        np.random.shuffle(perfect_seqpair[i])
    # perfect_weights = ((perfect_seqpair.copy()**2)%min(device_num, 9)) + 1
    perfect_weights = np.ones_like(perfect_seqpair)
    np.random.seed(int(time.time()))
    perfect_seqpair = torch.from_numpy(perfect_seqpair)
    perfect_weights = torch.from_numpy(perfect_weights)
    if USE_CUDA:
        perfect_seqpair = perfect_seqpair.to(device)
        perfect_weights = perfect_weights.to(device)

    return perfect_seqpair, perfect_weights

def num_correct_position(seqpair):
    perfect_seqpair, perfect_weights = get_perfect_data(seqpair.size(1))
    seqpair_diff = seqpair-perfect_seqpair

    return torch.sum(seqpair_diff==0.0)

def num_correct_position_batch(seqpairs):
    perfect_seqpair, perfect_weights = get_perfect_data(seqpairs.size(2))
    seqpair_diff = seqpairs - perfect_seqpair

    return torch.sum(seqpair_diff==0, axis=(1, 2))


def get_reward(seqpair):
    loss = 0
    perfect_seqpair, perfect_weights = get_perfect_data(seqpair.size(1))

    for i, p in enumerate(seqpair):
        diff = torch.abs(perfect_seqpair[i]-p)*perfect_weights[i]
        # print(diff)
        loss += -torch.sum(diff).float()

    return loss

def get_reward_batch(seqpairs):
    perfect_seqpair, perfect_weights = get_perfect_data(seqpairs.size(2))
    loss = -torch.sum(torch.abs(perfect_seqpair-seqpairs)*perfect_weights, axis=(1, 2)).float()

    return loss

if __name__=='__main__':
    perfect_pair, perfect_weights = get_perfect_data(40)
    print(perfect_pair)
    print(get_reward(perfect_pair))

    # tx = torch.FloatTensor([[-1., -0., -1., -0.,  1.,  1.,  1., -0., -0., -0.,  1.,  1., -2.,  1.,
    #       0.,  2., -1., -0.,  1.,  1.,  1.,  2.,  1.,  2.,  1., -0., -1.,  0.,
    #       2.,  1., -0.,  1.,  2., -1.,  0.,  2., -0.,  0., -0.,  1.],
    #     [-1.,  1.,  1.,  1., -0.,  0.,  1.,  1., -1.,  0., -0.,  1., -2., -1.,
    #      -1.,  1.,  0.,  1.,  0.,  1.,  1.,  1.,  1.,  1.,  2.,  1.,  1.,  1.,
    #       0., -0.,  1.,  1., -0.,  2., -1.,  1., -0., -1., -0.,  1.]])

    # print(tx)

    # print('correct num:', num_correct_position(tx))
    # print('loss:', get_reward(tx))