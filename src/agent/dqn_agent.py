import torch
#import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

from src.agent.network import QNetwork
from src.agent.buffer import ReplayBuffer
#import config


class DQNAgent:
    def __init__(self, state_size=7, action_size=8):
        self.action_size = action_size

        self.q_network = QNetwork(state_size, action_size)
        self.target_network = QNetwork(state_size, action_size)
        self.target_network.load_state_dict(self.q_network.state_dict())

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.buffer = ReplayBuffer(capacity=10000)

        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995
        
        
    def act(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.q_network(state_tensor)
            return torch.argmax(q_values).item()
        
        
        
if __name__ == "__main__":
    print("dqn agent setup")
    agent = DQNAgent()
    fake_state = np.random.rand(7)

    for i in range(10):
        action = agent.act(fake_state)
        print(action)