# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_observable import observable

# st.markdown('<style>@import url("https://fonts.googleapis.com/css2?family=Palanquin:wght@400;700&display=swap")</style>', unsafe_allow_html=True)
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))


timeSelected = st.sidebar.radio(
    label="Select time span", index=3, options=["day", "week", "month", "year"]
)


observers = observable(
    "",
    notebook="d/50b89c7d50524163",
    targets=["viewof chart", "style"],
    # observe=["corpus_agg"],
    redefine={"timeSelected": timeSelected},
)


# data = observers.get("corpus_agg")
# df = pd.DataFrame(data)
# st.dataframe(df)
