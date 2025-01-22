import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # loading all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def calculate_bmi(weight, height):
    return weight / (height/100) ** 2

def get_gemini_response(input_prompt, image_parts, bmi):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_parts[0], {"bmi": bmi}])
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

st.title("🥗 Gemini Health App")
st.markdown("## Discover the nutritional value and calories in your meals")

age = st.number_input("Enter your age", min_value=0, step=1)
height = st.number_input("Enter your height (in cm)", min_value=0.0, step=0.5)
weight = st.number_input("Enter your weight (in kg)", min_value=0.0, step=0.5)
bmi = calculate_bmi(weight, height) if height and weight else 0

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
Finally, mention whether the food is healthy or not and provide a percentage split of the nutritional content, including carbohydrates, fats, fibers, sugars, and others.
"""

if submit and uploaded_file is not None and bmi:
    with st.spinner('Analyzing...'):
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, bmi)
        st.subheader("📋 Nutritional Analysis")
        st.write(response)
        st.markdown(f"Your BMI is: **{bmi:.2f}**")
    st.balloons()

st.sidebar.title("📚 Nutrition Guide")
st.sidebar.info("Upload an image of your meal, and the AI will analyze the nutritional content, including an estimate of the total calories.")
