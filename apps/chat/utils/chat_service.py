import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI

from apps.chat.utils.history_message_util import HistoryMessageManager

logging.basicConfig(
    filename="/apps/chat/history.log",  # Log file path
    level=logging.DEBUG,  # Log everything from DEBUG and above
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ChatConfig:
    model_url: str
    model_name: str
    model_api_key: str
    temperature: float = 0.7


class ChatService:
    def __init__(self, config: ChatConfig):
        self.config = config
        self.client = self._create_client()

    def _create_client(self) -> OpenAI:
        """Create and return an OpenAI client instance."""
        try:
            return OpenAI(
                base_url=self.config.model_url,
                api_key=self.config.model_api_key,
            )
        except Exception as e:
            logger.error(f"Failed to create OpenAI client: {e}")
            raise ConnectionError("Could not connect to Ollama")

    def _process_agent_context(self, prompt: str, agent_id: Optional[str]) -> str:
        """Process agent context and add relevant documents to the prompt."""
        if not agent_id:
            return prompt

    def process_chat(
        self,
        prompt: str,
        history_manager: HistoryMessageManager,
        session_id: str,
        user_id: str,
        agent_id: Optional[str] = None
    ) -> str:
        """
        Process a chat message and return the response.

        Args:
            prompt: The user's input message
            messages: The conversation history
            session_id: The current session ID
            user_id: The current user's ID
            agent_id: Optional agent ID for context
            plugins: List of plugin ids
            tools: List of available tools
            active_plugins: Dictionary of active plugins

        Returns:
            str: The model's response
        """

        try:
            messages = []

            history_messages = history_manager.get_history_messages(user_id)

            if history_messages:
                for message in history_messages:
                    messages.append({
                        "role": "user",
                        "content": message["user_message"]
                    })
                    messages.append({
                        "role": "assistant",
                        "content": message["model_message"]
                    })
                logger.info(
                    f"Retrieved {len(history_messages)} historical messages for user {user_id}")

                # Add the current prompt to messages
                messages.append({
                    "role": "user",
                    "content": prompt
                })

            else:
                prompt = self._process_agent_context(prompt, agent_id)
                messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                tool_choice="auto",
                temperature=self.config.temperature,
            )
            response_message = response.choices[0].message

            messages.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response_message.content}
            ])
            result = str(response_message.content)

            self._store_history(session_id, prompt, result, user_id)
            return result

        except Exception as e:
            logger.error(f"Error processing chat: {e}")
            return f"Error: Could not get response from model - {str(e)}"

        finally:
            self._cleanup()

    def _store_history(self, session_id: str, prompt: str, response: str, user_id: str) -> None:
        """Store the conversation history in the database."""
        try:
            if response is None or prompt is None:
                logger.error(
                    "Response or prompt is None. Skipping history storage.")
                return False
            new_interaction = HistoryMessageManager(
                user_id=user_id,
                session_id=session_id,
                user_message=prompt,
                model_message=response,
                creator_id=user_id,
                last_modifier_id=user_id
            )
            new_interaction.save()
            return response
        except Exception as e:
            logger.error(f"Failed to store conversation history: {e}")
            raise

    def _cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Failed to close client: {e}")
