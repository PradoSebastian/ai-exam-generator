import logging
from typing import Any, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from app.agent.prompt.image_reader_prompt import IMAGE_READER_PROMPT
from app.constants.agent_constants import (
    IMAGE_READER_OUTPUT_FILE_NAME,
    IMAGE_READER_OUTPUT_KEY,
    GEMINI_MODEL
)
from app.util.md import MarkdownUtil

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
            instruction="""
            EXTRA CONTEXT:
            1. INCLUDE_ANSWERS: {include_answers}
            """,
            output_key=IMAGE_READER_OUTPUT_KEY,
            after_agent_callback = self.__class__.save_markdown_after_agent
        )
        

    def get_agent(self) -> LlmAgent:
        return self.image_reader_llm_agent

    @staticmethod
    def save_markdown_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
        generated_markdown = callback_context.state.get(IMAGE_READER_OUTPUT_KEY, "NO MARKDOWN GENERATED")

        if generated_markdown:
            MarkdownUtil.create_markdown_file(text=generated_markdown, file_name=IMAGE_READER_OUTPUT_FILE_NAME)
        
        return None

    
image_reader_agent = ImageReaderAgent()
        