import numpy as np
import time


def get_perfect_data(device_num):
    np.random.seed(device_num)
    perfect_seqpair = np.concatenate((np.arange(device_num)[np.newaxis], np.arange(device_num)[np.newaxis]))
    for i in range(2):
        np.random.shuffle(perfect_seqpair[i])
    perfect_weights = ((perfect_seqpair.copy()**2)%min(device_num, 9)) + 1
    perfect_weights = np.ones_like(perfect_seqpair)
    np.random.seed(int(time.time()))
    return perfect_seqpair, perfect_weights

def num_correct_position(seqpair):
    perfect_seqpair, perfect_weights = get_perfect_data(seqpair.shape[1])
    seqpair_diff = seqpair-perfect_seqpair

    return np.sum(seqpair_diff==0)

def num_correct_position_batch(seqpairs):
    perfect_seqpair, perfect_weights = get_perfect_data(seqpairs.shape[2])
    seqpair_diff = seqpairs - perfect_seqpair

    return np.sum(seqpair_diff==0, axis=(1, 2))


def get_reward(seqpair):
    loss = 0
    perfect_seqpair, perfect_weights = get_perfect_data(seqpair.shape[1])

    for i, p in enumerate(seqpair):
        diff = np.abs(perfect_seqpair[i]-p)*perfect_weights[i]
        # print(diff)
        loss += -np.sum(diff)

    return loss

    

def get_reward_batch(seqpairs):
    perfect_seqpair, perfect_weights = get_perfect_data(seqpairs.shape[2])
    loss = -np.sum(np.abs(perfect_seqpair-seqpairs)*perfect_weights, axis=(1, 2))
    return loss


if __name__=='__main__':
    seqpair_dict = {}
    dict_size = 10**6
    while len(seqpair_dict)<dict_size:
        x = np.arange(10)
        y = np.arange(10)
        # r = 30 * np.random.randn() + 100 # sigma * n + mu
        np.random.shuffle(x)
        np.random.shuffle(y)
        r = get_reward((tuple(x), tuple(y)))
        r2 = get_reward_batch(np.array((tuple(x), tuple(y)))[np.newaxis])
        print(r, r2)
        if seqpair_dict.get(f'({tuple(x)}, {tuple(y)})')==None:
            # print(x, y, r)
            seqpair_dict[f'({tuple(x)}, {tuple(y)})'] = r
            # print(f'{len(seqpair_dict)}: {r}')
            print(f'{len(seqpair_dict)}: {r}')

    # with open(f'seqpair_dict_size{dict_size}.pkl', 'wb') as f:
    #     pickle.dump(seqpair_dict, f, protocol=pickle.HIGHEST_PROTOCOL)



