"""Process Data Model"""
from dataclasses import dataclass


@dataclass
class Process:
    """Represents a process with all its attributes"""
    pid: str
    arrival_time: int
    burst_time: int
    priority: int
    remaining_time: int = 0
    finish_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    
    def __post_init__(self):
        self.remaining_time = self.burst_time
    
    def to_dict(self) -> dict:
        """Convert process to dictionary"""
        return {
            "pid": self.pid,
            "arrival_time": self.arrival_time,
            "burst_time": self.burst_time,
            "priority": self.priority,
            "finish_time": self.finish_time,
            "turnaround_time": self.turnaround_time,
            "waiting_time": self.waiting_time
        }
    
    def clone(self):
        """Create a fresh copy of the process"""
        return Process(
            pid=self.pid,
            arrival_time=self.arrival_time,
            burst_time=self.burst_time,
            priority=self.priority
        )


