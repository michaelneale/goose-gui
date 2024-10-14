import streamlit as st
import subprocess

st.title("Simple Shell Chat")

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

    # Initialize shell session if not already started
    if 'process' not in st.session_state:
        st.session_state.process = subprocess.Popen(
            ['goose', 'session', 'start'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    # Send command to shell and capture output
    if st.session_state.process:
        st.session_state.process.stdin.write(user_command + '\n')
        st.session_state.process.stdin.flush()

        # Display each line as an assistant message
        while True:
            line = st.session_state.process.stdout.readline()
            if not line:
                break
            line = line.replace("G❯", '')
            line = line.lstrip()
            if not line.startswith("starting session") and len(line) > 0 and line.strip() != user_command.strip():
                with st.chat_message("assistant"):
                    st.markdown(line)
                    print("line", line)
                    print("user command", user_command)
                st.session_state.messages.append({"role": "assistant", "content": line})

        # Check for errors
        if error_line := st.session_state.process.stderr.readline():
            with st.chat_message("error"):
                st.markdown(error_line)
            st.session_state.messages.append({"role": "error", "content": error_line})
