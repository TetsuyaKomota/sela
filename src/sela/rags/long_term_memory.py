from glob import glob
from os import makedirs
from os.path import exists, join
from textwrap import dedent
from typing import Any, Callable

from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings

from sela.utils.datetime_manager import get_dt


class LongTermMemory:
    retriever: VectorStoreRetriever = None
    vs: FAISS = None

    @staticmethod
    def get_retriever(
        dir_path: str = "tmp/long_term_memory",
    ) -> Callable[dict[str, Any], str]:
        if not LongTermMemory.retriever:
            if not exists(dir_path):
                LongTermMemory._create_initial_knowledge(dir_path)
            LongTermMemory._build_vectorstore(dir_path)

        def _f(params: dict[str, Any]) -> str:
            documents = LongTermMemory.retriever.invoke(params["user_message"].text)
            contents = "\n".join([f"- {d.page_content}" for d in documents])
            output = dedent(
                f"""
                必要に応じて，以下の情報を活用してください．
                ただし，回答のために有益でない場合は必ずしも参照する必要はありません
                {contents}
            """
            ).strip()
            return output

        return _f

    @staticmethod
    def _create_initial_knowledge(dir_path: str):
        text = "SeLaはLangGraphを用いて開発されたパーソナルAIである"
        makedirs(dir_path)
        LongTermMemory.add(text, dir_path)

    @staticmethod
    def _build_vectorstore(dir_path: str):
        doc_list = []
        for p in glob(join(dir_path, "*.txt")):
            with open(p, "rt", encoding="utf-8_sig") as f:
                doc_list.append(f.read().strip())

        embeddings = OpenAIEmbeddings()
        LongTermMemory.vs = FAISS.from_texts(doc_list, embeddings)
        LongTermMemory.retriever = LongTermMemory.vs.as_retriever(
            search_kwargs={"k": 3}
        )

    @staticmethod
    def add(text: str, dir_path: str = "tmp/long_term_memory"):
        timestamp = int(get_dt().timestamp() * 1000)
        output_path = join(dir_path, f"{timestamp}.txt")
        with open(output_path, "wt", encoding="utf-8_sig") as f:
            f.write(text)

        if LongTermMemory.vs:
            LongTermMemory.vs.add_texts([text])
