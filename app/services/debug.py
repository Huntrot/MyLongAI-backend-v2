import psutil
import os

def log_memory(stage=""):
    process = psutil.Process(os.getpid())
    print(
        f"[MEMORY] {stage}: "
        f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
    )