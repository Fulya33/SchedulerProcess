"""Priority Scheduling Algorithm"""
from typing import List, Dict
from models.process import Process
from utils.pid_utils import pid_key
from .base_algorithm import BaseAlgorithm


class PriorityAlgorithm(BaseAlgorithm):
    """Priority Scheduling - Non-preemptive with proper tie-breaking"""
    
    def execute(self, processes: List[Process], **kwargs) -> Dict:
        """
        Execute Priority Scheduling algorithm
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            Dictionary with results
        """
        gantt = []
        current_time = 0
        completed = []
        total_idle = 0
        
        while len(completed) < len(processes):
            # Get available processes
            available = [p for p in processes if p.arrival_time <= current_time and p not in completed]
            
            if not available:
                # CPU idle - jump to next arrival
                next_arrival = min([p.arrival_time for p in processes if p not in completed])
                idle_duration = next_arrival - current_time
                gantt.append({"pid": "IDLE", "start": current_time, "end": next_arrival})
                total_idle += idle_duration
                current_time = next_arrival
                continue
            
            # Select process: highest priority (lowest number), then FCFS, then NUMERIC PID
            proc = min(available, key=lambda x: (x.priority, x.arrival_time, *pid_key(x.pid)))
            
            # Execute process
            start_time = current_time
            current_time += proc.burst_time
            gantt.append({"pid": proc.pid, "start": start_time, "end": current_time})
            
            # Calculate metrics
            proc.finish_time = current_time
            proc.turnaround_time = proc.finish_time - proc.arrival_time
            proc.waiting_time = proc.turnaround_time - proc.burst_time
            completed.append(proc)
        
        total_time = current_time
        
        return self.calculate_results("Priority Scheduling", processes, gantt, total_time, total_idle)


