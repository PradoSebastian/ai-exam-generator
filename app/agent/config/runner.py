import logging
import uuid

from google.adk.sessions.base_session_service import BaseSessionService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents.llm_agent import LlmAgent

from app.constants.agent_constants import APP_NAME, CONTEXT_CACHE_CONFIG, USER_ID, INCLUDE_ANSWERS_KEY, INCLUDE_ANSWERS
from app.agent.image_reader_agent import image_reader_agent

logger = logging.getLogger(__name__)

class AgentRunner:
    """Class responsible for running the agents."""

    session_service: BaseSessionService
    runner: Runner

    def __init__(self, root_agent: LlmAgent):
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=root_agent, # The agent we want to run
            app_name=APP_NAME,   # Associates runs with our app
            session_service=self.session_service, # Uses our session manager
            # context_cache_config = CONTEXT_CACHE_CONFIG # You can configure context caching if needed, set as app
        )

    async def create_session(self):
        """Creates a new session."""
        session_id = str(uuid.uuid4())
        state = {
            INCLUDE_ANSWERS_KEY: INCLUDE_ANSWERS
        } # You can add any initial state you want to pass to the agent here
        session = await self.session_service.create_session(
            app_name = APP_NAME,
            user_id = USER_ID,
            session_id = session_id,
            state=state
        )
        logger.info(f"Session created with ID: {session_id}")
        return session
    
    def get_runner(self) -> Runner:
        """Returns the runner instance."""
        return self.runner
    
#runner = AgentRunner(image_reader_agent.get_agent())