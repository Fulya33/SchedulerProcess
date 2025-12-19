"""Simulation Service"""
from typing import List, Dict
from models.process import Process
from algorithms.scheduler import SchedulingSimulator


class SimulationService:
    """Handles simulation operations"""
    
    def __init__(self, processes: List[Process]):
        self.processes = processes
        self.simulator = SchedulingSimulator(processes)
    
    def run_all_algorithms(self, time_quantum: int = 3) -> Dict[str, dict]:
        """
        Run all scheduling algorithms
        
        Args:
            time_quantum: Time quantum for Round Robin algorithm
            
        Returns:
            Dictionary with results for each algorithm
        """
        return self.simulator.run_all(time_quantum)
    
    def run_single_algorithm(self, algorithm: str, time_quantum: int = 3) -> dict:
        """
        Run a single scheduling algorithm
        
        Args:
            algorithm: Algorithm name ('fcfs', 'sjf', 'round_robin', 'priority')
            time_quantum: Time quantum for Round Robin
            
        Returns:
            Results dictionary for the algorithm
        """
        if algorithm == 'fcfs':
            return self.simulator.fcfs()
        elif algorithm == 'sjf':
            return self.simulator.sjf()
        elif algorithm == 'round_robin':
            return self.simulator.round_robin(time_quantum)
        elif algorithm == 'priority':
            return self.simulator.priority_scheduling()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


