# CPU Scheduler - Modular Architecture

## Project Structure

This project follows a clean, modular architecture with clear separation of concerns:

```
Cpu-Scheduler3/
├── main.py                 # Application entry point
├── models/                 # Data models
│   ├── __init__.py
│   └── process.py         # Process data model
├── algorithms/            # Scheduling algorithms
│   ├── __init__.py
│   ├── base_algorithm.py  # Base class for all algorithms
│   ├── scheduler.py       # Main scheduler coordinator
│   ├── fcfs.py           # First Come First Served
│   ├── sjf.py            # Shortest Job First
│   ├── round_robin.py    # Round Robin
│   └── priority.py       # Priority Scheduling
├── services/              # Business logic services
│   ├── __init__.py
│   ├── process_service.py    # Process management
│   ├── simulation_service.py # Simulation orchestration
│   └── file_service.py       # File I/O operations
├── ui/                    # User interface
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── header.py         # Header component
│   ├── components/        # Reusable UI components
│   │   ├── __init__.py
│   │   ├── cards.py       # Card components
│   │   └── gantt_chart.py # Gantt chart component
│   └── tabs/              # Tab modules
│       ├── __init__.py
│       ├── input_tab.py      # Input tab
│       ├── results_tab.py    # Results tab
│       ├── gantt_tab.py      # Gantt charts tab
│       └── comparison_tab.py # Comparison tab
├── themes/                # Theme management
│   ├── __init__.py
│   └── theme_manager.py   # Theme styles
└── utils/                 # Utility functions
    ├── __init__.py
    ├── constants.py       # Application constants
    └── pid_utils.py       # Process ID utilities
```

## Architecture Principles

### 1. **Separation of Concerns**
- **Models**: Pure data structures with no business logic
- **Algorithms**: Independent, testable scheduling algorithms
- **Services**: Business logic and data operations
- **UI**: Presentation layer only, delegates to services

### 2. **Single Responsibility**
Each module has a single, well-defined responsibility:
- `ProcessService`: Manages process collection
- `SimulationService`: Orchestrates simulations
- `FileService`: Handles file operations
- Each algorithm class: Implements one scheduling algorithm

### 3. **Dependency Injection**
Services are injected into UI components, making them testable and flexible.

### 4. **Open/Closed Principle**
New algorithms can be added by:
1. Creating a new algorithm class inheriting from `BaseAlgorithm`
2. Adding it to `SchedulingSimulator`
3. No changes needed to existing code

## Module Descriptions

### Models (`models/`)
- **`process.py`**: `Process` dataclass representing a CPU process
  - Contains process attributes (PID, arrival, burst, priority)
  - Includes helper methods: `to_dict()`, `clone()`

### Algorithms (`algorithms/`)
- **`base_algorithm.py`**: Abstract base class for all algorithms
  - Defines `execute()` interface
  - Provides `calculate_results()` helper method
- **`scheduler.py`**: Main coordinator that runs all algorithms
- Individual algorithm modules: Each implements one scheduling algorithm

### Services (`services/`)
- **`process_service.py`**: Manages process collection
  - Add/remove/clear processes
  - Query operations
- **`simulation_service.py`**: Orchestrates simulation execution
  - Runs all or single algorithms
  - Returns formatted results
- **`file_service.py`**: Handles file I/O
  - Load processes from file
  - Save processes to file

### UI (`ui/`)
- **`main_window.py`**: Main application window
  - Coordinates tabs and services
  - Handles application-level events
- **`tabs/`**: Separate tab modules
  - `input_tab.py`: Process input and management
  - `results_tab.py`: Display simulation results
  - `gantt_tab.py`: Display Gantt charts
  - `comparison_tab.py`: Algorithm comparison charts
- **`components/`**: Reusable UI components
  - `cards.py`: Card components
  - `gantt_chart.py`: Gantt chart widget

### Themes (`themes/`)
- **`theme_manager.py`**: Centralized theme management
  - Light/dark theme stylesheets
  - Message box styles
  - Text color utilities

### Utils (`utils/`)
- **`constants.py`**: Application-wide constants
- **`pid_utils.py`**: Process ID utility functions

## Benefits of This Architecture

1. **Maintainability**: Clear structure makes it easy to find and modify code
2. **Testability**: Each module can be tested independently
3. **Extensibility**: Easy to add new algorithms or features
4. **Reusability**: Components can be reused across the application
5. **Readability**: Code is organized logically and easy to understand

## Adding a New Algorithm

1. Create a new file in `algorithms/` (e.g., `srtf.py`)
2. Inherit from `BaseAlgorithm`:
```python
from .base_algorithm import BaseAlgorithm

class SRTFAlgorithm(BaseAlgorithm):
    def execute(self, processes, **kwargs):
        # Implementation
        return self.calculate_results("SRTF", processes, gantt, total_time, total_idle)
```
3. Add to `SchedulingSimulator` in `algorithms/scheduler.py`:
```python
from .srtf import SRTFAlgorithm

class SchedulingSimulator:
    def __init__(self, processes):
        # ...
        self.srtf_algo = SRTFAlgorithm()
    
    def srtf(self):
        return self.srtf_algo.execute(self._clone())
    
    def run_all(self, time_quantum=3):
        return {
            # ...
            "srtf": self.srtf()
        }
```

## Running the Application

```bash
python main.py
```

The application will start with the modular structure, providing a clean, maintainable codebase that follows best practices.


