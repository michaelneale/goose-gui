import streamlit as st
import subprocess

GOOSE_EXECUTABLE = '/Users/micn/Documents/code/goose/.venv/bin/goose'

st.title("goose")

st.session_state.commenced = False

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_command := st.chat_input("Enter your command:"):
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(user_command)
    st.session_state.messages.append({"role": "user", "content": user_command})

    # Send command to shell and capture output
    with open('tempfile.txt', 'w') as f:
        f.write("Run the following command, but EXTREMELY CRITICAL IMPORTANT: Please return results formatted as markdown for display, and don't repeat instructions and commands: \n" + user_command)

    process = subprocess.Popen(f'{GOOSE_EXECUTABLE} run --resume-session tempfile.txt', 
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)

    # Wait for process to complete and capture all output
    stdout, stderr = process.communicate()

    # Display the complete output as a single assistant message
    if stdout:
        with st.chat_message("assistant"):
            st.markdown(stdout)
        st.session_state.messages.append({"role": "assistant", "content": stdout})

    # Check for and display errors
    if stderr:
        with st.chat_message("error"):
            st.markdown(stderr)
        st.session_state.messages.append({"role": "error", "content": stderr})
