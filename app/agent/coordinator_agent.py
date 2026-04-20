import logging
from typing import AsyncGenerator

from google.adk.agents.base_agent import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext

from app.agent.exam_generator_agent import ExamGeneratorAgent
from app.agent.image_reader_agent import ImageReaderAgent
from app.constants.agent_constants import (
    FILES_PATH,
    IMAGE_READER_OUTPUT_KEY, 
)
from app.util.path import PathUtil
from app.util.image import ImageUtil
from app.util.md import MarkdownUtil
from app.util.artifact import ArtifactUtil
from app.util.event import EventUtil

logger = logging.getLogger(__name__)

class CoordinatorAgent(BaseAgent):

    image_reader_agent: ImageReaderAgent
    exam_generator_agent: ExamGeneratorAgent

    def __init__(
        self, 
        image_reader_agent: ImageReaderAgent, 
        exam_generator_agent: ExamGeneratorAgent
    ):
        self.image_reader_agent = image_reader_agent
        self.exam_generator_agent = exam_generator_agent

    def _filter_image_files(
        self,
        files_tree: dict[str, dict[str, list[str]]]
    ) -> dict[str, list[tuple[str, str]]]:
        """Executes the image reading process."""
        images_per_folder: dict[str, list[tuple[str, str]]] = {}
        for folder, tree in files_tree.items():
            image_files: list[tuple[str, str]] = []
            for type, files in tree.items():
                if type in ImageUtil.IMAGE_EXTENSIONS:
                    image_files.extend([
                        (file, ImageUtil.get_mime_type(file)) for file in files
                    ])
            images_per_folder[folder] = image_files

        return images_per_folder

    def _filter_markdown_files(
        self,
        files_tree: dict[str, dict[str, list[str]]]
    ) -> list[tuple[str, str]]:
        """Executes the image reading process."""
        markdown_files: list[tuple[str, str]] = []
        for tree in files_tree.values():
            for type, files in tree.items():
                if type == MarkdownUtil.EXTENSION:
                    markdown_files.extend([
                        (file, MarkdownUtil.MIME_TYPE) for file in files
                    ])

        return markdown_files

    async def run_async(
      self,
      ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None] | None:

        files_tree = PathUtil.read_files_tree_from_folder(
            folder_path=FILES_PATH, 
            types=ImageUtil.IMAGE_EXTENSIONS + [MarkdownUtil.EXTENSION]
        )

        # Step 1: Execute image reading agent per existingfolder

        generated_markdown_files: list[str] = []
        # Filter image files per folder
        images_per_folder = self._filter_image_files(files_tree)
        for folder, image_files in images_per_folder.items():
            # Initialize image files
            error_event = self.image_reader_agent._initialize_image_files(folder, image_files, ctx)
            if error_event:
                yield error_event
                return

            # Execute image reading agent
            async for event in self.image_reader_agent.get_agent().run_async(ctx):
                yield event

            # Save generated markdown
            generated_markdown_files.append(ctx.session.state.get(IMAGE_READER_OUTPUT_KEY))
            # Clean image files
            self.image_reader_agent._clean_image_files(ctx)

        # Step 2: Execute exam generator agent

        # Filter markdown files
        markdown_files = self._filter_markdown_files(files_tree)
        
            
        return