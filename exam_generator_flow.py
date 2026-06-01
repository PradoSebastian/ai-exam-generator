import asyncio
import logging

import google.genai.types as types

from app.agent.config.runner import AgentRunner
from app.agent.coordinator_agent import CoordinatorAgent
from app.agent.exam_generator_agent import ExamGeneratorAgent
from app.agent.image_reader_agent import ImageReaderAgent
from app.constants.agent_constants import USER_ID

logger = logging.getLogger(__name__)

async def main():
    logger.info("El programa ha iniciado correctamente.")
    
    image_reader_agent = ImageReaderAgent()
    exam_generator_agent = ExamGeneratorAgent()

    coordinator_agent = CoordinatorAgent(
        image_reader_agent=image_reader_agent,
        exam_generator_agent=exam_generator_agent
    )

    runner = AgentRunner(coordinator_agent)

    session = await runner.create_session()

    content = types.Content(role='user', parts=[types.Part(text="Read the images stored as artifacts to complete your flows.")])
    
    async for event in runner.get_runner().run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=content
    ):

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text 
                logger.info(f"Final response received from agent from {event.author}")
        else:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_call:
                        logger.info(f"Function call: '{part.function_call}' from {event.author}")
                    elif part.function_response:
                        logger.info(f"Function response: '{part.function_response}' from {event.author}")
                

    logger.info("El programa ha finalizado correctamente.")

if __name__ == "__main__":
    asyncio.run(main())
