import operator
from enum import Enum
from textwrap import dedent
from typing import Annotated, Literal, Union

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field


class Mode(str, Enum):
    TALK_CASUAL = "talk_casual"
    DEBUG = "debug"


class ExecutionMode(BaseModel):
    mode: Mode = Field(
        default=Mode.TALK_CASUAL,
        description=dedent(
            """
    ユーザのクエリに対するエージェントの応答モード
    - talk_casual: 日常的な話し相手として接する
    - debug: 使用しない
    """
        ).strip(),
    )


class Message(BaseModel):
    role: str = Field(..., description="発話者")
    text: str = Field(..., description="発話内容")


class SeLaState(BaseModel):
    user_message: str = Field(..., description="ユーザからのクエリ")
    execution_mode: Mode = Field(
        default=Mode.TALK_CASUAL,
        description="ユーザのクエリに対するエージェントの応答モード",
    )
    messages: Annotated[list[Message], operator.add] = Field(
        default_factory=list, description="会話履歴"
    )


# BaseChatModel に相当する型エイリアス
# (langchain v0.3 では基底クラスを明示的に型指定で用いるのは非推奨らしい)
BaseChatModel = Runnable[list[BaseMessage], Union[BaseMessage, list[BaseMessage]]]
