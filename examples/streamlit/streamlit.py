# -*- coding: utf-8 -*-

# run with:
#
# streamlit run examples/streamlit/streamlit.py


import pyarrow as pa
import streamlit as st
from kiara import Kiara

kiara = Kiara()

st.title("My first kiara streamlit app")


result_table: pa.Table = kiara.run(
    "table.import.from_local_file",
    inputs={
        "path": "/home/markus/projects/dharpa/notebooks/NetworkXAnalysis/JournalEdges1902.csv"
    },
    output_name="table",
    resolve_result=True,
)

df = result_table.to_pandas()

st.write(df)
