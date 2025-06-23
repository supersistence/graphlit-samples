import streamlit as st
from other import client, helpers, graph_helpers
from components import header, sidebar, session_state
from graphlit_api import *

st.set_page_config(
    page_title="Hawaii Farm Data Chat - About",
    page_icon="https://raw.githubusercontent.com/supersistence/graphlit-samples/main/python/streamlit-multipage-chat-files-citations/components/hi_data_logo_dalle.png",
    layout="wide"
)

st.markdown("""
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
        ⚠️ This tool was developed and run during Summer 2024 and is no longer functioning.
        It remains online for archival and reference purposes only.
    </div>
""", unsafe_allow_html=True)


# Create sidebar and header
session_state.reset_session_state()
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


st.markdown("""# Knowledge Graph""")


if st.session_state['token'] is None:
    st.info("💡 To view a graph of the uploaded files, click 'Start a Chat Session' on the Start Here page.")
else:
    if st.session_state['token']:
        st.write("Visualize ingested content and extracted entities.")

        contents_graph = None
        error_message = None

        with st.spinner("Loading knowledge graph..."):
            contents_graph, error_message = helpers.run_async_task(client.query_contents_graph, None)

        if error_message is not None:
            st.error(error_message)
        else:
            if contents_graph is not None:
                                
                g = graph_helpers.create_pyvis_contents_graph(contents_graph)

                graph_helpers.display_pyvis_graph(g)

                # NOTE: uncomment to show the raw JSON for the graph
                #json = contents_graph.model_dump_json(indent=2)
                #st.json(json)                
            else:
                st.error('No knowledge graph was created.')

        with st.form("data_graph_form"):
            refresh_graph = st.form_submit_button("Refresh the Knowledge Graph")

            if refresh_graph:
                st.rerun()

        # with st.form("data_search_form"):
        #     submit_content = st.form_submit_button("Chat with the Knowledge Graph  >")

        #     if submit_content:
        #         st.switch_page("pages/3_Chat_With_Knowledge_Graph.py")
