import os
import streamlit as st
import numpy as np

# Custom imports 
from multipage import MultiPage
from pages import data_upload, timestamped_corpus

app = MultiPage()

# Title of the main page
st.title("TM Streamlit test")
#col1, col2 = st.beta_columns(2)
#col1.image(display, width = 400)
#col2.title("TM Streamlit test")

# Add all your application here
app.add_page("Upload Data", data_upload.app)
app.add_page("Timestamped data", timestamped_corpus.app)
#app.add_page("Machine Learning", machine_learning.app)
#app.add_page("Data Analysis",data_visualize.app)
#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()