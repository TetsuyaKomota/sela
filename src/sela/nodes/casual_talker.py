from typing import Callable

from langchain_core.output_parsers import StrOutputParser

from sela.data.schemas import BaseChatModel, Message, Messages
from sela.utils.datetime_manager import get_dt
from sela.utils.prompt_manager import get_prompt


class CasualTalker:
    def __init__(
        self,
        llm: BaseChatModel,
        long_term_memory: Callable[[str], str],
        hisoty_len: int = 10,
    ):
        config = {"temperature": 0.7}
        self.llm = llm.with_config(configurable=config) | StrOutputParser()
        self.long_term_memory = long_term_memory
        self.hisoty_len = hisoty_len

    def format_message_history(self, messages: Messages) -> str:
        output = [str(m) for m in messages.messages[-self.hisoty_len :]]
        return "\n".join(output)

    def run(self, user_message: Message, messages: Messages) -> Messages:
        prompt = get_prompt("casual_talker")

        chain = prompt | self.llm

        params = {
            "long_term_memory": self.long_term_memory(user_message.text),
            "message_history": self.format_message_history(messages),
            "user_message": user_message,
            "assistant_dt": get_dt(),
        }

        response = chain.invoke(params)

        response_message = Message(role="assistant", text=response)

        return Messages(messages=[user_message, response_message])
