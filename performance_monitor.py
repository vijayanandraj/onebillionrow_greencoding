import time
import psutil
from contextlib import contextmanager

class PerformanceMonitor:
    def __init__(self):
        self.process = psutil.Process()

    def memory_usage(self):
        """ Returns the current memory usage of the process in GB. """
        return self.process.memory_info().rss / (1024 ** 3)

    @contextmanager
    def track_performance(self):
        """ Context manager to measure CPU and memory usage. """
        start_time = time.time()
        start_cpu = self.process.cpu_percent(interval=None)
        start_memory = self.memory_usage()
        yield
        end_time = time.time()
        end_cpu = self.process.cpu_percent(interval=None)
        end_memory = self.memory_usage()

        self.processing_time = end_time - start_time
        self.cpu_usage = (end_cpu - start_cpu) / psutil.cpu_count()
        self.memory_used = end_memory - start_memory

    def get_metrics(self):
        """ Retrieve the collected metrics. """
        return {
            'processing_time': self.processing_time,
            'cpu_usage': self.cpu_usage,
            'memory_used': self.memory_used
        }
