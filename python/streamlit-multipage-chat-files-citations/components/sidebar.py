import streamlit as st

def create_sidebar():
    with st.sidebar:
        st.info("""
                ### ✅ Instructions
                - **Step 1:** Generate Graphlit project token.
                - **Step 2:** Browse for files to upload and ingest. Or review the [already loaded documents and datasets](https://www.zotero.org/groups/5591103/hi_farm_studies/library).
                - **Step 3:** Enter a prompt to ask about the files using [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.
                """)

        st.markdown("""
            [Support on Discord](https://discord.gg/ygFmfjy3Qx)            
            [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
            [More information](https://www.graphlit.com)      
            """)
