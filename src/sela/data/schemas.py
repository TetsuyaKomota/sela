import operator
from datetime import datetime
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
    dt: datetime = Field(default_factory=lambda: datetime.now(), description="発話時刻")

    def __str__(self):
        dt_str = self.dt.strftime("%Y%m%d %H:%M:%S")
        display_name = "SeLa" if self.role == "assistant" else "コモタ"
        return f"{display_name}|{dt_str}:\n{self.text}\n"


class Messages(BaseModel):
    messages: list[Message] = Field(
        default_factory=list, description="発話履歴のリスト"
    )

    def __add__(x1, x2):
        # Stateには直近100の履歴のみ残す
        # 各nodeでどこまで使うかはnode側で指定する
        return Messages(messages=(x1.messages + x2.messages)[-100:])


class ImportantFactor(BaseModel):
    factor: str = Field(..., description="注目すべき重要な要素")


class SeLaState(BaseModel):
    user_message: Message = Field(..., description="ユーザからの発話")
    execution_mode: Mode = Field(
        default=Mode.TALK_CASUAL,
        description="ユーザのクエリに対するエージェントの応答モード",
    )
    messages: Annotated[Messages, operator.add] = Field(
        default_factory=Messages, description="会話履歴"
    )
    important_factor: ImportantFactor = Field(
        default=ImportantFactor(factor=""), description="長期記憶に残すべき重要な要素"
    )


# BaseChatModel に相当する型エイリアス
# (langchain v0.3 では基底クラスを明示的に型指定で用いるのは非推奨らしい)
BaseChatModel = Runnable[list[BaseMessage], Union[BaseMessage, list[BaseMessage]]]
