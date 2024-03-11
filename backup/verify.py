import re

def add_test_rewards(file_path):
    # Regular expression to match lines with "test_reward: <number> ± <number>"
    pattern = re.compile(r"test_reward: (-?[\d.]+) ± [\d.]+")
    total_reward = 0.0
    count  = 0
    # Open and read the file
    with open(file_path, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Convert the captured reward to a float and add it to the total
                reward = float(match.group(1))
                total_reward += reward
                count += 1
                print(f"Reward: {reward}")
    # Print or save the total reward
    print(f"Total test reward: {total_reward}")

    print(total_reward /count)

# Replace 'your_file_path.txt' with the actual file path
file_path = 'temp'
add_test_rewards(file_path)