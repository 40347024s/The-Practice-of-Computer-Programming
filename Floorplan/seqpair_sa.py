import math
import random
from simanneal import Annealer
import numpy as np
from copy import deepcopy

from seqpair_reward_generator import get_reward, num_correct_position

class SASolver(Annealer):
    def __init__(self, state, cost_func):
        super(SASolver, self).__init__(state)
        self.cost_func = cost_func
        self.best_result = {'loss': -np.inf, 'pair': None, 'correct': None}

    def move(self):
        initial_energy = self.energy()

        a = random.randint(0, self.state.shape[1] - 1)
        b = random.randint(0, self.state.shape[1] - 1)
        i = random.randint(0, 1)
        self.state[i][a], self.state[i][b] = self.state[i][b], self.state[i][a]
        new_energy = self.energy()
        if -new_energy > self.best_result['loss']:
            self.best_result['loss'] = -new_energy
            self.best_result['pair'] = deepcopy(self.state)
            self.best_result['correct'] = num_correct_position(self.state)
            print('correct num:', self.best_result['correct'])
            # print(f'loss: {-new_energy}, correct/total num: {num_correct_position(self.state):2d}/{self.state.shape[1]*2:2d}')

        return new_energy - initial_energy

    def energy(self):
        return -self.cost_func(self.state)

if __name__=='__main__':
    device_num = 200
    x = np.concatenate((np.arange(device_num)[np.newaxis], np.arange(device_num)[np.newaxis]))
    sa = SASolver(x, get_reward)
    sa.set_schedule(sa.auto(minutes=0.5, steps=2000))
    sa.copy_strategy = 'deepcopy'
    state, e = sa.anneal()
    print('-'*15, 'summary', '-'*15)
    print('final state:\n', state)
    print(f'correct/total num: {num_correct_position(state):2d}/{state.shape[1]*2:2d}')
    print(f'origin/final loss: {get_reward(x)}/{get_reward(state)}')
