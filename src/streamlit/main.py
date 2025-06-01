import streamlit as st
from sela.agents.main_agent import MainAgent
from sela.utils.conf import Conf

conf = Conf()
agent = MainAgent()

history = st.session_state.get("history", [])


def main():
    messages = st.container(height=300)
    for h in history:
        messages.chat_message(h["role"]).write(h["message"])

    if prompt := st.chat_input("Say something"):
        history.append({"role": "user", "message": prompt})
        history.append({"role": "assistant", "message": agent.run(prompt)})
        st.session_state["history"] = history
        st.rerun()


if __name__ == "__main__":
    main()
