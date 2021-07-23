# -*- coding: utf-8 -*-

# run with:
#
# streamlit run examples/streamlit/streamlit.py


import streamlit as st
from kiara import Kiara
from kiara.workflow.kiara_workflow import KiaraWorkflow

st.title("Kiara/observable proof-of-concept app")

if "kiara" not in st.session_state:
    print("CREATE KIARA")
    kiara = Kiara()
    st.session_state["kiara"] = kiara
else:
    kiara = st.session_state["kiara"]

if "workflow" not in st.session_state:
    print("CREATE WORKFLOW")
    workflow: KiaraWorkflow = kiara.create_workflow("table.import.from_local_file")
    st.session_state["workflow"] = workflow
else:
    workflow = st.session_state["workflow"]


with st.form(key="Workflow inputs"):
    filename = st.text_input("Enter a file path:")
    submit_button = st.form_submit_button(label="Submit")


workflow.inputs.set_value("path", filename)

state = workflow.get_current_state()
# st.write(state.dict())

output = workflow.outputs.get_all_value_objects()
st.write(output)

data = workflow.outputs.get_value_data("table")
st.write(data.to_pandas())
