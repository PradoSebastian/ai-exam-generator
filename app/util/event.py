from google.adk.events import Event
import google.genai.types as types

class EventUtil:
    """Utility class for handling events."""

    @staticmethod
    def create_error_event(message: str) -> Event:
        return Event(
            author="system",
            content=types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
        )