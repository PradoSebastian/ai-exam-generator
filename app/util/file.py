
import os

import google.genai.types as types

class FileUtil:

    @staticmethod
    def read_str_file(path: str) -> str:
        """Reads a file from the specified path and returns its content as a string."""
        with open(path, 'r') as file:
            return file.read()

    @staticmethod
    def read_file(path: str) -> bytes:
        """Reads a file from the specified path and returns its bytes."""
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    def read_files_from_folder(
        folder_path: str, 
        types: list[str]
    ) -> list[tuple[str, bytes]]:
        """Reads files from the specified folder and returns their paths and bytes."""
        result: list[tuple[str, bytes]] = []
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(tuple(types)):
                    full_path = os.path.join(root, filename)
                    result.append((full_path, FileUtil.read_file(str(full_path))))
        return result