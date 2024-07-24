import streamlit as st
from other import helpers
from components import prompt, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

# Reset session state
session_state.reset_session_state()


# Create sidebar and header
sidebar.create_sidebar()
header.create_header()

# Set content_done to True for testing purposes
st.session_state['content_done'] = True

# Check if the token is generated
if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    st.markdown("**Enter your questions and get a response with citations from the research database**") 
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
            
            message, citations, error_message = helpers.run_async_task(prompt.handle_prompt, user_prompt)

            if error_message:
                st.error(f"Failed to prompt conversation. {error_message}")
            else:
                # Prompt conversation
                with st.chat_message("assistant"):
                    st.session_state.messages.append({"role": "assistant", "content": message})

                    # Render assistant message
                    st.markdown(message)

                    # Render citations
                    if citations:
                        helpers.render_citations(citations)
        
