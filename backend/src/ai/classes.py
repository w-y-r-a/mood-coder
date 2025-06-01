from typing import List, Literal, Dict

Role = Literal["system", "user", "assistant"]

class ConversationManager:
    def __init__(self, system_prompt: str = None, user_id: str = None, chat_id: str = None):
        self.user_id = user_id
        self.chat_id = chat_id
        self.messages: List[Dict[str, str]] = []

        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add(self, role: Role, content: str):
        self.messages.append({"role": role, "content": content})

    def user(self, content: str):
        self.add("user", content)

    def assistant(self, content: str):
        self.add("assistant", content)

    def system(self, content: str):
        self.add("system", content)

    def get_context(self) -> List[Dict[str, str]]:
        return self.messages

    def trim_context(self, max_tokens: int):
        # Token-based context trimming if needed
        pass

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "chat_id": self.chat_id,
            "messages": self.messages,
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj.user_id = data.get("user_id")
        obj.chat_id = data.get("chat_id")
        obj.messages = data.get("messages", [])
        return obj
