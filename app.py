import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv() #loading all the environment variables
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,Image):
    model_name = "gemini-1.5-flash"  # Updated model name
    model=genai.GenerativeModel(model_name)
    response=model.generate_content([input_prompt,Image[0]])
    return response.text

def input_image_setup(uploaded_file):
    #Check if a file has been uploaded
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, #get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")
    

# initializing streamlit app
    
st.set_page_config(page_title="Calories Advisor App")

st.header("Gemini Health App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.", use_container_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in Nutritionist where you need to see the food items from the image and need to calculate the total calories,
                also provide the details of every food item with calories intake in below format

                1. Item 1 - no of calories
                2. Item 2 - no of calories
                ----
                ----
            Finally you can also mention whether the food is healthy or not and also mention percentage split of the ratio of carbohydrates,
            fats, fibers, sugars, and other things required in our diet

            
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The response is")
    st.write(response)