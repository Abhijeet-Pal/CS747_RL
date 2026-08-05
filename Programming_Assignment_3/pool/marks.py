import threading
import subprocess

# # Define the commands you want to run

num_seeds = 50
parallel = 10
serial = 5

# # Function to run a command using subprocess
def run_command(commands):
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.wait()
    # print(f"Command '{command}' completed")

# Create a list to store the thread objects
threads = []

# Create and start a thread for each command
for parallel_seed in range(parallel):
    commands = []
    for serial_seed in range(serial):
        commands.append(f'py .\main.py --level-all --no-render --seed {serial*parallel_seed + serial_seed} > res/seed{serial*parallel_seed + serial_seed}_res.txt')
    thread = threading.Thread(target=run_command, args=(commands,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
marks = 0
for seed, thread in enumerate(threads):
    thread.join()
    for serial_seed in range(serial):
        with open(f'res\seed{seed * serial + serial_seed}_res.txt') as f:
            lines = f.readlines()
            lastline = lines[-1]
            marks += float(lastline.split()[3])


print(f"expected marks = {marks/num_seeds}")



