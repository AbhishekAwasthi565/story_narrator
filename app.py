import streamlit as st
import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate

# --- Page Configuration ---
st.set_page_config(page_title="Limited Memory Storyteller", page_icon="📖")
st.title("📖 Children's Story AI Narrator")
st.markdown("This AI uses **Limited Memory** to discuss the story of *Little Red Riding Hood*.")

# --- Sidebar for Manual API Key Entry ---
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input("Enter Hugging Face API Token:", type="password")
    st.info("Get a free token at: huggingface.co/settings/tokens")

    st.subheader("Memory Configuration")
    window_size = st.slider("Memory Window (k):", 1, 10, 3)
    st.caption("The AI remembers the last 'k' interactions.")

# --- Initialize Chatbot Logic ---
if user_api_key:
    try:
        os.environ["HUGGING_FACE_HUB_TOKEN"] = user_api_key

        # 1. Setup Model
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="text-generation",
            max_new_tokens=512,
            temperature=0.7
        )
        chat_model = ChatHuggingFace(llm=llm)

        # 2. Setup Memory (Stored in Streamlit Session State)
        if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferWindowMemory(k=window_size, return_messages=True)

        # 3. Prompt Template
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a whimsical narrator for 'Little Red Riding Hood'. Keep responses concise and child-friendly."
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        # 4. Chain
        story_bot = ConversationChain(llm=chat_model, memory=st.session_state.memory, prompt=prompt)

        # --- Chat UI ---
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        if prompt_input := st.chat_input("What happens next?"):
            st.session_state.messages.append({"role": "user", "content": prompt_input})
            with st.chat_message("user"):
                st.markdown(prompt_input)

            with st.chat_message("assistant"):
                response = story_bot.predict(input=prompt_input)
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Hugging Face API token in the sidebar to start.")
