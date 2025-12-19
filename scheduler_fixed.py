"""
CPU Process Scheduling Simulator - CORRECTED VERSION
All algorithms fixed with proper tie-breaking and queue management
"""

from dataclasses import dataclass
from typing import List, Tuple
import json
import re

def pid_key(pid: str):
    """Extract numeric part of PID for proper sorting (P10 > P2, not P10 < P2)
    Returns a tuple for sorting that handles both numeric and non-numeric PIDs:
    - (0, int_value) for numeric PIDs (sorted first, by number)
    - (1, pid_string) for non-numeric PIDs (sorted after, alphabetically)
    """
    m = re.search(r'\d+', pid)
    if m:
        return (0, int(m.group()))  # Numeric PIDs come first
    else:
        return (1, pid)  # Non-numeric PIDs come after, sorted alphabetically

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

class SchedulingSimulator:
    """Main simulator class for all scheduling algorithms"""
    
    def __init__(self, processes: List[Process]):
        self.processes = processes
        self.results = {}
    
    def _clone(self):
        """Create fresh copies of processes to avoid mutation between algorithms"""
        return [Process(p.pid, p.arrival_time, p.burst_time, p.priority) 
                for p in self.processes]
    
    def fcfs(self) -> dict:
        """First Come First Served - Non-preemptive"""
        # FIXED: Use fresh copies with NUMERIC PID sorting
        # Flatten pid_key tuple when used in compound key
        processes = sorted(self._clone(), key=lambda x: (x.arrival_time, *pid_key(x.pid)))
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
        
        # Total time is when last process finishes (not including trailing idle)
        total_time = current_time
        
        return self._calculate_results("FCFS", processes, gantt, total_time, total_idle)
    
    def sjf(self) -> dict:
        """Shortest Job First - Non-preemptive with proper tie-breaking"""
        # FIXED: Use fresh copies
        processes = self._clone()
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
            
            # Select process: shortest burst, then FCFS (arrival time), then NUMERIC PID
            # THIS IS THE FIX: Proper tie-breaking with numeric PID!
            proc = min(available, key=lambda x: (x.burst_time, x.arrival_time, *pid_key(x.pid)))
            
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
        
        return self._calculate_results("SJF", processes, gantt, total_time, total_idle)
    
    def round_robin(self, time_quantum: int = 3) -> dict:
        """
        Round Robin - Preemptive with CORRECTED queue management
        
        CRITICAL FIX: When a process uses its quantum at time T:
        1. First, add all processes that arrived at or before time T
        2. THEN add the current process back (if not finished)
        
        This ensures new arrivals get priority over re-queued processes!
        """
        # VALIDATION: Prevent infinite loop with invalid time quantum
        if time_quantum <= 0:
            raise ValueError(f"Time quantum must be greater than 0, got {time_quantum}")
        
        # FIXED: Use fresh copies
        processes = self._clone()
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
            
            # CRITICAL FIX: Add processes that arrived DURING execution BEFORE re-queueing current process
            # This ensures if process P finishes at time T and process Q arrives at time T,
            # Q gets queued before P (if P needs more time)
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
        
        return self._calculate_results(f"Round Robin (TQ={time_quantum})", processes, gantt, total_time, total_idle)
    
    def priority_scheduling(self) -> dict:
        """Priority Scheduling - Non-preemptive with proper tie-breaking"""
        # FIXED: Use fresh copies
        processes = self._clone()
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
            # THIS IS THE FIX: Proper tie-breaking with numeric PID!
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
        
        return self._calculate_results("Priority Scheduling", processes, gantt, total_time, total_idle)
    
    def _calculate_results(self, algorithm: str, processes: List[Process], gantt: List[dict], 
                          total_time: int, total_idle: int) -> dict:
        """
        Calculate and format results for an algorithm
        
        IMPORTANT: total_time is when the LAST PROCESS finishes, not including trailing idle time.
        CPU Utilization = (time spent executing processes) / (time from start to last process finish) * 100
        """
        avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)
        avg_waiting = sum(p.waiting_time for p in processes) / len(processes)
        
        # CPU Utilization calculation with edge case protection
        # Total time = time from start (0) to when last process finishes
        # Busy time = total_time - total_idle
        if total_time > 0:
            cpu_utilization = (total_time - total_idle) / total_time * 100
        else:
            # Edge case: all processes have 0 burst time
            cpu_utilization = 0.0
        
        process_results = [
            {
                "pid": p.pid,
                "arrival_time": p.arrival_time,
                "burst_time": p.burst_time,
                "priority": p.priority,
                "finish_time": p.finish_time,
                "turnaround_time": p.turnaround_time,
                "waiting_time": p.waiting_time
            }
            for p in sorted(processes, key=lambda x: pid_key(x.pid))
        ]
        
        return {
            "algorithm": algorithm,
            "gantt_chart": gantt,
            "processes": process_results,
            "metrics": {
                "avg_turnaround_time": round(avg_turnaround, 2),
                "avg_waiting_time": round(avg_waiting, 2),
                "cpu_utilization": round(cpu_utilization, 2)
            }
        }
    
    def run_all(self, time_quantum: int = 3) -> dict:
        """Run all scheduling algorithms and return combined results"""
        results = {
            "fcfs": self.fcfs(),
            "sjf": self.sjf(),
            "round_robin": self.round_robin(time_quantum),
            "priority": self.priority_scheduling()
        }
        return results


def parse_input_file(filename: str) -> List[Process]:
    """Parse input file and return list of processes"""
    processes = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 4:
                processes.append(Process(
                    pid=parts[0],
                    arrival_time=int(parts[1]),
                    burst_time=int(parts[2]),
                    priority=int(parts[3])
                ))
    return processes


def main():
    """Main entry point for command line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scheduler_fixed.py <input_file> [time_quantum]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    time_quantum = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    # Parse processes
    processes = parse_input_file(input_file)
    
    # Run simulation
    simulator = SchedulingSimulator(processes)
    results = simulator.run_all(time_quantum)
    
    # Print results
    for algo_key, result in results.items():
        print(f"\n{'='*60}")
        print(f"Algorithm: {result['algorithm']}")
        print(f"{'='*60}")
        
        # Gantt Chart
        print("\nGantt Chart:")
        gantt_str = ""
        for segment in result['gantt_chart']:
            gantt_str += f"[{segment['start']}]--{segment['pid']}--"
        gantt_str += f"[{result['gantt_chart'][-1]['end']}]"
        print(gantt_str)
        
        # Process table
        print(f"\n{'Process':<10} | {'Finish Time':<12} | {'Turnaround Time':<16} | {'Waiting Time':<12}")
        print("-" * 60)
        for proc in result['processes']:
            print(f"{proc['pid']:<10} | {proc['finish_time']:<12} | {proc['turnaround_time']:<16} | {proc['waiting_time']:<12}")
        
        # Metrics
        print(f"\nAverage Turnaround Time: {result['metrics']['avg_turnaround_time']}")
        print(f"Average Waiting Time: {result['metrics']['avg_waiting_time']}")
        print(f"CPU Utilization: {result['metrics']['cpu_utilization']}%")


if __name__ == "__main__":
    main()