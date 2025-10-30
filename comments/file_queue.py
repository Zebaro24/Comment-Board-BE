from queue import Queue
from threading import Thread
from .utils import resize_image_if_needed


class FileResizeQueue:
    def __init__(self, num_workers=1):
        self.queue = Queue()
        self.workers = []
        self.num_workers = num_workers
        self._stop_signal = object()

    def start(self):
        for _ in range(self.num_workers):
            t = Thread(target=self._worker, daemon=True)
            t.start()
            self.workers.append(t)

    def stop(self):
        for _ in range(self.num_workers):
            self.queue.put(self._stop_signal)
        for t in self.workers:
            t.join()

    def add_task(self, file_path):
        self.queue.put(file_path)

    def _worker(self):
        while True:
            file_instance  = self.queue.get()
            if file_instance is self._stop_signal:
                break
            try:
                new_file = resize_image_if_needed(file_instance.file)
                if new_file:
                    file_instance.file = new_file
                    file_instance.save(update_fields=['file'])
            except Exception as e:
                print(f"Error resizing {file_instance.id}: {e}")
            self.queue.task_done()

file_queue = FileResizeQueue(num_workers=2)