# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_observable import observable

def app():
    st.markdown("## Timestamped Corpus")

    kiara = st.session_state["kiara"]

    table_value = st.session_state.data
    augmented_table_value = st.session_state.augmented_data

    sql_query_day = "SELECT YEAR(date) as year, MONTH(date) as month, DAY(date) as day, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), DAY(date), pub_name order by year, month, day, pub_name"
    sql_query_month = "SELECT YEAR(date) as year, MONTH(date) as month, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), pub_name ORDER BY year, month, pub_name"
    sql_query_year = "SELECT YEAR(date) as year, pub_name, count(*) as count FROM data group by YEAR(date), pub_name ORDER BY year, pub_name"

    unit = st.radio("Display data by", ("year", "month", "day"))

    if unit == "day":
        query = sql_query_day
    elif unit == "month":
        query = sql_query_month
    else:
        query = sql_query_year
    
    query_workflow = kiara.create_workflow("table.query.sql")
    query_workflow.inputs.set_values(table=augmented_table_value, query=query)

    query_result_value = query_workflow.outputs.get_value_obj("query_result")
    query_result_table = query_result_value.get_value_data()

    st.dataframe(query_result_table.to_pandas())
    

    #observers = observable(
    #    "Test",
    #    notebook="d/50b89c7d50524163",
    #    targets=["viewof chart", "style"],
    #    redefine={"timeSelected": timeSelected, "corpus": cleaned_data, "scaleType": scaleType, "axisLabel": axisLabel},
    #)



