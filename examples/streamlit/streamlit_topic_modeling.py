# -*- coding: utf-8 -*-

# run with:
#
# streamlit run examples/streamlit/streamlit.py
import datetime
import os
import typing

import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile
from kiara import Kiara
from kiara.workflow.kiara_workflow import KiaraWorkflow
import streamlit as st
import datetime as dt
import pandas as pd
import pyarrow as pa
from dateutil.relativedelta import relativedelta # to add days or years

from kiara_modules.playground.markus.streamlit import init_session, set_workflow_input, process_to_stage, \
    get_step_output

st.title("Kiara/streamlit experiment - Topic modelling")

workflow_file = os.path.join(os.path.dirname(__file__), "..", "pipelines", "topic_modeling_end_to_end.json")
kiara, workflow = init_session(st, module_type=workflow_file)

path = None
with st.form(key="create_graph"):
    path = st.text_input("Path to corpus")
    load_path = st.form_submit_button(label="Load corpus")


languages = st.sidebar.multiselect("Languages", ["german", "italian", "english"])
compute_choerence = st.sidebar.checkbox("Compute coherence", value=False)
num_topic = st.sidebar.slider("Num topic", min_value=1, value=7, max_value=20)

if not path:
    st.stop()

set_workflow_input(workflow, path=path)

process_to_stage(workflow, 5)

dates = get_step_output(workflow, "extract_date_from_file_name", "array")
ts_series = dates.get_value_data().to_pandas()
start_date = ts_series.min().date()
end_date = ts_series.max().date()
format = 'MMM YYYY'  # format output
slider = st.sidebar.slider('Select date', min_value=start_date, value=(start_date, end_date), max_value=end_date, format=format)

set_workflow_input(workflow, earliest=str(slider[0]), latest=str(slider[1]), languages=languages, num_topic=num_topic, compute_choerence=compute_choerence)

process_to_stage(workflow, 6)
table = get_step_output(workflow, "filtered_table", "table")
if table.item_is_valid():
    st.write(table.get_value_data().to_pandas())

st.write(slider[0])
st.write(slider[1])
st.write(languages)
st.write(num_topic)
st.write(compute_choerence)

if st.button("Process"):
    print("BUTTON CLICKED")
    process_to_stage(workflow, 1000)
    print("BUTTON FINISHED")

outputs = workflow.outputs.get_all_value_data()
st.write(outputs)
