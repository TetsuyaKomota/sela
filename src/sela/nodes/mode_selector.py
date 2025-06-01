from typing import Callable

from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from sela.data.schemas import BaseChatModel, ExecutionMode, Message
from sela.utils.prompt_manager import get_prompt


class ModeSelector:
    def __init__(self, llm: BaseChatModel, long_term_memory: Callable[[str], str]):
        self.llm = llm.with_structured_output(ExecutionMode)
        self.long_term_memory = long_term_memory

    def run(self, user_message: Message) -> ExecutionMode:
        prompt = get_prompt("mode_selector")

        chain = (
            {
                "long_term_memory": self.long_term_memory,
                "user_message": RunnablePassthrough(),
            }
            | prompt
            | self.llm
        )

        params = {"user_message": user_message}

        return chain.invoke(params)
