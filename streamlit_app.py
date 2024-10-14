import streamlit as st
import os
import subprocess

def main():
    st.sidebar.title("Settings")
    directory = st.sidebar.text_input("Pick a directory", value=os.getcwd())
    stay_in_session = st.sidebar.checkbox("Stay in session")
    launch_button = st.sidebar.button("Launch")

    user_command = st.text_area("Enter your command:")

    output_placeholder = st.empty()

    session_state = st.session_state

    if 'process' not in session_state:
        session_state.process = None

    if launch_button or session_state.process is None:
        if not os.path.isdir(directory):
            st.error("Invalid directory")
            return
        os.chdir(directory)

        # Start a shell session using 'goose session start'
        session_state.process = subprocess.Popen('goose session start', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if session_state.process and user_command:
        session_state.process.stdin.write(user_command + '\n')
        session_state.process.stdin.flush()

        # Capture and stream output after sending each command
        output = []
        while True:
            line = session_state.process.stdout.readline()
            if not line and session_state.process.poll() is not None:
                break
            if line:
                output.append(line)
                output_placeholder.markdown("".join(output))

        error_line = session_state.process.stderr.readline()
        if error_line:
            output_placeholder.error(error_line)
        if not os.path.isdir(directory):
            st.error("Invalid directory")
            return
        os.chdir(directory)

        # Start a shell session using 'goose session start'
        process = subprocess.Popen('goose session start', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Send user commands and get the results in real time
        if user_command:
            process.stdin.write(user_command + '\n')
            process.stdin.flush()

            # Capture and stream output after sending each command
            output = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    output.append(line)
                    output_placeholder.markdown("".join(output))

            error_line = process.stderr.readline()
            if error_line:
                output_placeholder.error(error_line)

        output = []
        while True:
            if process.poll() is not None:
                break
            line = process.stdout.readline()
            if line:
                output.append(line)
                output_placeholder.markdown("".join(output))
        process.stdout.close()
        process.wait()

        output_placeholder.info("Session ended. Add more input to continue or restart the session.")

if __name__ == "__main__":
    main()
