"""File I/O Service"""
from typing import List
from models.process import Process


class FileService:
    """Handles file operations for processes"""
    
    @staticmethod
    def load_from_file(filepath: str) -> List[Process]:
        """
        Load processes from a file
        
        Expected format: pid,arrival_time,burst_time,priority
        Lines starting with # are ignored
        """
        processes = []
        try:
            with open(filepath, 'r') as f:
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
        except Exception as e:
            raise ValueError(f"Failed to load file: {str(e)}")
        
        return processes
    
    @staticmethod
    def save_to_file(filepath: str, processes: List[Process]) -> None:
        """Save processes to a file"""
        try:
            with open(filepath, 'w') as f:
                for proc in processes:
                    f.write(f"{proc.pid},{proc.arrival_time},{proc.burst_time},{proc.priority}\n")
        except Exception as e:
            raise ValueError(f"Failed to save file: {str(e)}")


