#run server with $ ollama-mcp-bridge
#run frontend with $ streamlit run frontend.py
import httpx
import streamlit as st 
import toml

with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

#constants
MODEL = config['project']['model']
HOST = config['project']['host']
PORT = config['project']['port']
ENDPOINT = "/api/chat"
PROMPT_POST_URL = f"http://{HOST}:{PORT}{ENDPOINT}"

st.set_page_config(page_title="Local MCP-enabled Chatbot")

with st.sidebar:
    st.title("Local MCP Client-Server")
    st.markdown("This is a basic chatbot which utilizes a custom MCP server for basic tool calling.")


# function for generating LLM response
def generate_response(prompt): 

    data = {
      "model": MODEL,
      "messages": [
        {
          "role": "system",
          "content": "You are an assistant which utilizes available MCP tools."
        },
        {
          "role": "user",
          "content": prompt
        }
      ],
      "think": False,
      "stream": False,
      "options": {
        "temperature": 0.7,
        "top_p": 0.9
      }
    }

    response = httpx.request('POST', PROMPT_POST_URL, json=data, timeout=20.0)     
    
    if response.status_code != 200:
        st.error("Error generating response. Please try again later.")
        return "Error generating response."
    
    response = response.json()['message']['content']
    return response


# welcome message if no chats have occurred
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "Machine Learning Tutor", "content": "Welcome to the MCP-enabled LLM!"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if last message is not from tutor
if st.session_state.messages[-1]["role"] != "Machine Learning Tutor":
    with st.chat_message("Machine Learning Tutor"):
        with st.spinner("Generating an answer for you..."):
            #context = get_context()
            response = generate_response(input) 
            st.write(response) 
    message = {"role": "Machine Learning Tutor", "content": response}
    st.session_state.messages.append(message)
