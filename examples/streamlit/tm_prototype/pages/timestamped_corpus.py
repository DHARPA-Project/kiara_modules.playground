# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_observable import observable
import json

def app():
    st.markdown("## Timestamped Corpus")

    kiara = st.session_state["kiara"]

    augmented_table_value = st.session_state.augmented_data

    sql_query_day = "SELECT strptime(concat(day, '/', month, '/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, DAY(date) as day, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), DAY(date), pub_name ORDER BY year, month, day, pub_name) as agg"
    sql_query_month = "SELECT strptime(concat('01/', month, '/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), pub_name ORDER BY year, month, pub_name) AS agg"
    sql_query_year = "SELECT strptime(concat('01/01/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, pub_name, count(*) as count FROM data group by YEAR(date), pub_name ORDER BY year, pub_name) AS agg"


    unit = st.selectbox("Aggregate by", ('year', 'month', 'day'))

    scaleType = st.selectbox("Scale by", ('color', 'height'))

    axisLabel = st.selectbox("Axis", ('5-year', 'year', 'month', 'day'))
    
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

    observers = observable(
        "Test",
        notebook="d/d1e17c291019759e",
        targets=["viewof chart", "style"],
        redefine={"timeSelected": unit, "data": cleaned_data, "scaleType": scaleType, "axisLabel": axisLabel},
        observe=["dateInfo"]
    )

    timeInfo = observers.get("dateInfo")

    col1, col2 = st.columns(2)

    def col1_callback():
        st.session_state.col2 = '0'
        st.session_state.col1 = 'col1'

    def col2_callback():
        st.session_state.col1 = '0'
        st.session_state.col2 = 'col2'


    with col1:
        with st.form(key='my_form'):
            submit_button = st.form_submit_button(label='Data preview', on_click=col1_callback)

    with col2:
        with st.form(key='my_form2'):
            submit_button = st.form_submit_button(label='Display sources', on_click=col2_callback)


    if 'col1' in st.session_state:
        if st.session_state.col1 == 'col1':
            st.dataframe(query_result_table.to_pandas())
    
    if 'col2' in st.session_state:
        
        if st.session_state.col2 == 'col2':

            st.text('Click on the tooltip date to display date')
            
            st.write('hello')

            if timeInfo is not None:

                st.write(timeInfo)

                
                sql_query_day2 = f"SELECT pub_name, date, content FROM data WHERE DATE_PART('year', date) = {timeInfo[0]} AND DATE_PART('month', date) = {timeInfo[1]} and DATE_PART('day', date) = {timeInfo[2]}"
                sql_query_month2 = f"SELECT pub_name, date, content FROM data WHERE DATE_PART('year', date) = {timeInfo[0]} AND DATE_PART('month', date) = {timeInfo[1]}"
                sql_query_year2 = f"SELECT pub_name, date, content FROM data WHERE DATE_PART('year', date) = {timeInfo[0]}"

                if unit == "day":
                    query2 = sql_query_day2
                elif unit == "month":
                    query2 = sql_query_month2
                else:
                    query2 = sql_query_year2

                
                query_workflow2 = kiara.create_workflow("table.query.sql")
                query_workflow2.inputs.set_values(table=augmented_table_value, query=query2)

                query_result_value2 = query_workflow2.outputs.get_value_obj("query_result")
                query_result_table2 = query_result_value2.get_value_data()

                df2 = query_result_table2.to_pandas()
                print(df2)
                st.dataframe(df2.head(10))

    
                

                
    






