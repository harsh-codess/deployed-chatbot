
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
store = {}
model = None
with_message_history = None

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def initialize_model(api_key):
    global model, with_message_history
    try:
        model = ChatGroq(model="Gemma2-9b-It", groq_api_key=api_key)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        chain = prompt | model
        with_message_history = RunnableWithMessageHistory(chain, get_session_history)
        return True
    except Exception as e:
        print(f"Error initializing model: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "AI Chatbot API is running!",
        "endpoints": {
            "POST /chat": "Send a message to the chatbot",
            "GET /health": "Check API health"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_initialized": model is not None})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        api_key = data.get('api_key') or os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        
        # Initialize model if not already done
        if model is None:
            if not initialize_model(api_key):
                return jsonify({"error": "Failed to initialize model"}), 500
        
        message = data['message']
        session_id = data.get('session_id', 'default_session')
        
        # Generate response
        config = {"configurable": {"session_id": session_id}}
        response = with_message_history.invoke(
            [HumanMessage(content=message)],
            config=config
        )
        
        return jsonify({
            "response": response.content,
            "session_id": session_id
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Try to initialize with environment variable
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        initialize_model(api_key)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
