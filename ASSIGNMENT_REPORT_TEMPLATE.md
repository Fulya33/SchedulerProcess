# CPU Process Scheduling Simulator - Assignment Report
**CENG 305: Operating Systems**  
**Student Name:** [Your Name]  
**Date:** December 19, 2025

---

## 1. Introduction

This report describes the implementation of a CPU Process Scheduling Simulator that implements four fundamental scheduling algorithms: First-Come First-Served (FCFS), Shortest Job First (SJF), Round Robin (RR), and Priority Scheduling. The simulator reads process information from input files, executes each algorithm, and calculates key performance metrics including turnaround time, waiting time, and CPU utilization.

The goal of this assignment was to deepen understanding of CPU scheduling algorithms by implementing them in a simulated environment and comparing their performance characteristics.

---

## 2. Design

### 2.1 High-Level Architecture

The simulator is designed with a modular architecture:

**Main Components:**
- **Process Data Model**: Represents a process with attributes (PID, arrival time, burst time, priority)
- **Scheduling Simulator**: Core class that orchestrates algorithm execution
- **Algorithm Implementations**: Separate methods for each scheduling algorithm
- **Result Calculator**: Computes metrics (turnaround time, waiting time, CPU utilization)

### 2.2 Key Data Structures

1. **Process Class**:
   - `pid`: Process identifier
   - `arrival_time`: Time when process arrives
   - `burst_time`: Total CPU time required
   - `priority`: Process priority (lower number = higher priority)
   - `remaining_time`: For preemptive algorithms (Round Robin)
   - `finish_time`: Calculated after execution
   - `turnaround_time`: finish_time - arrival_time
   - `waiting_time`: turnaround_time - burst_time

2. **Gantt Chart**: List of segments representing CPU execution timeline
   - Each segment: `{"pid": process_id, "start": time, "end": time}`
   - Includes "IDLE" segments when CPU is idle

3. **Ready Queue**: Used in Round Robin to manage processes waiting for CPU

### 2.3 Simulation Clock Management

The simulator uses a discrete event simulation approach:
- **Current Time**: Tracks simulation progress
- **Event-Driven**: Advances time based on process arrivals and completions
- **Idle Time Handling**: Detects when CPU is idle and advances to next arrival

### 2.4 Algorithm-Specific Design Decisions

**FCFS (First-Come First-Served)**:
- Non-preemptive: Process runs to completion once started
- Sorting: Processes sorted by arrival time, then PID for tie-breaking
- Simple queue-based execution

**SJF (Shortest Job First)**:
- Non-preemptive: Selects shortest available job
- Tie-breaking: Shortest burst → earliest arrival → numeric PID
- Maintains list of available processes at each time step

**Round Robin**:
- Preemptive: Time-sliced execution with configurable quantum
- Queue Management: FIFO ready queue, new arrivals added before re-queued processes
- Critical: Processes arriving during execution are added before current process is re-queued

**Priority Scheduling**:
- Non-preemptive: Selects highest priority (lowest number)
- Tie-breaking: Highest priority → earliest arrival → numeric PID
- Similar structure to SJF but uses priority instead of burst time

### 2.5 Key Functions

- `_clone()`: Creates fresh process copies to avoid mutation between algorithms
- `_calculate_results()`: Computes metrics and formats output
- `run_all()`: Executes all algorithms and returns combined results
- `parse_input_file()`: Reads and parses input file format

---

## 3. Results and Analysis

### 3.1 Sample Input Results

**Input File (processes.txt):**
```
P1, 0, 8, 3
P2, 1, 4, 1
P3, 2, 9, 4
P4, 3, 5, 2
```

**Time Quantum for Round Robin:** 3

### 3.2 Performance Comparison Table

| Algorithm | Avg Turnaround Time | Avg Waiting Time | CPU Utilization |
|-----------|---------------------|------------------|------------------|
| FCFS | 15.25 | 8.75 | 100.0% |
| SJF | 14.25 | 7.75 | 100.0% |
| Round Robin (TQ=3) | 20.0 | 13.5 | 100.0% |
| Priority Scheduling | 14.25 | 7.75 | 100.0% |

### 3.3 Detailed Results

**FCFS:**
- Gantt Chart: [0]--P1--[8]--P2--[12]--P3--[21]--P4--[26]
- Processes execute in arrival order
- Simple but may not be optimal for waiting times

**SJF:**
- Gantt Chart: [0]--P1--[8]--P2--[12]--P4--[17]--P3--[26]
- Selects shortest jobs first (P2, then P4, then P3)
- Better average waiting time than FCFS

**Round Robin (TQ=3):**
- Gantt Chart: [0]--P1--[3]--P2--[6]--P3--[9]--P4--[12]--P1--[15]--P2--[16]--P3--[19]--P4--[21]--P1--[23]--P3--[26]
- Time-sliced execution ensures fairness
- Higher waiting time due to context switching overhead (simulated)

**Priority Scheduling:**
- Gantt Chart: [0]--P1--[8]--P2--[12]--P4--[17]--P3--[26]
- Executes by priority: P2 (priority 1), P4 (priority 2), P1 (priority 3), P3 (priority 4)
- Same performance as SJF for this input (coincidence)

---

