import streamlit as st
import numpy as np
import pandas as pd
from data_process.file_content import *


def app():
    st.markdown("## Create dataframe")
    st.markdown("Select sample data from one publication folder located in  kiara_modules.playground/examples/newspaper_corpora/CI_newspaper_subcorpora") 
    st.markdown("Once you're ready, go to the next step via select box on the left")

    uploaded_files = st.file_uploader("Add files", type = 'txt', accept_multiple_files=True)

    file_names = [i.name for i in uploaded_files]
    #file_txt = [i.getvalue() for i in uploaded_files]
   
    df = pd.DataFrame(file_names, columns=['file_name'])

    df['file_content'] = [i.getvalue().decode("utf-8") for i in uploaded_files]
    df['publication'] = df['file_name'].apply(lambda x: get_pub_name(get_ref(x)))
    df['date'] = df['file_name'].apply(lambda x: get_date(x))

    st.dataframe(df)
    st.session_state.data = df
