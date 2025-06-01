from os.path import abspath, dirname, join

from langchain_core.prompts import ChatPromptTemplate


def get_prompt(prompt_name: str) -> list[tuple[str, str]]:
    dir_path = dirname(abspath(__file__))
    base_path = join(dirname(dir_path), "prompts")

    system_prompt_path = join(base_path, prompt_name, "system.txt")
    human_prompt_path = join(base_path, prompt_name, "human.txt")

    with open(system_prompt_path, "rt", encoding="utf-8_sig") as f:
        system_prompt = f.read().strip()

    with open(human_prompt_path, "rt", encoding="utf-8_sig") as f:
        human_prompt = f.read().strip()

    prompt = [
        ("system", system_prompt),
        ("human", human_prompt),
    ]

    return ChatPromptTemplate.from_messages(prompt)
