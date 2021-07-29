# -*- coding: utf-8 -*-

# run with:
#
# streamlit run examples/streamlit/streamlit.py


import streamlit as st
from kiara import Kiara
from kiara.workflow.kiara_workflow import KiaraWorkflow

st.title("Kiara/streamlit experiment 1")

if "kiara" not in st.session_state:
    print("CREATE KIARA")
    kiara = Kiara()
    st.session_state["kiara"] = kiara
else:
    kiara = st.session_state["kiara"]

if "workflow" not in st.session_state:
    print("CREATE WORKFLOW")
    workflow: KiaraWorkflow = kiara.create_workflow("table.query.sql")
    st.session_state["workflow"] = workflow
else:
    workflow = st.session_state["workflow"]

selected_alias = st.sidebar.selectbox("Select dataset", list(kiara.data_store.aliases))

workflow.inputs.set_value("table", f"value:{selected_alias}")
value = kiara.data_registry.get_value_item(selected_alias)
data = value.get_value_data()

st.write(f"## Table: *{selected_alias}*")
st.dataframe(data.to_pandas())


with st.form(key="sql_query"):
    query = st.text_input("SQL Query")
    submit_button = st.form_submit_button(label="Submit")


workflow.inputs.set_value("query", query)

result = workflow.outputs.get_value_data("query_result")
st.dataframe(result.to_pandas())



