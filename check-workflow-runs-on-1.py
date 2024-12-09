import threading
import queue
import time

# Define a queue to hold the jobs
job_queue = queue.Queue()

# Define the runners
class Runner(threading.Thread):
    def __init__(self, name, start_event, stop_event):
        threading.Thread.__init__(self)
        self.name = name
        self.start_event = start_event
        self.stop_event = stop_event

    def run(self):
        self.start_event.wait()  # Wait until the start event is set
        while not self.stop_event.is_set():
            try:
                job = job_queue.get(timeout=1)
                print(f"{self.name} is executing job {job}")
                time.sleep(60)  # Simulate job execution time
                print(f"{self.name} has completed job {job}")
                job_queue.task_done()
            except queue.Empty:
                break

# Create events to control the runners
runner1_start_event = threading.Event()
runner2_start_event = threading.Event()
stop_event = threading.Event()

# Create runners
runner1 = Runner("ubuntu-latest", runner1_start_event, stop_event)
runner2 = Runner("windows-latest", runner2_start_event, stop_event)

# Start runners
runner1.start()
runner2.start()

# Add jobs to the queue
for job in range(1, 11):
    job_queue.put(job)

# Start Runner 1
runner1_start_event.set()

# Wait for Runner 1 to finish all jobs
job_queue.join()

# Stop Runner 1 and start Runner 2
stop_event.set()
runner1.join()

# Reset stop event for Runner 2
stop_event.clear()

# Add more jobs to the queue for Runner 2
for job in range(11, 21):
    job_queue.put(job)

# Start Runner 2
runner2_start_event.set()

# Wait for Runner 2 to finish all jobs
job_queue.join()

# Stop Runner 2
stop_event.set()
runner2.join()

print("All jobs have been executed.")
