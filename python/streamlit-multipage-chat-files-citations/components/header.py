import streamlit as st

def create_header():
    #st.image("https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/hi_data_logo_dalle.png", width=128)
    #st.title("Hawaii Farm Data Dialog Graphlit Platform")
    #st.markdown("Chat with any uploaded files, with citations.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).  Chat completion uses the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.image("https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/hi_data_logo_dalle.png", width=128)
    
    with col2:
        st.title("Hawaii Farm Chat")
    st.header('Ask questions of recent agricultural research, get answers with citations.', divider='rainbow')

