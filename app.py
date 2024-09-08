# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Test Case Generator")

st.header("Multimodal Test Case Generator")
input=st.text_input("Optional Context for the Test Cases",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
submit = st.button("Describe Testing Instructions")
if submit:
    if not uploaded_file:
        st.error("Please upload at least one screenshot.")
    else:
        st.info("Generating test cases, please wait...")
        prompt = f"""
            Please generate detailed, step-by-step test cases for a mobile app based on the following screenshots and context: '{input}'. Each test case should include:
            - Description
            - Pre-conditions
            - Testing steps
            - Expected results
           """
        
        image_data = input_image_setup(uploaded_file)
        response=get_gemini_response(prompt,image_data,input)
        
        if response:
            st.subheader("Generated Test Cases")
            st.write(response)
        else:
            st.error("Failed to generate test cases. Please try again.")
