import streamlit as st

history = st.session_state.get("history", [])

messages = st.container(height=300)
for h in history:
    messages.chat_message(h["role"]).write(h["message"])

if prompt := st.chat_input("Say something"):
    history.append({"role": "user", "message": prompt})
    history.append({"role": "assistant", "message": f"Echo: {prompt}"})
    st.session_state["history"] = history
    st.rerun()
