from typing import Any

from data.schemas import BaseChatModel, Mode, SeLaState
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from nodes.casual_talker import CasualTalker
from nodes.mode_selector import ModeSelector


class MainAgent:
    def __init__(self, llm: BaseChatModel | None = None):
        if llm:
            self.llm = llm
        else:
            self.llm = ChatOpenAI(model="gpt-4.1", temperature=0)

        self.mode_selector = ModeSelector(self.llm)
        self.casual_talker = CasualTalker(self.llm)

        self.graph = self.create_graph()

    def create_graph(self) -> StateGraph:
        workflow = StateGraph(SeLaState)

        workflow.add_node("select_mode", self.select_mode)
        workflow.add_node("talk_casual", self.talk_casual)

        workflow.set_entry_point("select_mode")

        workflow.add_conditional_edges(
            "select_mode",
            lambda state: state.execution_mode,
            {Mode.TALK_CASUAL: "talk_casual", Mode.DEBUG: END},
        )

        workflow.add_edge("talk_casual", END)

        return workflow.compile()

    def select_mode(self, state: SeLaState) -> dict[str, Any]:
        new_mode: ExecutionMode = self.mode_selector.run(state.user_message)
        return {"mode": new_mode.mode}

    def talk_casual(self, state: SeLaState) -> dict[str, Any]:
        response: str = self.casual_talker.run(state.user_message)
        return {"messages": [response]}

    def run(self, user_message: str) -> str:
        initial_state = SeLaState(user_message=user_message)
        result = self.graph.invoke(initial_state)
        result_state = SeLaState(**result)
        return result_state.messages[-1]
