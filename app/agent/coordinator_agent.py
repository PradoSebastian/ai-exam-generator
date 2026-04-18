from typing import AsyncGenerator

from google.adk.agents.base_agent import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext

from app.agent.exam_generator_agent import ExamGeneratorAgent
from app.agent.image_reader_agent import ImageReaderAgent
from app.constants.agent_constants import IMAGE_READER_OUTPUT_KEY

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


    async def run_async(
      self,
      ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None] | None:
        
        async for event in self.image_reader_agent.get_agent().run_async(ctx):
            yield event

        markdown_from_images = ctx.session.state.get(IMAGE_READER_OUTPUT_KEY)
        
        if markdown_from_images:
            # Here you can add any additional processing or logic that you want to perform with the generated markdown.
            # For example, you could trigger another agent, save the markdown to a database, etc.
            pass
            
        return None