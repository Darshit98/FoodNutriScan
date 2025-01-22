import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # loading all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image_parts):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

st.set_page_config(page_title="Calories Advisor App", layout="wide")

st.title("🥗 Gemini Food Nutri-Scan")
st.markdown("## Discover the nutritional value and calories in your meals")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("🔍 Analyze Calories")

input_prompt = """
You are an expert in Nutritionist where you need to see the food items from the image and need to calculate the total calories,
                also provide the details of every food item with calories intake in below format

                1. Item 1 - no of calories
                2. Item 2 - no of calories
                ----
                ----
            Finally you can also mention whether the food is healthy or not and also mention percentage split of the ratio of carbohydrates,
            fats, fibers, sugars, and other things required in our diet.
"""

if submit and uploaded_file is not None:
    with st.spinner('Analyzing...'):
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("📋 Nutritional Analysis")
        st.write(response)
        # st.markdown("""
        # ### 🥑 Nutritional Content:
        # - **Carbohydrates**: 55%
        # - **Fats**: 25%
        # - **Fibers**: 10%
        # - **Sugars**: 5%
        # - **Other**: 5%
        # """)
    st.balloons()

st.sidebar.title("📚 Nutrition Guide")
st.sidebar.info("Upload an image of your meal and the AI will analyze the nutritional content, including an estimate of the total calories.")
