from typing import Callable

from sela.data.schemas import BaseChatModel, ImportantFactor, Messages
from sela.utils.prompt_manager import get_prompt


class MemorySaver:
    def __init__(
        self,
        llm: BaseChatModel,
        long_term_memory: Callable[[str], str],
        save_important_factor_to_memory: Callable[[ImportantFactor], None],
        hisoty_len: int = 10,
    ):
        self.llm = llm.with_structured_output(ImportantFactor)
        self.long_term_memory = long_term_memory
        self.save_important_factor_to_memory = save_important_factor_to_memory
        self.hisoty_len = hisoty_len

    def format_message_history(self, messages: list[str]) -> str:
        output = [str(m) for m in messages[-self.hisoty_len :]]
        return "\n".join(output)

    def run(self, messages: Messages) -> ImportantFactor:
        prompt = get_prompt("memory_saver")

        message_history = self.format_message_history(messages.messages)
        long_term_memory = self.long_term_memory(message_history)
        long_term_memory = long_term_memory.split("---")[
            1
        ].strip()  # TODO ダサいので直す

        chain = prompt | self.llm

        params = {
            "long_term_memory": long_term_memory,
            "message_history": message_history,
        }

        important_factor: ImportantFactor = chain.invoke(params)

        # LongTermMemory に保存
        if "重要な要素なし" not in important_factor.factor:
            self.save_important_factor_to_memory(important_factor)

        return important_factor
