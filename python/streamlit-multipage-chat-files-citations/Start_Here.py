import streamlit as st
import pandas as pd
from components import header, sidebar, session_state
from other.helpers import query_contents_count, query_contents
from streamlit_extras.stylable_container import stylable_container
from graphlit import Graphlit
import json
import os

def load_config():
    # Construct the full path to the config file
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

# Load the configuration
config = load_config()

st.set_page_config(
    page_title="Hawaii Farm Data Chat",
    page_icon="https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/hi_data_logo_dalle.png",
    layout="wide"
)

# Initialize session state if not already set
if 'organization_id' not in st.session_state:
    #st.session_state['organization_id'] = config.get('organization_id', '')
    st.session_state['organization_id'] = st.secrets["organization_id"]
if 'environment_id' not in st.session_state:
    #st.session_state['environment_id'] = config.get('environment_id', '')
    st.session_state['organization_id'] = st.secrets["environment_id"]
if 'jwt_secret' not in st.session_state:
    #st.session_state['jwt_secret'] = config.get('jwt_secret', '')
    st.session_state['organization_id'] = st.secrets["jwt_secret"]

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

        st.info("Cick the button below to start a session")

        # Use session state values directly without setting the value parameter
        st.text_input("Organization ID", key="organization_id", type="password")
        st.text_input("Preview Environment ID", key="environment_id", type="password")
        st.text_input("Secret", key="jwt_secret", type="password")

        submit_credentials = st.form_submit_button("Start a Chat Sesson")

        if submit_credentials:
            if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                # Initialize Graphlit client
                graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

                st.session_state['graphlit'] = graphlit
                st.session_state['token'] = graphlit.token

                st.switch_page("pages/2_Chat_With_Files.py")
            else:
                st.error("Please fill in all the connection information.")

            st.markdown("**Python SDK code example:**")

with col2:        
    st.markdown("**Hawaii farm and agricultural research resources have been added to a database that can be queried.**")
    
    # Fetch the count of contents
    filter = {
                # Your filter here
            }
    
    count = query_contents_count(filter)
    if count is not None:
        st.markdown(f"**{count} Hawaii farm and agricultural research resources have been added to a database that can be queried.**")
    else:
        st.error("Failed to retrieve the count of contents.")
    count = query_contents_count(filter)
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
        
                st.table(table_data)  # Display the table
            else:
                st.error("Failed to retrieve data or no contents found.")
        
        # Call display_table() in your Streamlit app
        display_table()






