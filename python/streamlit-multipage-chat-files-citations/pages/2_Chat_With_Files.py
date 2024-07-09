import streamlit as st
from other import helpers
from components import prompt, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

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
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['content_done']:
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Render previous messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_prompt := st.chat_input("Ask me anything about your content.", key="chat_input"):
                st.session_state.messages.append({"role": "user", "content": user_prompt})

                # Render user prompt
                with st.chat_message("user"):
                    st.markdown(user_prompt)

                # Call the Graphlit API to handle the user prompt
                message, citations, error_message = helpers.run_async_task(prompt.handle_prompt, user_prompt)

                if error_message:
                    st.error(f"Failed to prompt conversation. {error_message}")
                else:
                    # Render assistant's response
                    with st.chat_message("assistant"):
                        st.session_state.messages.append({"role": "assistant", "content": message})
                        st.markdown(message)

                        # Render citations if available
                        if citations:
                            helpers.render_citations(citations)
        else:
            st.info("Please ingest files to chat with.")

    with col2:
        st.markdown("### 📄 Ingested Files")
        # Display the ingested files (assuming they are stored in session state or fetched via API)
        ingested_files = helpers.get_ingested_files(st.session_state['token'])  # Adjust this to your actual implementation
        for file in ingested_files:
            st.markdown(f"- {file}")

        st.markdown("""
            **Zotero Library:**  
            [Access the Zotero library here](https://www.zotero.org/groups/5591103/hi_farm_studies/library) to review the already uploaded files.
        """)
