import streamlit as st
import os


def app():

    kiara = st.session_state["kiara"]

    table_value = st.session_state.data

    process_metadata = st.radio("Do the file names contain metadata?",("no", "yes"))

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
            st.dataframe(table.to_pandas())
