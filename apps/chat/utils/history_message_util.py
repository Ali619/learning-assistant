import logging
from typing import Dict, List, Optional

from django.db import transaction

from apps.chat.models import HistoryMessage

logger = logging.getLogger(__name__)


class HistoryMessageManager:
    def __init__(self,
                 session_id: str,
                 user_message: str = None,
                 model_message: str = None,
                 user_id: str = None,
                 creator_id: str = None,
                 last_modifier_id: str = None):
        self.session_id = session_id
        self.user_message = user_message
        self.model_message = model_message
        self.user_id = user_id
        self.creator_id = creator_id
        self.last_modifier_id = last_modifier_id
        self.created_at: Optional[str] = None
        self.updated_at: Optional[str] = None
        self.disable_at: Optional[str] = None
        self.history_messages: List[Dict] = []

    def save(self) -> bool:
        try:
            with transaction.atomic():
                history_message = HistoryMessage(
                    session_id=self.session_id,
                    user_message=self.user_message,
                    model_message=self.model_message,
                    user_id=self.user_id,
                    creator_id=self.creator_id,
                    last_modifier_id=self.last_modifier_id,
                )
                history_message.save()
                logger.info(
                    f"Successfully saved history message for session {self.session_id}")
                return True
        except Exception as e:
            logger.error(
                f"Error saving history message for session {self.session_id}: {str(e)}", exc_info=True)
            return False

    def get_history_messages(self, user_id: str) -> List[Dict]:
        """
        Retrieve history messages for a given user_id and session_id, store them in class attributes,
        and return the list of messages.

        Args:
            user_id (str): The user ID to filter messages

        Returns:
            List[Dict]: List of history messages
        """
        try:
            # Get messages from database
            messages = HistoryMessage.objects.filter(
                user_id=user_id,
                session_id=self.session_id
            ).order_by("created_at").values(
                "session_id",
                "user_message",
                "model_message",
                "user_id",
                "creator_id",
                "last_modifier_id",
                "created_at",
                "updated_at",
                "disable_at"
            )

            # Convert queryset to list
            self.history_messages = list(messages)

            # Update instance attributes with the latest message if available
            if self.history_messages:
                latest_message = self.history_messages[-1]
                self.user_message = latest_message["user_message"]
                self.model_message = latest_message["model_message"]
                self.user_id = latest_message["user_id"]
                self.creator_id = latest_message["creator_id"]
                self.last_modifier_id = latest_message["last_modifier_id"]
                self.created_at = latest_message["created_at"]
                self.updated_at = latest_message["updated_at"]
                self.disable_at = latest_message["disable_at"]

            logger.info(
                f"Successfully retrieved {len(self.history_messages)} messages for user {user_id}, session {self.session_id}")
            return self.history_messages

        except Exception as e:
            logger.error(
                f"Error retrieving history messages for user {user_id}, session {self.session_id}: {str(e)}",
                exc_info=True
            )
            return []
