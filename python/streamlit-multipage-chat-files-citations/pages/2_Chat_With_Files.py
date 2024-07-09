import streamlit as st
from other import helpers
from components import header, sidebar, session_state

st.set_page_config(
    page_title="Chat with Files",
    page_icon="💬",
    layout="wide"
)

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    # Simulate already ingested files (in a real application, you would load these from your backend)
    def get_ingested_files():
        return ["Document1.pdf", "Document2.pdf", "Document3.pdf"]

    ingested_files = get_ingested_files()

    # Initialize chat history in session state if not already set
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💬 Chat with your data")

        # Chat history display
        chat_history_container = st.container()
        with chat_history_container:
            for message in st.session_state['chat_history']:
                st.markdown(message)

        # Chat input
        with st.form("chat_form"):
            user_input = st.text_input("Your message", key="user_input")
            send_message = st.form_submit_button("Send")

            if send_message and user_input:
                st.session_state['chat_history'].append(f"**You:** {user_input}")
                # Here, you would add the logic to process the user input and generate a response
                response = f"**Bot:** You said '{user_input}'. (This is a placeholder response.)"
                st.session_state['chat_history'].append(response)
                st.experimental_rerun()

    with col2:
        st.markdown("### 📄 Ingested Files")
        for file in ingested_files:
            st.markdown(f"- {file}")

        st.markdown("""
            **Zotero Library:**  
            [Access the Zotero library here](https://www.zotero.org/groups/5591103/hi_farm_studies/library) to review the already uploaded files.
        """)
