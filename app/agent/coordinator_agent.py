import logging
from typing import AsyncGenerator

from google.adk.agents.base_agent import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext

from app.agent.exam_generator_agent import ExamGeneratorAgent
from app.agent.image_reader_agent import ImageReaderAgent
from app.constants.agent_constants import (
    AVOID_IMAGE_READING,
    CSV_IMAGE_FILE_PATH,
    FILES_PATH,
    IMAGE_ARTIFACTS_KEY,
    IMAGE_READER_OUTPUT_KEY,
    IMAGE_REFERENCES_KEY,
)
from app.util.csv import CSVUtil
from app.util.image import ImageUtil
from app.util.md import MarkdownUtil
from app.util.path import PathUtil

logger = logging.getLogger(__name__)

class CoordinatorAgent(BaseAgent):

    name: str = "coordinator_agent"
    image_reader_agent: ImageReaderAgent
    exam_generator_agent: ExamGeneratorAgent

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
            if image_files:
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
        
        # Step 0: Read files tree from input folder
        files_tree = PathUtil.read_files_tree_from_folder(
            folder_path=FILES_PATH, 
            types=ImageUtil.IMAGE_EXTENSIONS + [MarkdownUtil.EXTENSION]
        )
        image_references = CSVUtil.read_two_column(CSV_IMAGE_FILE_PATH)
        if image_references:
            ctx.session.state[IMAGE_REFERENCES_KEY] = image_references

        # Step 1: Execute image reading agent per existingfolderz``

        generated_markdown_files: list[str] = []
        # Filter image files per folder
        if not AVOID_IMAGE_READING:
            images_per_folder = self._filter_image_files(files_tree)
            for folder, image_files in images_per_folder.items():
                # Initialize image files
                error_event = await self.image_reader_agent._initialize_image_files(folder, image_files, ctx)
                if error_event:
                    yield error_event
                    return
                
                logger.info(f"Image reading agent execution started for folder {folder}")
                # Execute image reading agent
                async for event in self.image_reader_agent.get_agent().run_async(ctx):
                    yield event
            
                logger.info(f"Image reading agent executed successfully for folder {folder}")

                # Save generated markdown
                generated_markdown_files.append(str(ctx.session.state.get(IMAGE_READER_OUTPUT_KEY)))
                # Clean image files
                await self.image_reader_agent._clean_image_artifacts(ctx)

        # Step 2: Execute exam generator agent

        # Filter markdown files
        markdown_files = self._filter_markdown_files(files_tree)
        error_event = await self.exam_generator_agent._initialize_image_files(markdown_files, generated_markdown_files, ctx)
        if error_event:
            yield error_event

        # Execute image reading agent
        async for event in self.exam_generator_agent.get_agent().run_async(ctx):
            yield event

        await self.exam_generator_agent._clean_image_artifacts(ctx)