import logging

from google.adk.agents.invocation_context import InvocationContext
import google.genai.types as types

from app.constants.agent_constants import IMAGE_ARTIFACTS_KEY
from app.util.file import FileUtil

logger = logging.getLogger(__name__)

class ArtifactUtil:
    """Utility class for handling artifacts."""

    @staticmethod
    async def save_part_artifact(
        file_name: str,
        artifact: types.Part,
        ctx_key: str,
        ctx: InvocationContext
    ) -> bool:
        """Saves a bytes artifact to the specified path."""
        if ctx.artifact_service is None:
            logger.error("Artifact service is not available in the context.")
            return False
        await ctx.artifact_service.save_artifact(
            app_name=ctx.session.app_name,
            user_id=ctx.session.user_id,
            filename=file_name, 
            artifact=artifact,
            session_id=ctx.session.id
        )
        ctx.session.state.setdefault(ctx_key, []).append(file_name)
        return True

    @staticmethod
    async def save_artifact(
        file_path: str | bytes,
        mime_type: str,
        ctx_key: str,
        ctx: InvocationContext,
        folder: str | None = None,
        default_name: str | None = None
    ) -> bool:
        """Saves an artifact to the specified path."""
        try:
            if isinstance(file_path, str):
                bytes = FileUtil.read_file(file_path)
                file_name = file_path.split('/')[-1]
            else:
                bytes = file_path
                file_name = default_name or "artifact"
            file_name = f"{folder}_{file_name}" if folder else file_name
            artifact = types.Part.from_bytes(
                data=bytes, 
                mime_type=mime_type
            )
            return await ArtifactUtil.save_part_artifact(file_name, artifact, ctx_key, ctx)
        except Exception as e:
            logger.error(f"Error saving artifact: {e}")
            return False

    @staticmethod
    async def save_artifacts(
        file_paths: list[tuple[str, str]] | list[tuple[bytes, str]],
        ctx_key: str, 
        ctx: InvocationContext,
        folder: str | None = None,
        default_name: str | None = None
    ) -> bool:
        """Saves the artifacts to the session state."""
        counter = 0
        for file_path, mime_type in file_paths:
            default_name = f"{default_name}_{counter}.md" if default_name else None
            if not ArtifactUtil.save_artifact(file_path, mime_type, ctx_key, ctx, folder, default_name):
                logger.error(f"Error saving artifact: {file_path}")
                await ArtifactUtil.clean_artifacts(ctx_key, ctx)
                return False
        return True

    @staticmethod
    async def clean_artifacts(ctx_key: str, ctx: InvocationContext) -> None:
        """Cleans the artifacts from the session state."""
        if ctx.artifact_service is None:
            logger.error("Artifact service is not available in the context.")
            return

        for file_name in ctx.session.state.get(ctx_key, []):
            await ctx.artifact_service.delete_artifact(
                app_name=ctx.session.app_name,
                user_id=ctx.session.user_id,
                filename=file_name,
                session_id=ctx.session.id
            )
        ctx.session.state.pop(ctx_key, None)
