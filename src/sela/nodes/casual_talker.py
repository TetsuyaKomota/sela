from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from sela.data.schemas import BaseChatModel, Message
from sela.utils.prompt_manager import get_prompt


class CasualTalker:
    def __init__(self, llm: BaseChatModel, hisoty_len: int = 5):
        self.llm = llm | StrOutputParser()
        self.hisoty_len = hisoty_len

    def format_message_history(self, messages: list[str]) -> str:
        output = []
        for m in messages[-self.hisoty_len :]:
            output.append(f"{m.role}: {m.text}")
        return "\n".join(output)

    def run(self, user_message: str, messages: list[str]) -> list[Message]:
        prompt = get_prompt("casual_talker")

        chain = prompt | self.llm

        params = {
            "user_message": user_message,
            "message_history": self.format_message_history(messages),
        }

        response = chain.invoke(params)

        request_message = Message(role="human", text=user_message)
        response_message = Message(role="assistant", text=response)

        return [request_message, response_message]
