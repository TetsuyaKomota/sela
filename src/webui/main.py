from datetime import datetime, timedelta

import streamlit as st

from sela.agents.main_agent import MainAgent
from sela.utils.conf import Conf

conf = Conf()


@st.cache_resource(ttl=timedelta(days=1))
def get_or_create_agent():
    return MainAgent()


def update_chat(agent, prompt):
    agent.run(prompt)
    st.rerun()


def login_greed(agent):
    # agent が初期化されている場合は，ログイン時の挨拶をする
    if agent.state.user_message.text == "":
        now = datetime.now()
        if 7 <= now.hour < 10:
            prompt = "おはようございます"
        elif 10 <= now.hour < 18:
            prompt = "こんにちは"
        else:
            prompt = "こんばんは"
        update_chat(agent, prompt)


def view_chat(agent):
    messages = st.container()

    for h in agent.state.messages.messages[-10:]:
        with messages.chat_message(h.role):
            st.text(str(h))


def view_ui(agent):
    if prompt := st.chat_input("Say something"):
        update_chat(agent, prompt)


def view_state(agent):
    state = agent.state
    with st.expander("SeLaState を確認"):
        st.markdown("### execution_mode")
        st.markdown(state.execution_mode)

        st.markdown("### user_message")
        st.markdown(state.user_message)

        st.markdown("### important_factor")
        st.markdown(state.important_factor)


def main():
    st.set_page_config(
        page_title="SeLa チャット",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    agent = get_or_create_agent()

    login_greed(agent)

    view_chat(agent)

    view_ui(agent)

    view_state(agent)


if __name__ == "__main__":
    main()
