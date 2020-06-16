from typing import List


class Event:
    def execute(self):
        raise NotImplementedError()


class PriorityQueue:
    def __init__(self):
        self._queue: List[list] = list()

    def add(self, event: Event, priority: float):
        insertion_index: int = 0
        for enqueued_event in self._queue:
            if enqueued_event[0] > priority:
                break
            insertion_index += 1
        self._queue.insert(insertion_index, [priority, event])

    def pop(self) -> list:
        return self._queue.pop(0)

    def delete_by_ref(self, obj):
        index = None
        for idx, enqueued_event in enumerate(self._queue):
            if enqueued_event[1] is obj:
                index = idx
        del self._queue[index]

    def adjust_priorities(self, amount: float):
        for enqueued_event in self._queue:
            enqueued_event[0] += amount


class Scheduler:
    def __init__(self):
        self.priority_queue: PriorityQueue = PriorityQueue()

    def schedule(self, event: Event, delay):
        self.priority_queue.add(event, delay)

    def unschedule(self, event: Event):
        self.priority_queue.delete_by_ref(event)

    def tick(self) -> Event:
        delay, latest_event = self.priority_queue.pop()
        self.priority_queue.adjust_priorities(-delay)
        latest_event.execute()
        return latest_event
