"""
Session Logger - Structured JSONL logging with rotation.
"""

import time
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class SessionLogger:
    """Structured session logger writing JSONL format with automatic rotation."""

    def __init__(self, log_dir: str = "logs", session_name: Optional[str] = None):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        if session_name is None:
            session_name = f"session_{int(time.time())}"

        self.logger = logging.getLogger(f"maldi_session_{session_name}")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            handler = RotatingFileHandler(
                self.log_dir / f"{session_name}.jsonl",
                maxBytes=10_000_000,
                backupCount=5,
            )
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)

    def log_event(self, event_type: str, data: dict) -> None:
        record = {"timestamp": time.time(), "type": event_type, **data}
        self.logger.info(json.dumps(record))

    def log_deposit_start(self, channel: int, pressure: float,
                          target_vol: float, lookahead_ms: float) -> None:
        self.log_event("deposit_start", {
            "channel": channel, "pressure": pressure,
            "target_vol_pL": target_vol, "lookahead_ms": lookahead_ms,
        })

    def log_deposit_end(self, channel: int, final_vol: float,
                        duration_ms: float, success: bool) -> None:
        self.log_event("deposit_end", {
            "channel": channel, "final_vol_pL": final_vol,
            "duration_ms": duration_ms, "success": success,
        })

    def log_device_state_change(self, device: str, old_state: str,
                                 new_state: str, reason: str) -> None:
        self.log_event("device_state_change", {
            "device": device, "old_state": old_state,
            "new_state": new_state, "reason": reason,
        })

    def log_frame_stats(self, captured: int, dropped: int,
                        latency_ms: float, fps: float) -> None:
        self.log_event("frame_stats", {
            "captured": captured, "dropped": dropped,
            "latency_ms": round(latency_ms, 2), "fps": round(fps, 1),
        })

    def log_error(self, component: str, error: str, severity: str = "ERROR") -> None:
        self.log_event("error", {
            "component": component, "error": error, "severity": severity,
        })