## 4. Discussion

### 4.1 Best Performing Algorithm

For this specific input, **SJF and Priority Scheduling** both achieved the best performance with:
- Average Turnaround Time: 14.25
- Average Waiting Time: 7.75
- CPU Utilization: 100.0%

**Why SJF performed best:**
SJF minimizes waiting time by always selecting the shortest available job. In this input:
- P2 (burst=4) executes before P4 (burst=5) and P3 (burst=9)
- This reduces the waiting time for shorter processes
- The algorithm is optimal for minimizing average waiting time when all processes arrive at time 0, and performs well even with different arrival times

**Why Priority Scheduling matched SJF:**
In this case, the priority values happened to align with burst times (shorter jobs had higher priority), resulting in identical scheduling decisions.

**Trade-offs:**
- SJF requires knowledge of burst times (not always available)
- May cause starvation for long processes
- Optimal for minimizing waiting time but not always fair

### 4.2 Round Robin: Performance vs. Fairness Trade-off

**Fairness:**
Round Robin ensures fairness by giving each process equal time slices. No process waits indefinitely, making it suitable for interactive systems.

**Performance Impact:**
- **Time Quantum = 3**: Average waiting time = 13.5 (highest among all algorithms)
- The overhead comes from frequent context switching
- Short processes may wait longer than necessary

**Time Quantum Selection:**
- **Too Small (e.g., TQ=1)**: High context switching overhead, poor CPU utilization
- **Too Large (e.g., TQ=20)**: Approaches FCFS behavior, loses fairness benefits
- **Optimal Range**: Typically 10-100ms in real systems, depends on process mix

**Trade-off Analysis:**
- **Small TQ**: Better fairness, worse performance (more overhead)
- **Large TQ**: Better performance, worse fairness (long processes dominate)
- **Balanced TQ**: Compromise between both (TQ=3-5 for this input works reasonably)

### 4.3 Starvation Problem

**Definition:** Starvation occurs when a process is indefinitely delayed from execution, even though it's ready to run.

**Algorithms Prone to Starvation:**
1. **Priority Scheduling**: Low-priority processes can starve if high-priority processes keep arriving
2. **SJF**: Long processes can starve if shorter processes continuously arrive

**Demonstration (starvation.txt):**
```
P1, 0, 2, 1
P2, 1, 2, 1
P3, 2, 2, 1
P4, 3, 2, 1
P5, 0, 10, 5
```

**Priority Scheduling Result:**
- P5 (priority 5) arrives at time 0 but has lowest priority
- P1, P2, P3, P4 (all priority 1) execute first
- P5 waits: 0 → 2 → 4 → 6 → 8 (finishes at 18)
- **Waiting Time for P5: 8 time units** (much higher than others)

**Solution:**
- **Aging**: Gradually increase priority of waiting processes
- **Round Robin**: Prevents starvation by time-slicing
- **Multilevel Queues**: Different queues for different priority ranges

### 4.4 Impact of I/O Bursts on SJF vs. RR

**SJF with I/O:**
- **Problem**: SJF assumes processes run to completion
- **Reality**: Processes perform I/O, blocking CPU
- **Impact**: 
  - Short CPU bursts followed by I/O → SJF works well
  - Long CPU bursts → SJF may not be optimal
  - **Starvation Risk**: I/O-bound processes (short CPU bursts) may starve CPU-bound processes

**Round Robin with I/O:**
- **Advantage**: Time-slicing naturally handles I/O
- **Behavior**: 
  - Process blocks for I/O → removed from ready queue
  - Returns after I/O → added back to queue
  - Fair distribution of CPU time
- **Performance**: 
  - Better for mixed workloads (CPU-bound + I/O-bound)
  - No starvation
  - Slightly higher overhead but more predictable

**Comparison:**
- **I/O-Heavy Workload**: RR performs better (fairness, no starvation)
- **CPU-Heavy Workload**: SJF may perform better (less overhead)
- **Mixed Workload**: RR is generally preferred in real systems

**Real-World Example:**
- **Web Server**: Many short I/O-bound requests → RR preferred
- **Scientific Computing**: Long CPU-bound processes → SJF or FCFS may be better
- **Interactive Systems**: User responsiveness critical → RR or Priority with aging

---

## 5. Conclusion

This assignment successfully implemented four CPU scheduling algorithms and demonstrated their characteristics:

1. **FCFS**: Simple but may not optimize waiting times
2. **SJF**: Optimal for minimizing waiting time but requires burst time knowledge
3. **Round Robin**: Fair and prevents starvation, suitable for interactive systems
4. **Priority Scheduling**: Useful for real-time systems but can cause starvation

The results show that algorithm choice depends on system requirements:
- **Performance**: SJF minimizes waiting time
- **Fairness**: Round Robin ensures equal treatment
- **Real-time**: Priority scheduling for time-critical tasks
- **General-purpose**: Round Robin or multilevel queues

Understanding these trade-offs is crucial for operating system design and performance optimization.

---

## References

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley.
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson.

---

**Code Files:**
- `cli_main.py`: Command-line interface
- `scheduler_fixed.py`: Core algorithm implementations
- `processes.txt`: Sample input file
- `starvation.txt`: Starvation demonstration file


