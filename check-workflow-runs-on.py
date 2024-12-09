import threading
import queue
import time

# Define a queue to hold the jobs
job_queue = queue.Queue()

# Define the runners
class Runner(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            job = job_queue.get()
            if job is None:
                break
            print(f"{self.name} is executing job {job}")
            time.sleep(2)  # Simulate job execution time
            print(f"{self.name} has completed job {job}")
            job_queue.task_done()

# Create runners
runner1 = Runner("Runner 1")
runner2 = Runner("Runner 2")

# Start runners
runner1.start()
runner2.start()

# Add jobs to the queue
for job in range(1, 11):
    job_queue.put(job)

# Wait for all jobs to be processed
job_queue.join()

# Stop the runners
job_queue.put(None)
job_queue.put(None)

runner1.join()
runner2.join()

print("All jobs have been executed.")
