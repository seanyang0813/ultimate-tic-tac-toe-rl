import uttt_env
import numpy as np
env = uttt_env.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last(observe=True)

    if termination or truncation:
        action = None
    else:
        mask = observation["action_mask"]
        temp = np.where(mask == 1)[0]
        print(temp)
        action = np.random.choice(temp)
        print(action)
    env.step(action)
env.close()