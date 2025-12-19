"""Round Robin Algorithm"""
from typing import List, Dict
from models.process import Process
from utils.pid_utils import pid_key
from .base_algorithm import BaseAlgorithm


class RoundRobinAlgorithm(BaseAlgorithm):
    """Round Robin - Preemptive with corrected queue management"""
    
    def execute(self, processes: List[Process], time_quantum: int = 3, **kwargs) -> Dict:
        """
        Execute Round Robin algorithm
        
        Args:
            processes: List of processes to schedule
            time_quantum: Time quantum for Round Robin
            
        Returns:
            Dictionary with results
        """
        if time_quantum <= 0:
            raise ValueError(f"Time quantum must be greater than 0, got {time_quantum}")
        
        gantt = []
        current_time = 0
        ready_queue = []
        completed = []
        total_idle = 0
        
        # Track which processes have been added to ready queue
        remaining = sorted(processes, key=lambda x: (x.arrival_time, *pid_key(x.pid)))
        
        while len(completed) < len(processes):
            # Add newly arrived processes to ready queue (BEFORE processing)
            newly_arrived = [p for p in remaining if p.arrival_time <= current_time]
            for proc in newly_arrived:
                ready_queue.append(proc)
                remaining.remove(proc)
            
            if not ready_queue:
                # CPU idle - jump to next arrival
                if remaining:
                    next_arrival = min([p.arrival_time for p in remaining])
                    idle_duration = next_arrival - current_time
                    gantt.append({"pid": "IDLE", "start": current_time, "end": next_arrival})
                    total_idle += idle_duration
                    current_time = next_arrival
                continue
            
            # Get next process from ready queue (FIFO order)
            proc = ready_queue.pop(0)
            
            # Execute for time quantum or remaining time
            execution_time = min(time_quantum, proc.remaining_time)
            start_time = current_time
            current_time += execution_time
            gantt.append({"pid": proc.pid, "start": start_time, "end": current_time})
            
            proc.remaining_time -= execution_time
            
            # Add processes that arrived DURING execution BEFORE re-queueing current process
            during_execution = [p for p in remaining if p.arrival_time <= current_time]
            for p in during_execution:
                ready_queue.append(p)
                remaining.remove(p)
            
            # Check if process is complete
            if proc.remaining_time == 0:
                proc.finish_time = current_time
                proc.turnaround_time = proc.finish_time - proc.arrival_time
                proc.waiting_time = proc.turnaround_time - proc.burst_time
                completed.append(proc)
            else:
                # Put back in ready queue (AFTER newly arrived processes)
                ready_queue.append(proc)
        
        total_time = current_time
        
        return self.calculate_results(f"Round Robin (TQ={time_quantum})", processes, gantt, total_time, total_idle)


