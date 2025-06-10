import logging
from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.agents import Agent

logger = logging.getLogger(__name__)


class AdkAdapter:
    def __init__(self, agent_instance: Agent, adk_app_name: str):
        """
        Initializes the AdkAdapter.
        Args:
            agent_instance: An instance of google.adk.agents.Agent.
            adk_app_name: The application name for ADK.
        """
        self.session_service = InMemorySessionService()
        self.artifacts_service = InMemoryArtifactService()
        self.app_name = adk_app_name
        self.root_agent = agent_instance

    async def query_agent_stream(
        self, message_text: str, user_id: str, session_id_suffix: str
    ):
        """
        Queries the ADK agent and yields response parts as a stream.
        Manages session creation or retrieval.
        """
        try:
            session_id = f"slack_{user_id}_{session_id_suffix}"
            session = self.session_service.get_session(
                app_name=self.app_name, user_id=user_id, session_id=session_id
            )
            if not session:
                session = self.session_service.create_session(
                    state={},
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id,
                )

            if not self.root_agent:
                logger.error("ADK Agent instance is not set in AdkAdapter.")
                yield "エラー: ADKエージェントが設定されていません。"
                return

            runner = Runner(
                app_name=self.app_name,
                agent=self.root_agent,
                artifact_service=self.artifacts_service,
                session_service=self.session_service,
            )

            query_content = Content(role="user", parts=[Part(text=message_text)])
            logger.info(
                f"Querying ADK agent with: '{message_text}' for session: {session.id}"
            )

            events_async = runner.run_async(
                session_id=session.id,
                user_id=session.user_id,
                new_message=query_content,
            )

            async for event in events_async:
                if (
                    event
                    and event.content
                    and event.content.role == "model"
                    and event.content.parts
                ):
                    if any(part.text is not None for part in event.content.parts):
                        for part in event.content.parts:
                            if part.text and part.text.strip():
                                yield part.text
        except Exception as e:
            logger.error(f"Error querying ADK agent: {e}")
            yield f"ADKエージェントの処理中にエラーが発生しました: {str(e)}"
