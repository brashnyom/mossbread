from scheduling import Event, PriorityQueue, Scheduler


class TrackedEvent(Event):
    def __init__(self, event_id, execution_tracker):
        self.id = event_id
        self.tracker = execution_tracker

    def execute(self):
        self.tracker.add(self.id)


def test_queue_add():
    queue = PriorityQueue()
    queue.add(Event(), 0)
    queue.add(Event(), 3)
    queue.add(Event(), 1)
    queue.add(Event(), 2)
    queue.add(Event(), 5)
    queue.add(Event(), 10)
    queue.add(Event(), 7)
    queue.add(Event(), 4)

    for i in range(0, 4):
        assert queue._queue[i][0] == i


def test_queue_pop():
    queue = PriorityQueue()
    queue.add(Event(), 2)
    queue.add(Event(), 3)
    queue.add(Event(), 1)
    elem = queue.pop()
    assert elem[0] == 1


def test_queue_delete_by_ref():
    event = Event()
    queue = PriorityQueue()
    queue.add(Event(), 2)
    queue.add(Event(), 3)
    queue.add(Event(), 1)
    queue.add(event, 4)
    queue.delete_by_ref(event)
    assert len(queue._queue) == 3 and queue._queue[-1][0] == 3


def test_queue_adjust_priorities():
    queue = PriorityQueue()
    queue.add(Event(), 2)
    queue.add(Event(), 3)
    queue.add(Event(), 1)
    queue.adjust_priorities(-1)
    for i in range(0, 3):
        assert queue._queue[i][0] == i


def test_scheduler_schedule():
    scheduler = Scheduler()
    scheduler.schedule(Event(), 5)
    assert len(scheduler.priority_queue._queue) == 1


def test_scheduler_unschedule():
    event = Event()
    scheduler = Scheduler()
    scheduler.schedule(event, 6)
    scheduler.schedule(Event(), 5)
    scheduler.schedule(Event(), 7)

    scheduler.unschedule(event)

    for priority, scheduled_event in scheduler.priority_queue._queue:
        assert scheduled_event is not event


def test_scheduler_tick():
    scheduler = Scheduler()
    scheduler.schedule(TrackedEvent("event one", set()), 1)

    latest_event = scheduler.tick()
    assert latest_event.id == "event one"


def test_scheduler_tick_multiple_events():
    executed_events = set()

    scheduler = Scheduler()
    scheduler.schedule(TrackedEvent("event one", executed_events), 1)
    scheduler.schedule(TrackedEvent("event two", executed_events), 2)
    scheduler.schedule(TrackedEvent("event three", executed_events), 2)
    scheduler.schedule(TrackedEvent("event four", executed_events), 3)

    scheduler.tick()
    assert len(scheduler.priority_queue._queue) == 3
    assert executed_events == {"event one"}

    scheduler.tick()
    assert len(scheduler.priority_queue._queue) == 2
    assert executed_events == {"event one", "event two"}

    scheduler.tick()
    assert len(scheduler.priority_queue._queue) == 1
    assert executed_events == {"event one", "event two", "event three"}

    scheduler.tick()
    assert len(scheduler.priority_queue._queue) == 0
    assert executed_events == {"event one", "event two", "event three", "event four"}
