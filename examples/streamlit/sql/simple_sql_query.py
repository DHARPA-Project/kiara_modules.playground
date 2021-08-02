# -*- coding: utf-8 -*-

# run with:
#
# streamlit run examples/streamlit/sql/simple_sql_query.py


import streamlit as st

from kiara_modules.playground.markus.streamlit import (
    find_all_aliases_of_type,
    init_session,
    onboard_file,
    set_workflow_input,
)

st.title("Kiara/streamlit experiment: simple sql query")

# initialize kiar workflow and store it in the streamlit session state
module_type = "table.query.sql"
kiara, workflow = init_session(st, module_type=module_type)

# add a file import widget, so users can import files if their kiara data store is empty
fp = st.file_uploader(
    label="Onboard table data (.csv)", type=["csv"], accept_multiple_files=True
)
if fp:
    onboard_file(kiara=kiara, st=st, uploaded_file=fp)

selected_alias = st.selectbox(
    "Select dataset", find_all_aliases_of_type(kiara, value_type="table")
)

if not selected_alias:
    st.stop()

workflow.inputs.set_value("table", f"value:{selected_alias}")
value = kiara.data_registry.get_value_item(selected_alias)
data = value.get_value_data()

st.write(f"## Table: *{selected_alias}*")
st.dataframe(data.to_pandas())


with st.form(key="sql_query"):
    query = st.text_input("SQL Query")
    st.write(
        "*Note*: the query must use the relation name '***data***' (e.g. 'select \\* from ***data***)"
    )

    submit_button = st.form_submit_button(label="Submit")

if query:
    set_workflow_input(workflow, process=True, query=query)

result = workflow.outputs.get_value_data("query_result")
if result:
    st.dataframe(result.to_pandas())
