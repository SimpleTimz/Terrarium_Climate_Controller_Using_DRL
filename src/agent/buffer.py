import random
from collections import deque
import numpy as np


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
        
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
        
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards),
            np.array(next_states),
            np.array(dones)
        )
        
    def __len__(self):
        return len(self.buffer)
    
if __name__ == "__main__":
    print("replaybuffer")
    buffer = ReplayBuffer(capacity=100)

    for i in range(10):
        fake_state = np.random.rand(7)
        fake_next_state = np.random.rand(7)
        fake_action = 3
        fake_reward = -1.0
        fake_done = False
        buffer.push(fake_state, fake_action, fake_reward, fake_next_state, fake_done)

    print(len(buffer))

    states, actions, rewards, next_states, dones = buffer.sample(4)
    print(states.shape)
    print(actions)