import streamlit as st
import pandas as pd
from kiara import Kiara
from kiara_modules.playground.markus.streamlit import onboard_file_bundle


def app():

    kiara = st.session_state["kiara"]

    st.markdown("## Create dataframe")
    st.markdown("Select sample data from one publication folder located in  kiara_modules.playground/examples/newspaper_corpora/CI_newspaper_subcorpora") 
    st.markdown("Once you're ready, go to the next step via select box on the left")

    uploaded_files = st.file_uploader("Add files", type = 'txt', accept_multiple_files=True)
    
    corpus_alias = "tm1"

    file_names = [i.name for i in uploaded_files]
    file_txt = [i.getvalue().decode("utf-8") for i in uploaded_files]

    df_onboard = pd.DataFrame({
                'File name': file_names,
                'File content': file_txt
            })

    
    st.markdown("### Onboarded file preview")
    st.markdown("Once you're ready selecting files, click 'onboard' below")
    
    st.dataframe(df_onboard)
    onboard_button = st.button(label="Onboard")

    
    if onboard_button and uploaded_files:
        onboard_file_bundle(
            kiara=kiara, uploaded_files=uploaded_files, aliases=[corpus_alias]
        )
        st.markdown(f"Onboarded corpus: {corpus_alias}. Go to the next step via the navigation menu on the left.")
    else:

        st.markdown("Nothing onboarded (yet).")
        st.stop()


    if kiara.data_store.load_value(corpus_alias):

        table_value = kiara.data_store.load_value(corpus_alias)
        #table: pa.Table = table_value.get_value_data()
        #df = table.to_pandas()
        
        st.session_state.data = table_value
        