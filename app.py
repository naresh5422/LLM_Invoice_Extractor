from dotenv import load_dotenv

load_dotenv() # load all the environment variable

import streamlit as st
import os
from PIL import Image
import  google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision

model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def details_for_input_image(uploaded_file):
    if uploaded_file is not None:
        # read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [{
            "mime_type": uploaded_file.type, # to get the uploaded file type of mime
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No File is Uploaded")
    





# Initialize the streamlit setup for app
st.set_page_config(page_title="Demo for invoice extracter")
st.header("details about Invoice App")
input = st.text_input("Input_Prompt: ", key="input")
uploaded_file =st.file_uploader("Choose an image...", type=["jpg","jpeg","png", "webp"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Completed image uploading", use_column_width=True)


submit = st.button("Give me details for given query in Invoice")

input_prompt = """

We will upload an image as invoices, i know the your the expert in giving the info
So you will definitly give me answer for my question"""

## If submit button clicked

if submit:
    image_data = details_for_input_image(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Reply is:")
    st.write(response)

