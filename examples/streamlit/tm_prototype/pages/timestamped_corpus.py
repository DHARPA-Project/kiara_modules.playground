# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_observable import observable
import json

def app():
    st.markdown("## Timestamped Corpus")

    kiara = st.session_state["kiara"]

    table_value = st.session_state.data
    augmented_table_value = st.session_state.augmented_data

    sql_query_day = "SELECT strptime(concat(day, '/', month, '/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, DAY(date) as day, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), DAY(date), pub_name ORDER BY year, month, day, pub_name) as agg"
    sql_query_month = "SELECT strptime(concat('01/', month, '/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), pub_name ORDER BY year, month, pub_name) AS agg"
    sql_query_year = "SELECT strptime(concat('01/01/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, pub_name, count(*) as count FROM data group by YEAR(date), pub_name ORDER BY year, pub_name) AS agg"

    unit = "year"
    
    #unit = st.radio("Display data by", ("year", "month", "day"))

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
    


    data = list(query_result_table.to_pandas().to_dict(orient="index").values())
    data_json = json.dumps(data, default=str)
    cleaned_data = json.loads(data_json)

    print(cleaned_data)

    observers = observable(
        "Test",
        notebook="d/d1e17c291019759e",
        targets=["viewof chart", "style"],
        redefine={"timeSelected": unit, "data": cleaned_data},
    )

    # , "scaleType": scaleType, "axisLabel": axisLabel

    st.dataframe(query_result_table.to_pandas())



