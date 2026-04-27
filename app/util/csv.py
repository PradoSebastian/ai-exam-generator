import csv
import logging

import google.genai.types as types

from app.util.file import FileUtil

logger = logging.getLogger(__name__)

class CSVUtil:
    
    @staticmethod
    def read_two_column(file_path: str) -> dict[str, str]:
        """Reads the image references from the CSV file."""
        results = {}
        try:
            bytes = FileUtil.read_file(file_path)
            reader = csv.reader(bytes.decode('utf-8').splitlines())
            for row in reader:
                if len(row) >= 2:
                    name, content = row[0], row[1]
                    results[name] = content
                else:
                    logger.warning(f"Skipping invalid row in CSV: {row}")
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
        return results
