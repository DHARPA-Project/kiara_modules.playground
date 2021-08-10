import streamlit as st
import pandas as pd
from kiara import Kiara
from kiara_modules.playground.markus.streamlit import onboard_file_bundle


def app():



    kiara: Kiara = st.session_state["kiara"]

    st.markdown("Select sample data txt files from one publication folder located in  kiara_modules.playground/examples/newspaper_corpora/CI_newspaper_subcorpora") 
    st.markdown("Please wait for the success message to proceed further.")

    
    path = st.text_input('Path to files folder')

    button = st.button("Import")
    

    if button:
        module = kiara.operation_mgmt.profiles["table.import_from.folder_path.string"].module
        aliases = ['my_first_table']
        result = module.run(source=path, aliases=aliases)

        # table_obj = result.get_value_obj("value_item")
        table_value = kiara.data_store.load_value(aliases[0])
        st.session_state.data = table_value
        
        st.write("Success! Select the next step from the top left nav menu.")
    
