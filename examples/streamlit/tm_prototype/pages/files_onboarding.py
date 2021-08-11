import streamlit as st
import pandas as pd
from kiara import Kiara
from kiara_modules.playground.markus.streamlit import onboard_file_bundle


def app():



    kiara: Kiara = st.session_state["kiara"]

    st.markdown("Download the corpus on your computer, unzip and copy local folder path")
    st.markdown("https://zenodo.org/record/4596345/files/ChroniclItaly_3.0_original.zip?download")
    st.markdown("Paste local folder path into input below") 
    st.markdown("Wait for the success message, and then select next page in top left nav menu")

    
    path = st.text_input('Path to files folder')

    button = st.button("Onboard")
    

    if button:
        module = kiara.operation_mgmt.profiles["table.import_from.folder_path.string"].module
        aliases = ['my_first_table']
        result = module.run(source=path, aliases=aliases)

        table_value = kiara.data_store.load_value(aliases[0])
        st.session_state.data = table_value
        
        st.write("Success! Select the next step from the top left nav menu.")
    
