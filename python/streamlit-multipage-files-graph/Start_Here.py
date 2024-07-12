import streamlit as st
from components import header, sidebar, session_state
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
    page_title="Graphlit Demo Application",
    page_icon="💡",
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

col1 = st.columns(1)

with col1:
    with st.form("credentials_form"):
        st.markdown("### 💡 Start here:")

        st.info("Cick the button below to start a session")

        # Use session state values directly without setting the value parameter
        st.text_input("Organization ID", key="organization_id", type="password")
        st.text_input("Preview Environment ID", key="environment_id", type="password")
        st.text_input("Secret", key="jwt_secret", type="password")

        submit_credentials = st.form_submit_button("Start a sesson")

        if submit_credentials:
            if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                # Initialize Graphlit client
                graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

                st.session_state['graphlit'] = graphlit
                st.session_state['token'] = graphlit.token

                st.switch_page("pages/1_Upload_Files.py")
            else:
                st.error("Please fill in all the connection information.")
