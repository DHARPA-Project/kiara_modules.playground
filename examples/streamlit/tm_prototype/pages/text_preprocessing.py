import streamlit as st
from st_aggrid import AgGrid

def app():
    st.markdown("## Text pre-processing")

    kiara = st.session_state["kiara"]

    st.write('For languages based on latin characters, use default tokenization option (by word).')
    st.write('This first pre-processing step is necessary to proceed further. Depending on your corpus size, it could take several minutes')
    tokenize = st.selectbox("Tokenize by", ('word', 'character'), key="0")
    token_button = st.button('Proceed')

    if token_button:
        tokenize_workflow = kiara.create_workflow("playground.mariella.language.tokenize")
        tokenize_workflow.inputs.set_values(table=st.session_state.augmented_data, column_name="content")
        tokenized_table_value = tokenize_workflow.outputs.get_value_obj("tokens_array")

        table = tokenized_table_value.get_value_data()


        if table:
        # if the output exists, we write it as a pandas Series (since streamlit supports that natively)
            df = table.to_pandas()
            st.write('Result preview')
            st.write('Use the settings menu to apply pre-processing options')
            st.dataframe(df.head(50))
            my_expander = st.sidebar.expander(label='Settings')
            with my_expander:
                lowercase = st.selectbox("Lowercase", ('no', 'yes'), key="1")
                #isalnum,isalph,isdigit
                display = ['None','Remove all tokens that include numbers','Remove all tokens that include punctuation and numbers','Remove all numbers']
                preprocess = st.radio("Text processing", options=range(len(display)),format_func=lambda x: display[x])
        else:
            st.write("No result")

    