import streamlit as st
from components import sidebar, header

st.set_page_config(
    page_title="Hawaii Farm Data Chat - About",
    page_icon="https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/hi_data_logo_dalle.png",
    layout="wide"
)

# Create sidebar and header
sidebar.create_sidebar()
header.create_header()

def about_page():
    st.title("About Hawaii Farm Data Chat")

    st.markdown("""
    Welcome to the Hawaii Farm Data Chat! This platform is designed to provide comprehensive and interactive access to recent agricultural research and data about Hawaii. Our goal is to empower farmers, researchers, policymakers, and the general public with valuable insights and information that can drive informed decision-making and foster a resilient agricultural community in Hawaii.

    #### Key Features:

    - **Relevant Research Database:** Explore a rich database of Hawaii farm and agricultural research resources. The [database](https://www.zotero.org/groups/5591103/hi_farm_studies/library) includes a growing collection of documents, studies, and data sets, all curated to support your agricultural needs.
          
    - **Interactive Chat Interface:** Start a chat session to ask questions about recent agricultural research and receive detailed, cited answers. Our platform leverages advanced data retrieval methods to provide relevant information quickly.
      
    - **Chat Session Downloads:** After engaging in a chat session, you can download the conversation along with cited answers for future reference. This feature ensures you have access to the information and insights discussed, even after the session ends.
    
    #### How to Use the App:

    1. **Start a Chat Session:** Click the "Start a Chat Session" button to initiate a chat session. This will enable you to ask questions and get answers from the research database.
       
    2. **Explore Research Resources:** Use the provided tools to query and explore the extensive database of agricultural research resources. You can view detailed information and download relevant documents.

    We are committed to supporting the agricultural community in Hawaii through access to high-quality research and data. Whether you're a farmer looking for the latest best practices, a researcher seeking detailed data, or a policymaker in need of informed insights, Hawaii Farm Data Chat is here to help.

    Feel free to explore the platform and reach out with any questions or feedback. Together, we can drive the future of agriculture in Hawaii!
    """)

if __name__ == "__main__":
    about_page()
