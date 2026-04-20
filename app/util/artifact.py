import logging

from google.adk.agents.invocation_context import InvocationContext
import google.genai.types as types

from app.constants.agent_constants import IMAGE_ARTIFACTS_KEY

logger = logging.getLogger(__name__)

class ArtifactUtil:
    """Utility class for handling artifacts."""

    @staticmethod
    def save_artifact(file_path: str, mime_type: str, ctx: InvocationContext) -> bool:
        """Saves an artifact to the specified path."""
        try:
            with open(file_path, 'rb') as f:
                file_name = file_path.split('/')[-1]
                artifact = types.Part.from_bytes(
                    data=f.read(), 
                    mime_type=mime_type
                )
                ctx.artifact_service.save_artifact(filename=file_name, artifact=artifact)
                ctx.session.state.setdefault(IMAGE_ARTIFACTS_KEY, []).append(file_name)
        except Exception as e:
            logger.error(f"Error saving artifact: {e}")
            return False
        return True

    @staticmethod
    def save_artifacts(file_paths: list[tuple[str, str]], ctx: InvocationContext) -> bool:
        """Saves the artifacts to the session state."""
        for file_path, mime_type in file_paths:
            if not ArtifactUtil.save_artifact(file_path, mime_type, ctx):
                logger.error(f"Error saving artifact: {file_path}")
                ArtifactUtil.clean_artifacts(ctx)
                return False
        return True

    @staticmethod
    def clean_artifacts(ctx: InvocationContext) -> None:
        """Cleans the artifacts from the session state."""
        for file_name in ctx.session.state.get(IMAGE_ARTIFACTS_KEY, []):
            ctx.artifact_service.delete_artifact(filename=file_name)
        ctx.session.state.pop(IMAGE_ARTIFACTS_KEY, None)
