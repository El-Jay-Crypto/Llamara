# Placeholder for chat memory
from langchain_community.chat_message_histories import ChatMessageHistory
class ConversationManager:
   def __init__(self):
     self.chat_history = ChatMessageHistory()

   def add_message(self, role, content):
     if role == "user":
       self.chat_history.add_user_message(content)
     elif role == "assistant":
        self.chat_history.add_ai_message(content)
     else:
        print(f"Role {role} is not a valid role, must be either 'user' or 'assistant'")

   def get_history(self):
      history = self.chat_history.messages
      return history

   def clear_history(self):
        self.chat_history.clear()