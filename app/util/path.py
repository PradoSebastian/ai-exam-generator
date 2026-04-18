
from pathlib import Path

class PathUtil:
    """Utility class for handling file paths."""
    
    @staticmethod
    def get_full_path(path: str) -> str:
        """Returns the full path to a file or directory."""
        BASE_DIR = Path(__file__).resolve().parent
        return str(BASE_DIR.parent / path)