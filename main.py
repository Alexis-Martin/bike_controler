import os
import machine

# Function to read configuration from run.conf
def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

# Read configuration
config = read_config('conf/run.conf')
current_partition = config.get('current_partition', 'part1')
print(confing, current_partition)

# Construct the path to the main.py in the current partition
main_path = f"{current_partition}/main.py"

# Execute the main.py from the current partition
try:
    exec(open(main_path).read(), globals())
except Exception as e:
    print(f"Error executing {main_path}: {e}")
    # Optionally, handle the error (e.g., switch partitions)
    # For example, you could set writable_partition as the new current_partition
    # and restart the device.
    new_current_partition = config.get('writable_partition', 'part2')
    with open('conf/run.conf', 'w') as file:
        file.write(f"current_partition={new_current_partition}\n")
        file.write(f"writable_partition={current_partition}\n")
    print("Restarting with new partition...")
    machine.reset()
