import streamlit as st
from other import client, helpers, graph_helpers
from components import header, sidebar, session_state
from graphlit_api import *


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