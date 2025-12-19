"""First Come First Served Algorithm"""
from typing import List, Dict
from models.process import Process
from utils.pid_utils import pid_key
from .base_algorithm import BaseAlgorithm


class FCFSAlgorithm(BaseAlgorithm):
    """First Come First Served - Non-preemptive"""
    
    def execute(self, processes: List[Process], **kwargs) -> Dict:
        """
        Execute FCFS algorithm
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            Dictionary with results
        """
        # Sort by arrival time, then by PID
        processes = sorted(processes, key=lambda x: (x.arrival_time, *pid_key(x.pid)))
        gantt = []
        current_time = 0
        total_idle = 0
        
        for proc in processes:
            # Handle idle time
            if current_time < proc.arrival_time:
                idle_duration = proc.arrival_time - current_time
                gantt.append({"pid": "IDLE", "start": current_time, "end": proc.arrival_time})
                total_idle += idle_duration
                current_time = proc.arrival_time
            
            # Execute process
            start_time = current_time
            current_time += proc.burst_time
            gantt.append({"pid": proc.pid, "start": start_time, "end": current_time})
            
            # Calculate metrics
            proc.finish_time = current_time
            proc.turnaround_time = proc.finish_time - proc.arrival_time
            proc.waiting_time = proc.turnaround_time - proc.burst_time
        
        total_time = current_time
        
        return self.calculate_results("FCFS", processes, gantt, total_time, total_idle)


