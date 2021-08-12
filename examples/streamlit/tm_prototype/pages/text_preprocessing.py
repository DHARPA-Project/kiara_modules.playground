import streamlit as st


def app():
    st.markdown("## Text pre-processing")

    kiara = st.session_state["kiara"]
    
    my_expander = st.sidebar.expander(label='Settings')
    
    with my_expander:
        tokenize = st.selectbox("Tokenize by", ('sentence', 'word'))
        lowercase = st.selectbox("Lowercase", ('yes', 'no'))
        #filter_tokens = 
