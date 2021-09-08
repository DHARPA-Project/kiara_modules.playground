import streamlit as st
from st_aggrid import AgGrid
import os


def app():

    kiara = st.session_state["kiara"]

    table_value = st.session_state.data

    st.markdown('Wait for file preview to be displayed, before proceeding to the next step')
    st.markdown('*Temporary screen for file names metadata step*')
    st.markdown('*This module will be completed at a later stage *')

    process_metadata = st.radio("Do your file names contain metadata?",("no", "yes"))
    
    st.write("Supported pattern: '/sn86069873/1900-01-05/'")
    st.write("LCCN title information and publication date (yyyy-mm-dd)")

    if process_metadata:
        if process_metadata == 'no':
            st.session_state.metada = False
        
        elif process_metadata == 'yes':
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