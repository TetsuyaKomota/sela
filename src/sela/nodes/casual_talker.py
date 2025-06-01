from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from sela.data.schemas import BaseChatModel
from sela.utils.prompt_manager import get_prompt


class CasualTalker:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm | StrOutputParser()

    def run(self, user_message: str) -> str:
        prompt = get_prompt("casual_talker")

        chain = prompt | self.llm

        params = {"user_message": user_message}

        return chain.invoke(params)
