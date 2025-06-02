import sqlite3
from typing import Any

from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from sela.data.schemas import BaseChatModel, Message, Mode, SeLaState
from sela.nodes.casual_talker import CasualTalker
from sela.nodes.mode_selector import ModeSelector
from sela.rags.long_term_memory import LongTermMemory
from sela.utils.datetime_manager import get_dt


class MainAgent:
    def __init__(
        self,
        llm: BaseChatModel | None = None,
        state: SeLaState | None = None,
        checkpoint_path: str = "tmp/checkpoint",
    ):
        if llm:
            self.llm = llm
        else:
            self.llm = ChatOpenAI(model="gpt-4.1", temperature=0)
        self.llm = self.llm.configurable_fields(
            temperature=ConfigurableField(id="temperature")
        )

        self.long_term_memory = LongTermMemory.get_retriever()

        self.mode_selector = ModeSelector(self.llm, self.long_term_memory)
        self.casual_talker = CasualTalker(self.llm, self.long_term_memory)

        if state:
            self.state = state
        else:
            new_message = Message(text="", role="human")
            self.state = SeLaState(user_message=new_message)

        # 自分しか使わないので一旦固定値
        self.checkpoint_conf = {"configurable": {"thread_id": "thread-1"}}

        self.graph = self.create_graph(checkpoint_path)

    def create_graph(self, checkpoint_path: str) -> StateGraph:
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

        checkpointer = self.create_checkpointer(checkpoint_path)

        return workflow.compile(checkpointer=checkpointer)

    def create_checkpointer(self, checkpoint_path: str) -> SqliteSaver:
        conn = sqlite3.connect(checkpoint_path, check_same_thread=False)
        return SqliteSaver(conn)

    def select_mode(self, state: SeLaState) -> dict[str, Any]:
        new_mode: ExecutionMode = self.mode_selector.run(state.user_message)
        return {"mode": new_mode.mode}

    def talk_casual(self, state: SeLaState) -> dict[str, Any]:
        response: Messages = self.casual_talker.run(state.user_message, state.messages)
        return {"messages": response}

    def run(self, user_message: str) -> str:
        new_message = Message(text=user_message, role="human")
        self.state = SeLaState(user_message=new_message)
        result = self.graph.invoke(self.state, self.checkpoint_conf)
        self.state = SeLaState(**result)
        return self.state
