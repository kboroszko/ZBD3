import subprocess
import time
# Run commands in parallel
processes = []


start = time.time()
for i in range(20):
    command = f"python3 work.py {i}"
    # command = f'echo "{i}"'
    process = subprocess.Popen(command, shell=True)
    processes.append(process)
end1 = time.time()
# Collect statuses
output = [p.wait() for p in processes]
end2 = time.time()
print("end1", end1 - start)
print("end2", end2 - start)