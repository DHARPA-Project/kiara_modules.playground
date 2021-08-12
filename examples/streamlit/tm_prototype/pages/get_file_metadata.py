import streamlit as st
from st_aggrid import AgGrid
import os


def app():

    kiara = st.session_state["kiara"]

    table_value = st.session_state.data

    st.markdown('Wait for file preview to be displayed, before proceeding to the next step')
    st.markdown('*Temporary screen for file names metadata step*')
    st.markdown('*This module will be completed at a later stage (all help welcome!)*')
    
    my_expander = st.sidebar.expander(label='Settings')
    
    with my_expander:
    
        process_metadata = st.radio("Do your file names contain metadata?",("yes", "no"))

        if process_metadata == "yes":

            file_format = st.radio("Which pattern describes your file names?", ('/sn86069873/1900-01-05/', ''))

    if file_format == '/sn86069873/1900-01-05/':
        # load the pipeline file and create a workflow
        augment_pipeline = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "newspaper_corpora",
            "augment_newspaper_corpora_table.json",
        )
    
        workflow = kiara.create_workflow(augment_pipeline)
        # set our table as input to the workflow
        workflow.inputs.set_value("value_id", table_value.id)

        # retrieve the actual table value
        augmented_table_value = workflow.outputs.get_value_obj("table")

        st.session_state.augmented_data = augmented_table_value

        table = augmented_table_value.get_value_data()
        df = table.to_pandas()
        st.write('Result preview')
        AgGrid(df.head(50))
