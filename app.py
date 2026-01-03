import streamlit as st
import os

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(page_title="Limited Memory Storyteller", page_icon="📖")
st.title("📖 Children's Story AI Narrator")
st.markdown(
    "This AI uses **Limited Memory** to discuss the story of *Little Red Riding Hood*."
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input(
        "Enter Hugging Face API Token:",
        type="password",
    )
    st.info("Get a free token at: https://huggingface.co/settings/tokens")

    st.subheader("Memory Configuration")
    window_size = st.slider("Memory Window (k):", 1, 10, 3)
    st.caption("The AI remembers the last 'k' interactions.")

# -------------------------------------------------
# App Logic
# -------------------------------------------------
if not user_api_key:
    st.warning("Please enter your Hugging Face API token in the sidebar to start.")
    st.stop()

try:
    os.environ["HUGGING_FACE_HUB_TOKEN"] = user_api_key

    # -------------------------------------------------
    # LLM (PUBLIC MODEL via ROUTER)
    # -------------------------------------------------
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        task="chat-completions",   # ✅ IMPORTANT
        temperature=0.7,
        max_new_tokens=512,
    )

    chat_model = ChatHuggingFace(llm=llm)

    # -------------------------------------------------
    # Memory
    # -------------------------------------------------
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(
            k=window_size,
            return_messages=True,
        )

    # -------------------------------------------------
    # Prompt
    # -------------------------------------------------
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a whimsical narrator for the story 'Little Red Riding Hood'. "
                "Keep responses concise, friendly, and suitable for children."
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    # -------------------------------------------------
    # Chain
    # -------------------------------------------------
    story_bot = ConversationChain(
        llm=chat_model,
        memory=st.session_state.memory,
        prompt=prompt,
    )

    # -------------------------------------------------
    # Chat UI
    # -------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Ask about the story..."):
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = story_bot.predict(input=user_input)
            st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

except Exception as e:
    st.error(f"Error: {e}")
