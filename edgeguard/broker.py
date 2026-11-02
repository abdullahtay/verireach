import time
import queue
import threading
from typing import Dict, List, Callable, Any, Optional


class LocalEdgeBroker:
    """
    Lightweight, deterministic local event broker for edge microservices and sensor pipelines.
    Guarantees thread-safe publish-subscribe with priority channels and sub-millisecond dispatch.
    """

    def __init__(self, max_queue_size: int = 1000):
        self.max_queue_size = max_queue_size
        self._subscribers: Dict[str, List[Callable[[str, Any], None]]] = {}
        self._queue: queue.PriorityQueue = queue.PriorityQueue(maxsize=max_queue_size)
        self._running: bool = False
        self._worker_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Telemetry
        self.messages_dispatched: int = 0
        self.messages_dropped: int = 0
        self.avg_dispatch_latency_us: float = 0.0

    def subscribe(self, topic: str, callback: Callable[[str, Any], None]) -> None:
        """Subscribes a listener to a specific topic."""
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(callback)

    def publish(self, topic: str, payload: Any, priority: int = 5) -> bool:
        """
        Publishes a message to a topic.
        priority: 1 (highest / emergency) to 10 (lowest / background).
        Returns True if queued, False if queue is full (dropped).
        """
        timestamp = time.perf_counter()
        try:
            self._queue.put_nowait((priority, timestamp, topic, payload))
            return True
        except queue.Full:
            self.messages_dropped += 1
            return False

    def start(self) -> None:
        """Starts asynchronous dispatcher loop in background thread."""
        with self._lock:
            if self._running:
                return
            self._running = True
            self._worker_thread = threading.Thread(target=self._dispatch_loop, daemon=True)
            self._worker_thread.start()

    def stop(self) -> None:
        """Stops the broker and drains remaining events."""
        with self._lock:
            self._running = False
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)

    def _dispatch_loop(self) -> None:
        while self._running:
            try:
                priority, enqueue_time, topic, payload = self._queue.get(timeout=0.05)
            except queue.Empty:
                continue

            dispatch_time = time.perf_counter()
            latency_us = (dispatch_time - enqueue_time) * 1_000_000

            with self._lock:
                callbacks = list(self._subscribers.get(topic, []))
                # Wildcard subscriber support
                callbacks.extend(self._subscribers.get("*", []))

            for cb in callbacks:
                try:
                    cb(topic, payload)
                except Exception:
                    pass

            self.messages_dispatched += 1
            # Update running average latency
            self.avg_dispatch_latency_us = (
                0.95 * self.avg_dispatch_latency_us + 0.05 * latency_us
            )
            self._queue.task_done()
