"""Main Scheduling Simulator"""
from typing import List, Dict
from models.process import Process
from .fcfs import FCFSAlgorithm
from .sjf import SJFAlgorithm
from .round_robin import RoundRobinAlgorithm
from .priority import PriorityAlgorithm


class SchedulingSimulator:
    """Main simulator class for all scheduling algorithms"""
    
    def __init__(self, processes: List[Process]):
        self.processes = processes
        self.results = {}
        self.fcfs_algo = FCFSAlgorithm()
        self.sjf_algo = SJFAlgorithm()
        self.round_robin_algo = RoundRobinAlgorithm()
        self.priority_algo = PriorityAlgorithm()
    
    def _clone(self):
        """Create fresh copies of processes to avoid mutation between algorithms"""
        return [p.clone() for p in self.processes]
    
    def fcfs(self) -> dict:
        """First Come First Served - Non-preemptive"""
        return self.fcfs_algo.execute(self._clone())
    
    def sjf(self) -> dict:
        """Shortest Job First - Non-preemptive"""
        return self.sjf_algo.execute(self._clone())
    
    def round_robin(self, time_quantum: int = 3) -> dict:
        """Round Robin - Preemptive"""
        return self.round_robin_algo.execute(self._clone(), time_quantum=time_quantum)
    
    def priority_scheduling(self) -> dict:
        """Priority Scheduling - Non-preemptive"""
        return self.priority_algo.execute(self._clone())
    
    def run_all(self, time_quantum: int = 3) -> dict:
        """Run all scheduling algorithms and return combined results"""
        results = {
            "fcfs": self.fcfs(),
            "sjf": self.sjf(),
            "round_robin": self.round_robin(time_quantum),
            "priority": self.priority_scheduling()
        }
        return results

