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

col1, col2 = st.columns(2)

with col1:
    with st.form("credentials_form"):
        st.markdown("### 💡 Start here:")

        st.info("Locate connection information for your project in the [Graphlit Developer Portal](https://portal.graphlit.dev/)")

        # Use session state values directly without setting the value parameter
        st.text_input("Organization ID", key="organization_id", type="password")
        st.text_input("Preview Environment ID", key="environment_id", type="password")
        st.text_input("Secret", key="jwt_secret", type="password")

        submit_credentials = st.form_submit_button("Generate Token")

        if submit_credentials:
            if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:
