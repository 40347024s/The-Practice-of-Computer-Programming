import numpy as np
from seqpair_reward_generator import get_perfect_data

perfect_seqpair = ((9, 0, 4, 8, 2, 7, 5, 6, 1, 3), (5, 8, 4, 3, 0, 2, 1, 7, 9, 6))

print(np.argsort(perfect_seqpair[0]))
print(np.arange(10))
print(np.abs(np.arange(10)-np.argsort(perfect_seqpair[0])))


perfect_seqpair, perfect_weights = get_perfect_data(23)
print(f'pair: [{perfect_seqpair[0]}, {perfect_seqpair[1]}]')
print(f'weig: [{perfect_weights[0]}, {perfect_weights[1]}]')