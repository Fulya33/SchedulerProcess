CPU Process Scheduling Simulator
CENG 305 Assignment
==========================================

COMPILATION/EXECUTION INSTRUCTIONS
==================================

This project is written in Python 3 and requires PyQt6 for the GUI version.

REQUIREMENTS:
- Python 3.8 or higher
- PyQt6 (for GUI version only)
- matplotlib (for GUI version only)
- numpy (for GUI version only)

INSTALLATION:
1. Install Python dependencies:
   pip install -r requirements_pyqt.txt

   OR for command-line only (no GUI):
   pip install (no additional packages needed for CLI)

EXECUTION:
==========

1. COMMAND-LINE INTERFACE (Required for Assignment):
   ------------------------------------------------
   python cli_main.py <input_file> [time_quantum]
   
   Examples:
   python cli_main.py processes.txt 3
   python cli_main.py starvation.txt 2
   
   This will run all 4 scheduling algorithms and display results
   in the exact format required by the assignment.

2. GUI INTERFACE (Bonus Feature):
   ------------------------------
   python main.py
   
   This opens a graphical interface where you can:
   - Add processes manually
   - Upload process files
   - Run simulations
   - View Gantt charts
   - Compare algorithms
   - Export results to PDF

INPUT FILE FORMAT:
==================
Each line should contain: Process_ID, Arrival_Time, Burst_Time, Priority

Example (processes.txt):
P1, 0, 8, 3
P2, 1, 4, 1
P3, 2, 9, 4
P4, 3, 5, 2

Lines starting with # are treated as comments and ignored.

ALGORITHMS IMPLEMENTED:
========================
1. First-Come, First-Served (FCFS) - Non-preemptive
2. Shortest Job First (SJF) - Non-preemptive
3. Round Robin (RR) - Preemptive with configurable time quantum
4. Priority Scheduling - Non-preemptive (lower number = higher priority)

FEATURES:
=========
- Correct tie-breaking using FCFS when metrics are equal
- Proper handling of idle time
- Accurate calculation of all metrics:
  * Finish Time
  * Turnaround Time
  * Waiting Time
  * CPU Utilization
- Gantt chart generation
- Starvation demonstration (see starvation.txt)

PROJECT STRUCTURE:
==================
- cli_main.py          : Command-line interface (assignment requirement)
- main.py              : GUI application entry point
- scheduler_fixed.py    : Core scheduling algorithms
- processes.txt        : Sample input file
- starvation.txt       : Starvation demonstration file
- README.txt           : This file

For detailed architecture documentation, see README_ARCHITECTURE.md

AUTHOR:
=======
[Your Name]
CENG 305 - Operating Systems
December 2025


