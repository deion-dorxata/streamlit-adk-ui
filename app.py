import streamlit as st
import requests
import json
from datetime import datetime
import time
import os

# Page configuration
st.set_page_config(
    page_title="ADK Chat Agent Interface",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Function to get available agents
def get_available_agents():
    """Get list of available agents from subdirectories"""

    server_url="http://localhost:8080"
    response = requests.get(
                    f"{server_url}/list-apps",
                    headers={"Content-Type": "application/json"}
                )
    agent_list = response.json()
    return agent_list

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_created' not in st.session_state:
    st.session_state.session_created = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"s_{int(time.time())}"
if 'user_id' not in st.session_state:
    st.session_state.user_id = "u_default"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Default credentials (for demo purposes)
DEFAULT_CREDENTIALS = {
    "admin": "password123",
    "user": "demo123",
    "test": "test123"
}

# Function to load initial state from mock_database.json
def load_initial_state(user_id):
    """Load initial session state for the logged-in user from mock_database.json."""
    
    mock_db_path = os.path.join(os.getcwd(), "mock_database.json")
    if os.path.exists(mock_db_path):
        try:
            with open(mock_db_path, "r") as file:
                data = json.load(file)
                for user in data.get("users", []):
                    if user.get("user_id") == user_id:
                        return user
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format in mock_database.json")
        except Exception as e:
            st.error(f"❌ Error reading mock_database.json: {str(e)}")
    return {}  # Return empty dict if file doesn't exist or no match found

def show_login_page():
    """Display the login page"""
    st.title("🔐 ADK Chat Agent - Login")
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Please sign in to continue")
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🔑 Sign In", type="primary", use_container_width=True)
            with col_b:
                show_creds = st.form_submit_button("👁️ Show Demo Credentials", use_container_width=True)
        
        # Handle login
        if login_button:
            if username in DEFAULT_CREDENTIALS and DEFAULT_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success(f"✅ Welcome, {username}!")
                time.sleep(1)  # Brief pause to show success message
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        # Show demo credentials
        if show_creds:
            st.info("**Demo Credentials:**")
            for user, pwd in DEFAULT_CREDENTIALS.items():
                st.code(f"Username: {user} | Password: {pwd}")
        
        st.markdown("---")
        st.markdown("*This is a demo login system with hardcoded credentials.*")

def show_main_app():
    """Display the main application after authentication"""
    # Main title
    st.title("🤖 ADK Chat Agent Interface")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # User session info at top
        st.markdown("---")
        st.subheader("👤 User Session")
        st.info(f"Logged in as: **{st.session_state.username}**")
        
        if st.button("🚪 Logout", type="secondary"):
            # Clear authentication and reset session
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.session_state.session_created = False
            st.rerun()
        
        st.markdown("---")
        
        # Server configuration
        st.subheader("Server Settings")
        server_url = st.text_input(
            "API Server URL",
            value="http://localhost:8080",
            help="The URL where your ADK API server is running"
        )
        
        # Agent configuration
        st.subheader("Agent Settings")
        available_agents = get_available_agents()
        
        # Set default agent
        default_index = 0
        
        agent_name = st.selectbox(
            "Select Agent",
            options=available_agents,
            index=default_index,
            help="Choose from available agent directories"
        )
        
        # Display selected agent info
        st.info(f"📁 Selected Agent Directory: `{agent_name}`")
        
        # Session configuration
        st.subheader("Session Settings")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.user_id = st.text_input(
                "User ID",
                value=st.session_state.user_id,
                help="Unique identifier for the user"
            )
        with col2:
            st.session_state.session_id = st.text_input(
                "Session ID",
                value=st.session_state.session_id,
                help="Unique identifier for this session"
            )
        
        # Initial state configuration
        st.subheader("Initial Session State (Optional)")
        user_data = load_initial_state(st.session_state.username)  # Load user-specific data
        initial_state = st.text_area(
            "Initial State (JSON)",
            value=json.dumps(user_data, indent=2),  # Use initial_state from user data
            height=100,
            help="Optional initial state for the session in JSON format"
        )
        
        # Streaming option
        use_streaming = st.checkbox(
            "Enable Streaming",
            value=False,
            help="Enable token-level streaming for responses"
        )
        
        st.markdown("---")
        
        # Session management buttons
        st.subheader("Session Management")
        
        # Create/Update session button
        if st.button("🔄 Create/Update Session", type="primary"):
            try:
                # Parse initial state
                state_data = {}
                if initial_state.strip():
                    state_data = json.loads(initial_state)
                
                # Create session
                response = requests.post(
                    f"{server_url}/apps/{agent_name}/users/{st.session_state.user_id}/sessions/{st.session_state.session_id}",
                    headers={"Content-Type": "application/json"},
                    json=state_data
                )
                
                if response.status_code == 200:
                    st.session_state.session_created = True
                    st.success(f"✅ Session created/updated successfully!")
                    session_info = response.json()
                    st.json(session_info)
                else:
                    st.error(f"❌ Failed to create session: {response.text}")
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON format for initial state")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Get session info button
        if st.button("ℹ️ Get Session Info"):
            try:
                response = requests.get(
                    f"{server_url}/apps/{agent_name}/users/{st.session_state.user_id}/sessions/{st.session_state.session_id}"
                )
                
                if response.status_code == 200:
                    session_info = response.json()
                    st.success("✅ Session retrieved successfully!")
                    st.json(session_info)
                else:
                    st.error(f"❌ Failed to get session: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Delete session button
        if st.button("🗑️ Delete Session"):
            try:
                response = requests.delete(
                    f"{server_url}/apps/{agent_name}/users/{st.session_state.user_id}/sessions/{st.session_state.session_id}"
                )
                
                if response.status_code == 204:
                    st.session_state.session_created = False
                    st.session_state.messages = []
                    st.success("✅ Session deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to delete session: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Clear chat button
        if st.button("🧹 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Available agents list
        st.subheader("Available Agents")
        if st.button("📋 List All Agents"):
            try:
                response = requests.get(f"{server_url}/list-apps")
                if response.status_code == 200:
                    agents = response.json()
                    st.success("✅ Agents retrieved successfully!")
                    for agent in agents.get('apps', []):
                        st.info(f"• {agent}")
                else:
                    st.error(f"❌ Failed to list agents: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Main chat interface
    main_container = st.container()
    
    with main_container:
        # Session status indicator
        if st.session_state.session_created:
            st.success(f"🟢 Session Active: {st.session_state.session_id}")
        else:
            st.warning("🟡 No active session. Please create a session first.")
        
        # Chat history display
        st.subheader("💬 Chat History")
        
        # Display all messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    # For assistant messages, handle different response formats
                    if isinstance(message["content"], str):
                        st.write(message["content"])
                    elif isinstance(message["content"], dict):
                        st.json(message["content"])
                    elif isinstance(message["content"], list):
                        # Handle list of events
                        for event in message["content"]:
                            if isinstance(event, dict) and "content" in event:
                                if "parts" in event["content"]:
                                    for part in event["content"]["parts"]:
                                        if "text" in part:
                                            st.write(part["text"])
                                        elif "functionCall" in part:
                                            st.code(json.dumps(part["functionCall"], indent=2))
                                        elif "functionResponse" in part:
                                            st.code(json.dumps(part["functionResponse"], indent=2))
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Check if session is created
            if not st.session_state.session_created:
                st.error("⚠️ Please create a session first before sending messages!")
            else:
                # Add user message to history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Display user message
                with st.chat_message("user"):
                    st.write(user_input)
                
                # Prepare the request
                request_data = {
                    "app_name": agent_name,
                    "user_id": st.session_state.user_id,
                    "session_id": st.session_state.session_id,
                    "new_message": {
                        "role": "user",
                        "parts": [{"text": user_input}]
                    }
                }
                
                # Add streaming flag if enabled
                if use_streaming:
                    request_data["streaming"] = True
                
                # Show spinner while waiting for response
                with st.spinner("🤔 Agent is thinking..."):
                    try:
                        if use_streaming:
                            # Use SSE endpoint for streaming
                            response = requests.post(
                                f"{server_url}/run_sse",
                                headers={"Content-Type": "application/json"},
                                json=request_data,
                                stream=True
                            )
                            
                            if response.status_code == 200:
                                # Process SSE stream
                                full_response = []
                                response_placeholder = st.empty()
                                
                                for line in response.iter_lines():
                                    if line:
                                        line = line.decode('utf-8')
                                        if line.startswith("data: "):
                                            try:
                                                event_data = json.loads(line[6:])
                                                full_response.append(event_data)
                                                
                                                # Extract and display text from the event
                                                if "content" in event_data and "parts" in event_data["content"]:
                                                    for part in event_data["content"]["parts"]:
                                                        if "text" in part:
                                                            with response_placeholder.container():
                                                                with st.chat_message("assistant"):
                                                                    st.write(part["text"])
                                            except json.JSONDecodeError:
                                                continue
                                
                                # Add to message history
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": full_response
                                })
                            else:
                                st.error(f"❌ Error: {response.text}")
                        else:
                            # Use regular endpoint
                            response = requests.post(
                                f"{server_url}/run",
                                headers={"Content-Type": "application/json"},
                                json=request_data
                            )
                            
                            if response.status_code == 200:
                                response_data = response.json()
                                
                                # Extract and display the response
                                with st.chat_message("assistant"):
                                    if isinstance(response_data, list):
                                        # Process list of events
                                        response_text = ""
                                        for event in response_data:
                                            if isinstance(event, dict) and "content" in event:
                                                if "parts" in event["content"]:
                                                    for part in event["content"]["parts"]:
                                                        if "text" in part:
                                                            response_text += part["text"]
                                        
                                        if response_text:
                                            st.write(response_text)
                                        else:
                                            # Show raw response if no text found
                                            st.json(response_data)
                                    else:
                                        st.json(response_data)
                                
                                # Add to message history
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response_data
                                })
                            else:
                                st.error(f"❌ Error: {response.text}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Could not connect to the API server. Please make sure it's running.")
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")

# Main application logic - Check authentication and render appropriate view
if not st.session_state.authenticated:
    show_login_page()
else:
    show_main_app()

# Footer (shown on all pages)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit for ADK Chat Agent API | 
        <a href='https://google.github.io/adk-docs/' target='_blank'>ADK Documentation</a></p>
    </div>
    """,
    unsafe_allow_html=True
)