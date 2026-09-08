"""
Device Watchdog - Health monitoring for all hardware devices.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Optional

from PySide6.QtCore import QObject, QMutex, QMutexLocker, Signal, QTimer


class DeviceState(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNRESPONSIVE = "unresponsive"
    FAILED = "failed"
    RECOVERING = "recovering"


@dataclass
class DeviceHealth:
    name: str
    state: DeviceState = DeviceState.HEALTHY
    last_heartbeat: float = 0.0
    missed_heartbeats: int = 0
    error_count: int = 0
    last_error: str = ""
    metadata: dict = field(default_factory=dict)


class DeviceWatchdog(QObject):
    """Monitors all hardware devices, emits state changes for UI reaction."""

    device_state_changed = Signal(str, DeviceState, str)
    critical_failure = Signal(str, str)

    HEARTBEAT_TIMEOUT_MS = 2000
    MAX_MISSED_HEARTBEATS = 3
    MAX_ERRORS_BEFORE_FAILED = 5
    RECONNECT_INTERVAL_MS = 5000

    def __init__(self, parent=None):
        super().__init__(parent)
        self.devices: dict[str, DeviceHealth] = {}
        self.mutex = QMutex()
        self.running = False
        self._reconnect_timers: dict[str, QTimer] = {}
        self._reconnect_attempts: dict[str, int] = {}
        self._monitor_timer: Optional[QTimer] = None

    def register_device(self, name: str, expected_hz: float = 30.0,
                        heartbeat_callback: Optional[Callable] = None,
                        reconnect_callback: Optional[Callable] = None) -> None:
        with QMutexLocker(self.mutex):
            self.devices[name] = DeviceHealth(
                name=name,
                metadata={
                    "expected_period_ms": 1000.0 / expected_hz,
                    "heartbeat_cb": heartbeat_callback,
                    "reconnect_cb": reconnect_callback,
                },
            )

    def heartbeat(self, name: str, metadata: Optional[dict] = None) -> None:
        with QMutexLocker(self.mutex):
            dev = self.devices.get(name)
            if dev is None:
                return
            dev.last_heartbeat = time.perf_counter()
            dev.missed_heartbeats = 0
            if metadata:
                dev.metadata.update(metadata)
            if dev.state in (DeviceState.DEGRADED, DeviceState.UNRESPONSIVE):
                self._set_state(name, DeviceState.HEALTHY, "Heartbeat restored")

    def report_error(self, name: str, error: str) -> None:
        with QMutexLocker(self.mutex):
            dev = self.devices.get(name)
            if dev is None:
                return
            dev.error_count += 1
            dev.last_error = error
            if dev.error_count >= self.MAX_ERRORS_BEFORE_FAILED:
                self._set_state(name, DeviceState.FAILED,
                                f"Error threshold exceeded: {error}")

    def start_monitoring(self) -> None:
        if self.running:
            return
        self.running = True
        self._monitor_timer = QTimer(self)
        self._monitor_timer.timeout.connect(self._check_all_devices)
        self._monitor_timer.start(500)

    def stop_monitoring(self) -> None:
        self.running = False
        if self._monitor_timer is not None:
            self._monitor_timer.stop()
            self._monitor_timer = None
        for timer in self._reconnect_timers.values():
            timer.stop()
        self._reconnect_timers.clear()
        self._reconnect_attempts.clear()

    def _check_all_devices(self) -> None:
        now = time.perf_counter()
        with QMutexLocker(self.mutex):
            for name, dev in self.devices.items():
                expected_ms = dev.metadata.get("expected_period_ms", 33.0)
                timeout_ms = max(self.HEARTBEAT_TIMEOUT_MS, expected_ms * 3)

                elapsed_ms = (
                    (now - dev.last_heartbeat) * 1000
                    if dev.last_heartbeat else float("inf")
                )

                if dev.state == DeviceState.HEALTHY:
                    if elapsed_ms > timeout_ms:
                        dev.missed_heartbeats += 1
                        if dev.missed_heartbeats >= self.MAX_MISSED_HEARTBEATS:
                            self._set_state(
                                name, DeviceState.DEGRADED,
                                f"Missed {dev.missed_heartbeats} heartbeats",
                            )

                elif dev.state == DeviceState.DEGRADED:
                    if elapsed_ms > timeout_ms * 2:
                        self._set_state(
                            name, DeviceState.UNRESPONSIVE,
                            "No response to probes",
                        )
                        self._schedule_reconnect(name)

                elif dev.state == DeviceState.FAILED:
                    if dev.metadata.get("reconnect_cb"):
                        self._schedule_reconnect(name)

    def _set_state(self, name: str, state: DeviceState, message: str) -> None:
        dev = self.devices.get(name)
        if dev is None:
            return
        old_state = dev.state
        dev.state = state
        if old_state != state:
            self.device_state_changed.emit(name, state, message)
            if state == DeviceState.FAILED:
                self.critical_failure.emit(name, message)

    def _schedule_reconnect(self, name: str) -> None:
        if name in self._reconnect_timers:
            return
        dev = self.devices.get(name)
        if dev is None:
            return
        cb = dev.metadata.get("reconnect_cb")
        if not cb:
            return

        attempts = self._reconnect_attempts.get(name, 0)
        delay = min(self.RECONNECT_INTERVAL_MS * (2 ** attempts), 60_000)

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._attempt_reconnect(name, cb))
        timer.start(delay)
        self._reconnect_timers[name] = timer
        self._reconnect_attempts[name] = attempts + 1

        self._set_state(
            name, DeviceState.RECOVERING,
            f"Reconnect scheduled in {delay} ms (attempt {attempts + 1})",
        )

    def _attempt_reconnect(self, name: str, callback: Callable) -> None:
        try:
            callback()
            self._reconnect_attempts.pop(name, None)
        except Exception as e:
            self.report_error(name, f"Reconnect failed: {e}")
            self._schedule_reconnect(name)
        finally:
            self._reconnect_timers.pop(name, None)