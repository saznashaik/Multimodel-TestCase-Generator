from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to get a response from the Gemini model
def get_gemini_response(input, images, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, *images, prompt])  # Unpacking the list of images
    return response.text

## Function to process multiple image uploads
def input_image_setup(uploaded_files):
    image_parts = []
    for uploaded_file in uploaded_files:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts.append({
            "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
            "data": bytes_data
        })
    
    if image_parts:
        return image_parts
    else:
        raise FileNotFoundError("No files uploaded")

## Initialize the Streamlit app
st.set_page_config(page_title="Test Case Generator")

st.header("Multimodal Test Case Generator")

# Input context for the test cases
input_text = st.text_input("Optional Context for the Test Cases", key="input")

# Allow multiple image uploads
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display uploaded images
if uploaded_files and len(uploaded_files) > 0:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, use_column_width=True)

# Submit button for generating test cases
submit = st.button("Describe Testing Instructions")

if submit:
    if not uploaded_files or len(uploaded_files) == 0:
        st.error("Please upload at least one screenshot.")
    else:
        st.info("Generating test cases, please wait...")
        
        # Prompt for test case generation
        prompt = f"""
            Please generate detailed, step-by-step test cases for a mobile app based on the following screenshots and context: '{input_text}'. Each test case should include:
            - Description
            - Pre-conditions
            - Testing steps
            - Expected results
        """
        
        # Prepare the image data
        image_data = input_image_setup(uploaded_files)
        
        # Generate response using the Gemini model
        response = get_gemini_response(input_text, image_data, prompt)
        
        # Display the generated test cases
        if response:
            st.subheader("Generated Test Cases")
            st.write(response)
        else:
            st.error("Failed to generate test cases. Please try again.")
