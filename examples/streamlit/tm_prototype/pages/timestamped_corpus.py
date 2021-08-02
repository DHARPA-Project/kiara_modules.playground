# -*- coding: utf-8 -*-
import json

import pandas as pd
import pyarrow as pa
import streamlit as st
from kiara import Kiara

# before running this, the dataset must be imported into the local kiara data store, with the alias 'df_distrib':
#
# kiara run table.import.from_local_file path=/Users/mariella.decrouychan/Documents/kiara/kiara_modules.playground/examples/data/tm/df_distrib-3.csv aliases=df_distrib
from kiara.data import Value
from pandas import DataFrame
from streamlit_observable import observable

def app():
    st.markdown("## Timestamped Corpus")

    kiara = Kiara.instance()

    table_value: Value = kiara.data_store.load_value("df_distrib")

    table: pa.Table = table_value.get_value_data()
    df: DataFrame = table.to_pandas()


    data = list(df.to_dict(orient="index").values())
    data_json = json.dumps(data, default=str)
    cleaned_data = json.loads(data_json)

    # print(cleaned_data)

    timeSelected = st.sidebar.selectbox(
        label="Select time span", index=0, key="0", options=["year", "month", "day"]
    )

    scaleType = st.sidebar.selectbox(
        label="Select scale type", index=0, key="1", options=["color", "height"]
    )

    axisLabel = st.sidebar.selectbox(
        label="Select axis label", index=0, key="2", options=["5-year", "year", "month", "day"]
    )

    #dataView = st.sidebar.selectbox(
    #    label="Data view", index=0, key="3", options=["Aggregated data", "Sources"]
    #)

    # we need to assemble the sql query with the column value to filter on
    query = f"select * from data where agg='{timeSelected}'"
    # now we run the 'table.query.sql' kiara module with our table and query
    result = kiara.run("table.query.sql", inputs={"table": table_value, "query":query})
    # here we extract the result table
    query_result_table = result.get_value_data("query_result")


    observers = observable(
        "Test",
        notebook="d/50b89c7d50524163",
        targets=["viewof chart", "style"],
        redefine={"timeSelected": timeSelected, "corpus": cleaned_data, "scaleType": scaleType, "axisLabel": axisLabel},
    )

    # old version with pandas filtering
    # st.dataframe(df[df['agg'] == timeSelected])

    # here we convert the result table to a pandas data frame
    df_result = query_result_table.to_pandas()
    st.dataframe(df_result)

    dataView = st.sidebar.selectbox(
        label="Data view", index=0, key="3", options=["Aggregated data", "Sources"]
    )


