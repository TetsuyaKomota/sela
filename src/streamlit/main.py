import streamlit as st
from sela.agents.main_agent import MainAgent
from sela.utils.conf import Conf

conf = Conf()


def main():
    messages = st.container(height=300)

    agent = st.session_state.get("agent", MainAgent())

    for h in agent.state.messages:
        messages.chat_message(h.role).write(h.text)

    if prompt := st.chat_input("Say something"):
        agent.run(prompt)
        st.session_state["agent"] = agent
        st.rerun()


if __name__ == "__main__":
    main()
