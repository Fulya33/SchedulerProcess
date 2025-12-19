"""Process Management Service"""
from typing import List, Optional
from models.process import Process


class ProcessService:
    """Manages process operations"""
    
    def __init__(self):
        self.processes: List[Process] = []
    
    def add_process(self, pid: str, arrival_time: int, burst_time: int, priority: int) -> bool:
        """
        Add a new process
        
        Returns:
            True if added successfully, False if PID already exists
        """
        if self.get_process_by_pid(pid) is not None:
            return False
        
        process = Process(pid, arrival_time, burst_time, priority)
        self.processes.append(process)
        return True
    
    def remove_process(self, pid: str) -> bool:
        """Remove a process by PID"""
        process = self.get_process_by_pid(pid)
        if process:
            self.processes.remove(process)
            return True
        return False
    
    def get_process_by_pid(self, pid: str) -> Optional[Process]:
        """Get a process by PID"""
        for proc in self.processes:
            if proc.pid == pid:
                return proc
        return None
    
    def clear_all(self) -> None:
        """Clear all processes"""
        self.processes.clear()
    
    def get_all(self) -> List[Process]:
        """Get all processes"""
        return self.processes.copy()
    
    def count(self) -> int:
        """Get number of processes"""
        return len(self.processes)
    
    def has_processes(self) -> bool:
        """Check if there are any processes"""
        return len(self.processes) > 0


