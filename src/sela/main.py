import os

from sela.agents.main_agent import MainAgent
from sela.utils.conf import Conf

if __name__ == "__main__":
    conf = Conf()
    agent = MainAgent()

    response = agent.run("こんにちは．")

    print(response)
