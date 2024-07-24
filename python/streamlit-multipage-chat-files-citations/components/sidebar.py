import streamlit as st

def create_sidebar():
    with st.sidebar:
        st.markdown("Chat with [uploaded files](https://www.zotero.org/groups/5591103/hi_farm_studies/library) , with citations.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).  Chat completion uses the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
        st.info("""
                ### ✅ Instructions
                - **Step 1:** Start a chat session.
                - **Step 2:** Enter a prompt to ask about the files using [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.
                - **Step 3:** Browse existing files or select other files to upload and ingest.
                """)   
        st.image(
                "https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/SUPERSISTENCE%2Blogo-Photoroom.png",
                width=250, # Manually Adjust the width of the image as per requirement
            )
