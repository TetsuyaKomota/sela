from langchain_openai import ChatOpenAI

from sela.data.schemas import BaseChatModel, ExecutionMode, Message
from sela.utils.prompt_manager import get_prompt


class ModeSelector:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm.with_structured_output(ExecutionMode)

    def run(self, user_message: Message) -> ExecutionMode:
        prompt = get_prompt("mode_selector")

        chain = prompt | self.llm

        params = {"user_message": user_message}

        return chain.invoke(params)
