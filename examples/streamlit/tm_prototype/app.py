import os
import streamlit as st
from kiara import Kiara

# Custom imports 
from multipage import MultiPage
from pages import files_onboarding, timestamped_corpus

app = MultiPage()

# Title of the main page
st.title("TM Streamlit test")

kiara = Kiara.instance()
st.session_state["kiara"] = kiara

# Add all your application here
app.add_page("Upload Data", files_onboarding.app)
app.add_page("Timestamped data", timestamped_corpus.app)

# The main app
app.run()