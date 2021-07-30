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

path = "/home/markus/projects/dharpa/notebooks/TopicModelling/data_tm_workflow"


set_workflow_input(workflow, path=path, earliest="1919-01-01", latest="2000-01-01", languages=["italian", "german"], num_topics=7, compute_coherence=False)

print("STARTING")
process_to_stage(workflow, 1000)
print("FINISHED")

outputs = workflow.outputs.get_all_value_data()
st.write(outputs)
