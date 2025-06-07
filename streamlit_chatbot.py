
import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Set page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Title
st.title("🤖 AI Chatbot")
st.write("Chat with our AI assistant powered by Groq!")

# Sidebar for API key
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Enter Groq API Key:", type="password")
    if not groq_api_key:
        st.warning("Please enter your Groq API key to continue.")
        st.info("Get your API key from: https://console.groq.com/keys")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "store" not in st.session_state:
    st.session_state.store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

if groq_api_key:
    # Initialize the model
    try:
        model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        chain = prompt | model
        
        # Wrap with message history
        with_message_history = RunnableWithMessageHistory(chain, get_session_history)
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt_input := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt_input})
            with st.chat_message("user"):
                st.write(prompt_input)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    config = {"configurable": {"session_id": "streamlit_session"}}
                    response = with_message_history.invoke(
                        [HumanMessage(content=prompt_input)],
                        config=config
                    )
                    st.write(response.content)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        st.info("Please check your API key and try again.")

# Instructions
with st.expander("ℹ️ How to use"):
    st.write("""
    1. Enter your Groq API key in the sidebar
    2. Start chatting with the AI assistant
    3. The bot will remember your conversation history
    4. You can ask questions, have conversations, or request help with various topics
    """)
