import streamlit as st
from agent import agent_step

st.set_page_config(page_title="AutoStream AI", page_icon="🎬")

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🎬 AutoStream AI Assistant</h1>",
    unsafe_allow_html=True
)

# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = {
        "collecting": False,
        "lead": {"name": None, "email": None, "platform": None}
    }

# Display Chat
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
# ---------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    
    # Build Memory (last 5–6 turns)
    # ---------------------------
    history = "\n".join(
        [f"{m['role']}: {m['content']}"
         for m in st.session_state.messages[-6:]]
    )

    
    # Agent Response
    # ---------------------------
    response, new_state = agent_step(
        user_input,
        st.session_state.state,
        history
    )

    st.session_state.state = new_state

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)