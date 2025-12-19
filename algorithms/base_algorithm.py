"""Base Algorithm Interface"""
from abc import ABC, abstractmethod
from typing import List, Dict
from models.process import Process


class BaseAlgorithm(ABC):
    """Base class for all scheduling algorithms"""
    
    @abstractmethod
    def execute(self, processes: List[Process], **kwargs) -> Dict:
        """
        Execute the scheduling algorithm
        
        Args:
            processes: List of processes to schedule
            **kwargs: Additional algorithm-specific parameters
            
        Returns:
            Dictionary with algorithm results
        """
        pass
    
    def calculate_results(self, algorithm_name: str, processes: List[Process], 
                         gantt: List[dict], total_time: int, total_idle: int) -> dict:
        """
        Calculate and format results for an algorithm
        
        Args:
            algorithm_name: Name of the algorithm
            processes: List of scheduled processes
            gantt: Gantt chart data
            total_time: Total execution time
            total_idle: Total idle time
            
        Returns:
            Formatted results dictionary
        """
        from utils.pid_utils import pid_key
        
        if not processes:
            return {
                "algorithm": algorithm_name,
                "gantt_chart": gantt,
                "processes": [],
                "metrics": {
                    "avg_turnaround_time": 0.0,
                    "avg_waiting_time": 0.0,
                    "cpu_utilization": 0.0
                }
            }
        
        avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)
        avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
        
        if total_time > 0:
            cpu_utilization = (total_time - total_idle) / total_time * 100
        else:
            cpu_utilization = 0.0
        
        process_results = [
            p.to_dict()
            for p in sorted(processes, key=lambda x: pid_key(x.pid))
        ]
        
        return {
            "algorithm": algorithm_name,
            "gantt_chart": gantt,
            "processes": process_results,
            "metrics": {
                "avg_turnaround_time": round(avg_turnaround, 2),
                "avg_waiting_time": round(avg_waiting, 2),
                "cpu_utilization": round(cpu_utilization, 2)
            }
        }


