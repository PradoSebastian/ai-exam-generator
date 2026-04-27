import logging
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types

from app.agent.prompt.image_reader_prompt import IMAGE_READER_PROMPT
from app.constants.agent_constants import (
    INCLUDE_ANSWERS_KEY,
    IMAGE_ARTIFACTS_KEY,
    IMAGE_READER_OUTPUT_FILE_NAME,
    IMAGE_READER_OUTPUT_KEY,
    IMAGE_REFERENCES_KEY,
    GEMINI_MODEL
)
from app.util.md import MarkdownUtil
from app.util.artifact import ArtifactUtil
from app.util.event import EventUtil

logger = logging.getLogger(__name__)

class ImageReaderAgent:

    image_reader_llm_agent: LlmAgent

    def __init__(self):
        self.image_reader_llm_agent = LlmAgent(
            model=GEMINI_MODEL,
            name="image_reader_agent",
            description="Reads and transform images into a markdown structure based on the part images (already ordered) content.",
            static_instruction=types.Content(
                role="user", parts=[types.Part(text=IMAGE_READER_PROMPT)]
            ),
            instruction=f"""
            EXTRA CONTEXT:
            1. IMAGE ARTIFACT NAMES: {{{IMAGE_ARTIFACTS_KEY}}}
            2. IMAGE REFERENCES: {{{IMAGE_REFERENCES_KEY}?}}
            3. INCLUDE_ANSWERS: {{{INCLUDE_ANSWERS_KEY}}}
            """,
            output_key=IMAGE_READER_OUTPUT_KEY,
            after_agent_callback = self.__class__.save_markdown_after_agent
        )

    @staticmethod
    def save_markdown_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
        generated_markdown = callback_context.state.get(IMAGE_READER_OUTPUT_KEY, "NO MARKDOWN GENERATED")
        file_name = callback_context.state.get(IMAGE_READER_OUTPUT_FILE_NAME)

        if generated_markdown:
            MarkdownUtil.create_markdown_file(text=generated_markdown, file_name=file_name)
        
        return None

    async def _initialize_image_files(
        self, 
        folder: str, 
        image_files: list[tuple[str, str]],
        ctx: InvocationContext
    ) -> Event | None:
        """Initializes the image files."""
        if not image_files:
            logger.error(f"No image files found in {folder}")
            return EventUtil.create_error_event(f"No image files found in {folder}")

        if not await ArtifactUtil.save_artifacts(image_files, IMAGE_ARTIFACTS_KEY, ctx):
            logger.error(f"Error saving artifacts: {image_files}")
            return EventUtil.create_error_event(f"Error saving artifacts: {image_files}")
        
        ctx.session.state[IMAGE_READER_OUTPUT_FILE_NAME] = f"{folder}_{IMAGE_READER_OUTPUT_FILE_NAME}" if folder else IMAGE_READER_OUTPUT_FILE_NAME
        
    async def _clean_image_artifacts(self, ctx: InvocationContext) -> None:
        ctx.session.state.pop(IMAGE_READER_OUTPUT_FILE_NAME, None)
        await ArtifactUtil.clean_artifacts(IMAGE_ARTIFACTS_KEY, ctx)

    def get_agent(self) -> LlmAgent:
        return self.image_reader_llm_agent

    
image_reader_agent = ImageReaderAgent()
        