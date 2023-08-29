# Import necessary libraries
import streamlit as st
from streamlit_player import st_player
from utils import set_api_key

st.set_page_config(
    page_title="Smart With Sebi",
    page_icon=":detective:",
    layout="wide",
)

with st.columns(3)[1]:
    st.image("media/smart_with_sebi.jpeg", width=200)

st.markdown("<h2 style='text-align: center; color: black;'>Welcome to Smart with SEBI portal</h1>", unsafe_allow_html=True)

with st.sidebar:
    if "api_token" not in st.session_state:
        user_openai_api_key = st.text_area("Enter your OPENAI API Key here: ")
        user_serper_api_key = st.text_area("Enter your SERPER API Key here: ")
        if st.button("Submit") and user_openai_api_key and user_serper_api_key:
            st.session_state.openai_api_token, st.session_state.serper_api_token = set_api_key(user_openai_api_key,user_serper_api_key)
            st.success("API Key set successfully!")
    else:
        st.success("API Key already set!")

    st.markdown("**Select a page above!**")

st.markdown("<h3 style='text-align: left; color: black;'><hr> About this project:</h3>", unsafe_allow_html=True)



st_player("https://www.youtube.com/watch?v=jNVTSDwTm14")
