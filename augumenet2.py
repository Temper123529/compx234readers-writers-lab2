from __future__ import annotations
import random
import threading
import time

class ReadersWritersMonitor:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.active_readers = 0
        self.active_writers = 0
        self.waiting_writers = 0

    def start_read(self, reader_id: int) -> None:
        with self.condition:
            while self.active_writers > 0:
                print(f"Reader {reader_id} is waiting to read")
                self.condition.wait()
            self.active_readers += 1
            print(f"Reader {reader_id} starts reading. Active readers = {self.active_readers}")

    def end_read(self, reader_id: int) -> None:
        with self.condition:
            self.active_readers -= 1
            print(f"Reader {reader_id} stops reading. Active readers = {self.active_readers}")
            if self.active_readers == 0:
                self.condition.notify_all()

    def start_write(self, writer_id: int) -> None:
        with self.condition:
            self.waiting_writers += 1
            while self.active_readers > 0 or self.active_writers > 0:
                print(f"Writer {writer_id} is waiting to write")
                self.condition.wait()
            self.waiting_writers -= 1
            self.active_writers += 1
            print(f"Writer {writer_id} starts writing")

    def end_write(self, writer_id: int) -> None:
        with self.condition:
            self.active_writers -= 1
            print(f"Writer {writer_id} stops writing")
            self.condition.notify_all()

class Reader(threading.Thread):
    def __init__(self, reader_id: int, monitor: ReadersWritersMonitor, rounds: int = 3) -> None:
        super().__init__()
        self.reader_id = reader_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.1, 0.7))
            print(f"Reader {self.reader_id} wants to read")
            self.monitor.start_read(self.reader_id)
            print(f"Reader {self.reader_id} is READING")
            time.sleep(random.uniform(0.3, 0.8))
            self.monitor.end_read(self.reader_id)
            print(f"Reader {self.reader_id} finished reading")

class Writer(threading.Thread):
    def __init__(self, writer_id: int, monitor: ReadersWritersMonitor, rounds: int = 2) -> None:
        super().__init__()
        self.writer_id = writer_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.2, 0.9))
            print(f"Writer {self.writer_id} wants to write")
            self.monitor.start_write(self.writer_id)
            print(f"Writer {self.writer_id} is WRITING")
            time.sleep(random.uniform(0.4, 0.9))
            self.monitor.end_write(self.writer_id)
            print(f"Writer {self.writer_id} finished writing")

def main() -> None:
    random.seed(42)
    monitor = ReadersWritersMonitor()

    readers = [
        Reader(1, monitor),
        Reader(2, monitor),
        Reader(3, monitor)
    ]

    writers = [
        Writer(1, monitor),
        Writer(2, monitor)
    ]

    all_threads = readers + writers

    print("Starting Readers-Writers Simulation...")
    for thread in all_threads:
        thread.start()

    for thread in all_threads:
        thread.join()

    print("\nSimulation completed successfully!")

if __name__ == "__main__":
    main()