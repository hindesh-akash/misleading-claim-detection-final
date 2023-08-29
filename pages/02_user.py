# --- IMPORT DEPENDENCIES -------------------------------+
import sys
import streamlit as st

# obtain path to "english.wav" in the same folder as this script
from os import PathLike
import base64
from pathlib import Path
# setting path

sys.path.append("../prompts")
sys.path.append("../utils")

from prompts import *
from utils import *
from streamlit_option_menu import option_menu


# --- TITLE --------------------------------------------+

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

image_bytes = img_to_bytes("media/smart_with_sebi.jpeg")
header_html = f"""
    <header>
        <h2 style="text-align: center; margin-top:10px;"> <img src='data:image/png;base64,{image_bytes}' alt="My Logo" style="float: left; margin-bottom: 10px;width:100px;height:100px;"> USER PAGE</h1>
    </header>
    """
st.markdown(
    header_html, unsafe_allow_html=True,
)


with st.sidebar:
    if "openai_api_token" and "serper_api_token" not in st.session_state:
        st.error("Set the API key first!")
    else:
        st.success("API Key already set!")
    st.markdown("**Select a page above!**")

# --- OPTION MENU --------------------------------------+
selected = option_menu(
    menu_title=None,
    options=["TEXT", "AUDIO", "VIDEO", "IMAGE", "QnA"],
    icons=["card-text", "volume-up", "camera-reels", "image", "question-circle"],
    menu_icon="cast",
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "indigo"},
    },
)

# Main content based on user's selected
if selected == "TEXT":
    st.write("**TEXT BASED CLAIM DETECTION:**\n\n")
    examples = ["", "Kingfisher company has been restored, keep looking for its IPO and invest in it!"]

    example_select = st.selectbox("Select an example", examples)
    if example_select: 
        prompt = st.text_area("User Input: ",value=example_select)
    else:
        prompt = st.text_area("User Input: ")
        

    if st.button("Submit") and prompt:
        new_claim_detection_pipeline(prompt)
        financial_points = financial_point_extractor(prompt)
        display_video_links(financial_points)
        # display_articles(financial_points)

#-------------------------------------------------------------------------------

if selected == "AUDIO":
    st.write("**AUDIO BASED CLAIM DETECTION:**")

    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "ogg", "wav"])
    if audio_file:
        st.audio(audio_file, format="audio/ogg", start_time=0)
        transcript = transcribe_audio(audio_file)
        prompt = st.text_area("Transcribed User Input", value=transcript)
        
        if st.button("Submit") and prompt:
            new_claim_detection_pipeline(prompt)
            financial_points = financial_point_extractor(prompt)
            display_video_links(financial_points)

#--------------------------------------------------------------------------------


if selected == "IMAGE":
    st.write("**IMAGE BASED CLAIM DETECTION:**")
    example_images = {
    "Sample Image 1": "media/text_influencer.jpg"
    }

    image_type = st.radio("Select an example or upload your own image", ["upload", "example"])

    if image_type == "upload":
        image_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])
        with st.columns(3)[1]:
            if image_file is not None:
                st.image(image_file, caption="Uploaded Image.", use_column_width=True, width=300)
            else:
                st.write("Please upload an Image file.")
    else:
        selected_example = st.selectbox("Select an example image:", list(example_images.keys()))
        image_file = example_images[selected_example]
        with st.columns(3)[1]:
            st.image(image_file, caption="Sample Image-1", use_column_width=True, width=300)

    if image_file :
        
        text_from_image = get_text_from_image(image_file)
        prompt = st.text_area("User input image to text:", value=text_from_image)

        if st.button("Submit") and prompt:
            new_claim_detection_pipeline(prompt)
            financial_points = financial_point_extractor(prompt)
            display_video_links(financial_points)

if selected == "QnA":
    st.write("**Question - Answering**")
    prompt = st.text_area("User Input")

    if st.button("Submit") and prompt:
        question_and_answer(prompt)

if selected == "VIDEO":
    st.write("**VIDEO BASED CLAIM DETECTION:**")
    example_videos = {
    "Sample Video 1": "media/demo_video.mp4"
    }
    mode = None
    video_type = st.radio("Select an example or upload your own video", ["upload", "example"])

    if video_type == "upload":
        mode="upload"
        video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
        with st.columns(3)[1]:
            if video_file is not None:
                st.video(video_file, start_time=0)
            else:
                st.write("Please upload an Video file.")
    else:
        mode="example"
        selected_example = st.selectbox("Select an example video:", list(example_videos.keys()))
        video_file = example_videos[selected_example]
        with st.columns(3)[1]:
            st.video(video_file, start_time=0)

    if video_file:
        
        #----------------------------------------
        transcript = video_to_text(video_file,mode)
        #----------------------------------------
        prompt = st.text_area("Transcribed User Input", value=transcript)
        
        if st.button("Submit") and prompt:
            new_claim_detection_pipeline(prompt)
            financial_points = financial_point_extractor(prompt)
            display_video_links(financial_points)
