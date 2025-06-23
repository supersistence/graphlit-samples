import streamlit as st
import pandas as pd
from components import header, sidebar, session_state
from other.helpers import query_contents_count, query_contents
from streamlit_extras.stylable_container import stylable_container
from graphlit import Graphlit
import json
import os

# set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
st.set_page_config(
    page_title="Hawaii Farm Data Chat",
    page_icon="https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/hi_data_logo_dalle.png",
    layout="wide"#,
    # menu_options={"About": "your custom text"}
)

st.markdown(
    """
    <div style="
        background-color: #ffeaea;
        border-bottom: 1px solid #ffb3b3;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 600;
        color: #990000;
        text-align: center;
        z-index: 9999;
    ">
        ⚠️ This tool was developed and run during Summer 2024 and is no longer functioning.<br/>
        The application remains online for archival and reference purposes only.<br/>
        📬 Interested in a similar tool? Contact <a href="mailto:hunter@supersistence.org" style="color:#990000; text-decoration: underline;">hunter@supersistence.org</a>
    </div>
    """, 
    unsafe_allow_html=True
)


def load_config():
    # Construct the full path to the config file
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

# Load the configuration
config = load_config()

# Add custom CSS to hide the GitHub icon
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Initialize session state if not already set
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = config.get('organization_id', '')
    #st.session_state['organization_id'] = st.secrets["organization_id"]
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = config.get('environment_id', '')
    #st.session_state['organization_id'] = st.secrets["environment_id"]
if 'jwt_secret' not in st.session_state:
    st.session_state['jwt_secret'] = config.get('jwt_secret', '')
    #st.session_state['organization_id'] = st.secrets["jwt_secret"]

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

# Inject custom CSS and JavaScript to hide the "eye" icon and specific elements
hide_elements = """
    <style>
        .stTextInput label {
            display: none;
        }
        .stInfo {
            display: none;
        }
        .stTextInput [data-baseweb="input"] {
            display: none;
        }
    </style>
    <script>
        // Find all password fields and remove the toggle visibility button
        const observer = new MutationObserver(() => {
            const inputFields = document.querySelectorAll('[type="password"]');
            inputFields.forEach(field => {
                const parent = field.parentElement;
                const toggleButton = parent.querySelector('[data-baseweb="input"]');
                if (toggleButton) {
                    toggleButton.style.display = 'none';
                }
            });
        });
        observer.observe(document, { childList: true, subtree: true });
    </script>
"""

st.markdown(hide_elements, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.form("credentials_form"):
        st.markdown("### 💡 Start a chat with recent documents and data about Hawaii agriculture here:")

        #st.info("Cick the button below to start a session")

        # Use session state values directly without setting the value parameter
        st.text_input("Organization ID", key="organization_id", type="password")
        st.text_input("Preview Environment ID", key="environment_id", type="password")
        st.text_input("Secret", key="jwt_secret", type="password")

        submit_credentials = st.form_submit_button("Start a Chat Session")

        if submit_credentials:
            if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                # Initialize Graphlit client
                graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

                st.session_state['graphlit'] = graphlit
                st.session_state['token'] = graphlit.token

                #st.switch_page("pages/2_Chat_With_Files.py")
            else:
                st.error("Please fill in all the connection information.")

            #st.markdown("**Python SDK code example:**")

with col2:        
    #st.markdown("**The following Hawaii farm and agricultural research resources have been added to a database that can be queried.**")
    
    # Fetch the count of contents
    #filter = {
                # Your filter here
    #        }
    #count = query_contents_count(filter)
    #if count is not None:
    #    st.markdown(f"**{count} Hawaii farm and agricultural research resources have been added to a database that can be queried.**")
    #else:
    #    st.error("Failed to retrieve the count of contents.")
        
    #count = query_contents_count(filter)
    #if count is not None:
    #    st.write(f"Content count: {count}")
    #else:
   #     st.write("Query failed.")

    def display_table():
            filter = {
                # Your filter here
            }
        
            results = query_contents(filter)
        
            if results and 'data' in results and 'contents' in results['data']:
                contents = results['data']['contents']['results']
                table_data = []
        
                for result in contents:
                    table_data.append({
                        'Name': result.get('name', 'N/A'),
                        'Format': result.get('format', 'N/A')
                    })

                df = pd.DataFrame(table_data)
                df.reset_index(drop=True, inplace=True)
                st.dataframe(df, hide_index=True, use_container_width=True)
                #st.table(df)  # Display the table without indices
                #st.table(table_data)  # Display the table
            else:
                st.error("Failed to retrieve data or no contents found.")
        
    # Call display_table() in your Streamlit app
    with st.expander("Hawaii farm and agricultural research database files"):
        st.markdown("Review the files on [Zotero](https://www.zotero.org/groups/5591103/hi_farm_studies/library)") 
        display_table()

import streamlit as st
import logging
from other import helpers
from components import prompt, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Reset session state
session_state.reset_session_state()

# # Create sidebar and header
# sidebar.create_sidebar()
# header.create_header()

# Set content_done to True for testing purposes
st.session_state['content_done'] = True

# Initialize session state for messages and citations
if "messages" not in st.session_state:
    st.session_state.messages = []

if "citations" not in st.session_state:
    st.session_state.citations = []

# Check if the token is generated
if st.session_state['token'] is None:
    st.info("💡 To get started, click 'Start a Chat Session' to connect to the database.")
else:
    st.markdown("**Enter your questions and get a response with citations from the research database**")

    # Render previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask anything about Hawaii agriculture.", key="chat_input"):
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

                # Log citations
                logging.debug(f"Citations: {citations}")

                # Store and render citations
                if citations:
                    st.session_state.citations.append({"prompt": user_prompt, "citations": citations})
                    helpers.render_citations(citations)

    # Only display the download button if there are messages and citations
    if st.session_state.messages and st.session_state.citations:
        # Prepare the chat and citations for download as a human-readable text file
        chat_text = ""
        for msg in st.session_state.messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            chat_text += f"{role}:\n{content}\n\n"

        # Add citations to the chat_text
        if st.session_state.citations:
            chat_text += "Citations:\n"
            for citation_data in st.session_state.citations:
                chat_text += f"Prompt: {citation_data['prompt']}\n"
                citation_counter = 1  # Reset citation counter for each prompt
                for citation in citation_data['citations']:
                    try:
                        name = citation.content.name
                        page_number = f", Page {citation.page_number}" if citation.page_number else ""
                    except AttributeError:
                        name = "No title available"
                        page_number = ""
                    chat_text += f"{citation_counter}. {name}{page_number}\n"
                    citation_counter += 1
                chat_text += "\n"

        # Add a download button
        st.download_button(
            label="Download Chat and Citations",
            data=chat_text,
            file_name="chat_citations.txt",
            mime="text/plain"
        )
