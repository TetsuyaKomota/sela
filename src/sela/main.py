import os

from sela.agents.main_agent import MainAgent
from sela.utils.conf import Conf

if __name__ == "__main__":
    conf = Conf()
    agent = MainAgent()

    response = agent.run("こんにちは")
    print(response.messages.messages[-1].text)
    response = agent.run("調子はどうですか？")
    print(response.messages.messages[-1].text)
    response = agent.run("さようなら")
    print(response.messages.messages[-1].text)
