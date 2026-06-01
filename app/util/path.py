import logging
import os
from pathlib import Path

from app.constants.agent_constants import FILES_PATH

logger = logging.getLogger(__name__)
class PathUtil:
    """Utility class for handling file paths."""
    
    @staticmethod
    def get_full_path(path: str) -> str:
        """Returns the full path to a file or directory."""
        BASE_DIR = Path(__file__).resolve().parent
        return str(BASE_DIR.parent / path).replace('\\', '/')

    @staticmethod
    def read_files_tree_from_folder(
        folder_path: str, 
        types: list[str]
    ) -> dict[str, dict[str, list[str]]]:
        """Reads files from the specified folder and returns a dictionary of files per folder."""
        files_per_folder: dict[str, dict[str, list[str]]] = {}
        for root, dirs, files in os.walk(PathUtil.get_full_path(folder_path)):
            for filename in files:
                type = filename.split('.')[-1]
                normalized_root = root.replace('\\', '/').split(FILES_PATH)[-1]
                if type in types:
                    split = normalized_root.split('/')
                    if len(split) > 1:
                        folder = split[-1]
                    else:
                        folder = ''
                    full_path = os.path.join(root, filename)
                    files_per_folder.setdefault(
                        folder, {}
                    ).setdefault(type, []).append(full_path.replace('\\', '/'))
            
        return files_per_folder