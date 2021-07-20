# -*- coding: utf-8 -*-

import pyarrow as pa
import streamlit as st
from kiara import Kiara

kiara = Kiara()

st.title("My first kiara streamlit app")


result_table: pa.Table = kiara.run(
    "table.from_csv",
    inputs={
        "path": "/home/markus/projects/dharpa/notebooks/NetworkXAnalysis/JournalEdges1902.csv"
    },
    output_name="table",
    resolve_result=True,
)

df = result_table.to_pandas()

st.write(df)
