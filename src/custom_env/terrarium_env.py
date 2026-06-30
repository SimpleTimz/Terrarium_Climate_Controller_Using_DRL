import gymnasium as gym
import numpy as np
import config



def banded_penalty(value, safe_low, safe_high):
        if safe_low <= value <=safe_high:
            return 0
        distance = max(safe_low - value, value - safe_high, 0)
        return distance ** 2


class TerrariumEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(8)
        self.observation_space = gym.spaces.Box(low = 0.0, 
                                                high = 1.0, 
                                                shape = (7,), 
                                                dtype=np.float32)
        self.reset()

    def _get_obs(self):
        normalized_temp = (self.temperature - config.TEMP_DANGER_LOW) / (config.TEMP_DANGER_HIGH - config.TEMP_DANGER_LOW)
        normalized_humidity = (self.humidity - config.HUM_DANGER_LOW) / (config.HUM_DANGER_HIGH - config.HUM_DANGER_LOW)
        normalized_co2 = (self.co2 - config.CO2_DANGER_LOW) / (config.CO2_DANGER_HIGH - config.CO2_DANGER_LOW)
        normalized_time = (self.time - 0) / (24 - 0)
        normalized_heater_state = self.heater_state
        normalized_fan_state = self.fan_state
        normalized_light_state = self.light_state

        return np.array([
            normalized_temp,
            normalized_humidity,
            normalized_co2,
            normalized_time,
            normalized_heater_state,
            normalized_fan_state,
            normalized_light_state
        ], dtype=np.float32)

    def _compute_reward(self, temp_penalty, hum_penalty, co2_penalty, switch_count, in_danger):
        reward = -(temp_penalty + hum_penalty + co2_penalty)
        reward -= config.W_SWITCH * switch_count
        if in_danger:
            reward -= config.W_DANGER
        return reward

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.temperature = np.random.uniform(config.TEMP_SAFE_LOW, config.TEMP_SAFE_HIGH)
        self.humidity = np.random.uniform(config.HUM_SAFE_LOW, config.HUM_SAFE_HIGH)
        self.co2 = np.random.uniform(config.CO2_SAFE_LOW, config.CO2_SAFE_HIGH)
        self.time = np.random.uniform(0, 24)
        
        self.heater_state = 0
        self.fan_state = 0 
        self.light_state = 0
        
        self.current_step = 0
        
        observation = self._get_obs()
        info = {}
        
        return observation, info
    
    
    
    def step(self, action):
        old_heater = self.heater_state
        old_fan = self.fan_state
        old_light = self.light_state    
    
        heater_state = action % 2
        action = action // 2
        fan_state = action % 2
        action = action // 2
        light_state = action % 2
        
        self.heater_state = heater_state
        self.fan_state = fan_state
        self.light_state = light_state  

        new_temp = (self.temperature
                + config.K_AMBIENT_T * (config.AMBIENT_TEMP - self.temperature)
                + config.K_HEATER * heater_state
                - config.K_FAN_T * fan_state
                + config.K_LIGHT_T * light_state)

        new_hum = (self.humidity
                + config.K_AMBIENT_H * (config.AMBIENT_HUMIDITY - self.humidity)
                - config.K_HEATER_H * heater_state
                - config.K_FAN_H * fan_state
                - config.K_LIGHT_H * light_state)

        new_co2 = (self.co2
                + config.ANIMAL_CO2_OUTPUT
                - config.K_FAN_C * fan_state)
    
        new_temp = np.clip(new_temp, config.TEMP_DANGER_LOW, config.TEMP_DANGER_HIGH)
        new_hum = np.clip(new_hum, config.HUM_DANGER_LOW, config.HUM_DANGER_HIGH)
        new_co2 = np.clip(new_co2, config.CO2_DANGER_LOW, config.CO2_DANGER_HIGH)

        self.temperature = new_temp
        self.humidity = new_hum
        self.co2 = new_co2

        self.time = (self.time + 1) % 24
        
        switch_count = (
            (heater_state != old_heater) +
            (fan_state != old_fan) +
            (light_state != old_light)
        )

        temp_penalty = banded_penalty(self.temperature, config.TEMP_SAFE_LOW, config.TEMP_SAFE_HIGH)
        hum_penalty = banded_penalty(self.humidity, config.HUM_SAFE_LOW, config.HUM_SAFE_HIGH)
        co2_penalty = banded_penalty(self.co2, config.CO2_SAFE_LOW, config.CO2_SAFE_HIGH)

        in_danger = (
            self.temperature <= config.TEMP_DANGER_LOW or self.temperature >= config.TEMP_DANGER_HIGH or
            self.humidity <= config.HUM_DANGER_LOW or self.humidity >= config.HUM_DANGER_HIGH or
            self.co2 <= config.CO2_DANGER_LOW or self.co2 >= config.CO2_DANGER_HIGH
        )

        reward = self._compute_reward(temp_penalty, hum_penalty, co2_penalty, switch_count, in_danger)
        self.current_step += 1
        terminated = False
        truncated = self.current_step >= config.MAX_STEPS_PER_EPISODE

        observation = self._get_obs()
        info = {}

        return observation, reward, terminated, truncated, info    

    
if __name__ == "__main__":
    print("custom gym environment setup")
    env = TerrariumEnv()
    print(env.temperature)
    print(env.humidity)
    print(env.co2)
    
    
    for i in range(50):
        observation, reward, terminated, truncated, info = env.step(5)
        print(env.temperature)