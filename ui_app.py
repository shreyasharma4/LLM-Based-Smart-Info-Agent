import streamlit as st
from app.graph_builder import build_graph

# Initialize once
st.set_page_config(page_title="Smart Info Agent", page_icon="🤖", layout="wide")

# Initialize agent graph
graph = build_graph()

st.title(" Smart Info Agent (Azure OpenAI + Tools)")
st.markdown(
    """
    This agent can:
    - Fetch **live weather** 
    - Get and compare **cryptocurrency prices**
    - Retrieve **crypto history trends** 
    - Answer general questions 
    """
)

# Chat UI state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
if user_input := st.chat_input("Ask me anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Query the backend agent
    state = {"query": user_input}
    result = graph.invoke(state)
    response = result["response"]

    # Display agent reply
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
