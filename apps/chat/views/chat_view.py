from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.chat.serializers.chat_serializer import ChatSerializer
from apps.chat.utils.chat_service import ChatConfig, ChatService
from apps.chat.utils.history_message_util import HistoryMessageManager
from config.settings import GOOGLE_API_KEY, GOOGLE_URL


class ChatView(GenericAPIView):
    serializer_class = ChatSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        user_id = request.user.id
        if not user_id:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user_message = serializer.validated_data["user_message"]
        session_id = serializer.validated_data["session_id"]

        try:
            config = ChatConfig(model_url=GOOGLE_URL,
                                model_api_key=GOOGLE_API_KEY,
                                model_name="gemini-1.5-flash")

            chat_service = ChatService(config=config)
            history_manager = HistoryMessageManager(session_id=session_id)

            response = chat_service.process_chat(
                prompt=user_message,
                history_manager=history_manager,
                session_id=session_id,
                user_id=user_id,
            )
            return Response({"response": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error process chat": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
