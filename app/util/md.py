import logging
from datetime import date

from app.constants.agent_constants import RESULTS_PATH
from app.util.path import PathUtil

class MarkdownUtil:

    EXTENSION = 'md'
    MIME_TYPE = 'text/markdown'

    @staticmethod
    def create_markdown_file(text: str, file_name: str = "output") -> None:
        """Creates a markdown file with the specified content."""
        with open(
            PathUtil.get_full_path(RESULTS_PATH) + f"/{file_name}-{date.today()}.{MarkdownUtil.EXTENSION}", "w", encoding="utf-8"
        ) as file:
            file.write(text)
            
        logging.info("Generated markdown saved successfully.")