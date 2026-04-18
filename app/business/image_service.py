import logging

import google.genai.types as types

from app.agent.config.runner import AgentRunner
from app.agent.image_reader_agent import ImageReaderAgent, image_reader_agent
from app.constants.agent_constants import FILES_PATH, USER_ID
from app.util.image import ImageUtil
from app.util.md import MarkdownUtil
from app.util.path import PathUtil

logger = logging.getLogger(__name__)

class ImageService:
    """Service for handling image-related operations."""

    image_parts: list[types.Part] = []
    runner: AgentRunner

    def __init__(self, image_reader_agent: ImageReaderAgent):
        self.runner = AgentRunner(image_reader_agent.get_agent())
        self._initialize_image_contents(PathUtil.get_full_path(FILES_PATH))

    def _initialize_image_contents(self, path: str):
        """Initializes the image contents."""
        # This method can be used to set up any necessary data structures or state related to image handling.
        self.image_parts = [part for name, part in ImageUtil.read_images_from_folder(path)]
        logger.info(f"Initialized image contents with {len(self.image_parts)} images from {path}.")

    async def trigger_image_processing_runner(self):
        """Triggers the image processing and returns the image parts."""
        # This method can be called to trigger any processing related to the images, such as preparing them for the agent.
        session = await self.runner.create_session()

        content = types.Content(role='user', parts=self.image_parts)

        final_response_md = "Agent did not produce a final response." # Default

        logger.info("Triggering image processing with the agent.")

        async for event in self.runner.get_runner().run_async(user_id=USER_ID, session_id=session.id, new_message=content):
           if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text 
                    logger.info(f"Final response received from agent: {final_response_text}")    
                break 

        if final_response_text:
            MarkdownUtil.create_markdown_file(text=final_response_text)
        else:
            logger.warning("No final response received from the agent.")

image_service = ImageService(image_reader_agent)