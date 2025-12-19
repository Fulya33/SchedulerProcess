"""
Command-Line Interface for CPU Scheduler
Matches assignment requirements exactly
"""
import sys
from scheduler_fixed import SchedulingSimulator, parse_input_file


def print_results(result):
    """Print results in the exact format required by assignment"""
    print(f"\n--- Scheduling Algorithm: {result['algorithm']} ---")
    
    # Gantt Chart
    gantt_str = ""
    for segment in result['gantt_chart']:
        gantt_str += f"[{segment['start']}]--{segment['pid']}--"
    gantt_str += f"[{result['gantt_chart'][-1]['end']}]"
    print(f"Gantt Chart: {gantt_str}")
    
    # Process table
    print(f"\n{'Process':<10} | {'Finish Time':<12} | {'Turnaround Time':<16} | {'Waiting Time':<12}")
    print("-" * 60)
    for proc in result['processes']:
        print(f"{proc['pid']:<10} | {proc['finish_time']:<12} | {proc['turnaround_time']:<16} | {proc['waiting_time']:<12}")
    
    # Metrics
    print(f"\nAverage Turnaround Time: {result['metrics']['avg_turnaround_time']}")
    print(f"Average Waiting Time: {result['metrics']['avg_waiting_time']}")
    print(f"CPU Utilization: {result['metrics']['cpu_utilization']}%")


def main():
    """Main entry point for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python cli_main.py <input_file> [time_quantum]")
        print("Example: python cli_main.py processes.txt 3")
        sys.exit(1)
    
    input_file = sys.argv[1]
    time_quantum = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    try:
        # Parse processes
        processes = parse_input_file(input_file)
        
        if not processes:
            print(f"Error: No valid processes found in {input_file}")
            sys.exit(1)
        
        # Run simulation
        simulator = SchedulingSimulator(processes)
        results = simulator.run_all(time_quantum)
        
        # Print results for each algorithm
        print_results(results['fcfs'])
        print_results(results['sjf'])
        print_results(results['round_robin'])
        print_results(results['priority'])
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


