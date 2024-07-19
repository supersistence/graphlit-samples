import streamlit as st
from components import header, sidebar, session_state
from other.helpers import query_contents
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
    st.session_state['organization_id'] = config.get('organization_id', '')
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = config.get('environment_id', '')
if 'jwt_secret' not in st.session_state:
    st.session_state['jwt_secret'] = config.get('jwt_secret', '')

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
    st.image(
            "https://images.squarespace-cdn.com/content/v1/5e3885654a153a6ef84e6c9c/1653003266864-VIGG314YMEN3YTAZDR93/SUPERSISTENCE%2Blogo.jpg",
            width=150, # Manually Adjust the width of the image as per requirement
        )
    def display_table():
        filter = {
            # Define your filter criteria here
        }
    
        results = query_contents(filter)
    
        if results:
            table_data = []
            for result in results:
                table_data.append([
                    result.get('name'),
                    result.get('fileExtension')
                ])
    
            headers = ["Name", "File Extension"]
    
            st.title("Query Results")
            st.table(table_data)
    
            # Alternatively, you can use st.dataframe for more interactive tables
            # import pandas as pd
            # df = pd.DataFrame(table_data, columns=headers)
            # st.dataframe(df)
        else:
            st.write("No results found.")

if __name__ == "__main__":
    display_table()





