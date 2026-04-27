import logging
from typing import Any, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types

from app.agent.prompt.exam_generator_prompt import EXAM_GENERATOR_PROMPT
from app.constants.agent_constants import (
    CSV_CUSTOM_CHARACTERS_FILE_PATH,
    CSV_SPECIAL_CONSIDERATIONS_FILE_PATH,
    CUSTOM_CHARACTERS_KEY,
    EXAM_GENERATOR_OUTPUT_FILE_NAME,
    EXAM_GENERATOR_OUTPUT_KEY,
    GEMINI_MODEL,
    GENERATED_DEFAULT_FILE_NAME,
    GENERATED_FOLDER,
    MARKDOWN_ARTIFACTS_KEY,
    SPECIAL_CONSIDERATIONS_KEY
)
from app.util.artifact import ArtifactUtil
from app.util.csv import CSVUtil
from app.util.event import EventUtil
from app.util.md import MarkdownUtil

logger = logging.getLogger(__name__)

class ExamGeneratorAgent:

    exam_generator_llm_agent: LlmAgent

    def __init__(self):
        self.exam_generator_llm_agent = LlmAgent(
            model=GEMINI_MODEL,
            name="exam_generator_agent",
            description="Generates exams in markdown based on the provided markdown content.",
            static_instruction=types.Content(
                role="user", parts=[types.Part(text=EXAM_GENERATOR_PROMPT)]
            ),
            instruction=f"""
            EXTRA CONTEXT:
            1. MARKDOWN ARTIFACT NAMES: {{{MARKDOWN_ARTIFACTS_KEY}}}
            2. CUSTOM CHARACTER REFERENCES: {{{CUSTOM_CHARACTERS_KEY}?}}
            3. SPECIAL CONSIDERATIONS: {{{SPECIAL_CONSIDERATIONS_KEY}?}}
            """,
            output_key=EXAM_GENERATOR_OUTPUT_KEY,
            after_agent_callback = self.__class__.save_markdown_after_agent
        )

    @staticmethod
    def save_markdown_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
        generated_markdown = callback_context.state.get(EXAM_GENERATOR_OUTPUT_KEY, "NO MARKDOWN GENERATED")

        if generated_markdown:
            MarkdownUtil.create_markdown_file(text=generated_markdown, file_name=EXAM_GENERATOR_OUTPUT_FILE_NAME)
        
        return None

    async def _initialize_image_files(
        self, 
        markdown_files: list[tuple[str, str]],
        markdown_results: list[str],
        ctx: InvocationContext
    ) -> Event | None:
        """Initializes the image files.""" 
        if not markdown_files or not markdown_results:
             logger.error(f"No markdown files found or no markdown results generated")
             return EventUtil.create_error_event(f"No markdown files found or no markdown results generated")
        
        if not await ArtifactUtil.save_artifacts(markdown_files, MARKDOWN_ARTIFACTS_KEY, ctx):
            logger.error(f"Error saving artifacts: {markdown_files}")
            return EventUtil.create_error_event(f"Error saving artifacts: {markdown_files}")
        
        bytes_list = [(result.encode('utf-8'), MarkdownUtil.MIME_TYPE) for result in markdown_results]
        
        if not await ArtifactUtil.save_artifacts(
            bytes_list, 
            MARKDOWN_ARTIFACTS_KEY, 
            ctx, 
            GENERATED_FOLDER, 
            GENERATED_DEFAULT_FILE_NAME):
            logger.error(f"Error saving generated artifacts.")
            return EventUtil.create_error_event(f"Error saving generated artifacts.")

        custom_characters = CSVUtil.read_two_column(CSV_CUSTOM_CHARACTERS_FILE_PATH)
        special_considerations = CSVUtil.read_two_column(CSV_SPECIAL_CONSIDERATIONS_FILE_PATH)
        if custom_characters:
            logger.info(f"Custom characters read successfully: {custom_characters}")
            ctx.session.state[CUSTOM_CHARACTERS_KEY] = custom_characters
        if special_considerations:
            logger.info(f"Special considerations read successfully: {special_considerations}")
            ctx.session.state[SPECIAL_CONSIDERATIONS_KEY] = special_considerations

    async def _clean_image_artifacts(self, ctx: InvocationContext) -> None:
        ctx.session.state.pop(CUSTOM_CHARACTERS_KEY, None)
        ctx.session.state.pop(SPECIAL_CONSIDERATIONS_KEY, None)
        await ArtifactUtil.clean_artifacts(MARKDOWN_ARTIFACTS_KEY, ctx)

    def get_agent(self) -> LlmAgent:
        return self.exam_generator_llm_agent

    
exam_generator_agent = ExamGeneratorAgent()
        