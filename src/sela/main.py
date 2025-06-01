import os

from agents.main_agent import MainAgent
from utils.conf import Conf

if __name__ == "__main__":
    conf = Conf()
    agent = MainAgent()

    response = agent.run("こんにちは．")

    print(response)
