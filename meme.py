# Required Libraries: pip install streamlit openai pillow requests

import streamlit as st
import openai
import base64
import os
import requests
from PIL import Image
from io import BytesIO

# ---------------------
# OpenAI API Key
# ---------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your API key in environment variable or Streamlit secrets

# ---------------------
# Streamlit App
# ---------------------
st.set_page_config(page_title="AI Meme Generator", layout="centered")
st.title("AI Meme Generator 🤖🎉")

# Upload user image
uploaded_file = st.file_uploader("Upload your photo", type=["png", "jpg", "jpeg"])

# Meme template selection
template = st.selectbox("Choose Meme Template", ["Funny", "Sarcastic", "School Joke", "Teacher Joke"])

# Generate Meme Button
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Photo", use_column_width=True)

    if st.button("Generate Meme"):
        with st.spinner("Generating your meme... ⏳"):
            # Convert image to base64
            img_bytes = uploaded_file.read()
            img_b64 = base64.b64encode(img_bytes).decode()

            # Create prompt for OpenAI
            prompt = f"Create a {template} meme using this image in base64 format: {img_b64}. Make it funny with short text."

            try:
                # Generate meme image using OpenAI Image API
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                meme_url = response['data'][0]['url']

                # Display generated meme
                response_img = requests.get(meme_url)
                img = Image.open(BytesIO(response_img.content))
                st.image(img, caption="Your AI Meme", use_column_width=True)

            except Exception as e:
                st.error(f"Error generating meme: {e}")

# ---------------------
# Pricing / Membership UI
# ---------------------
st.markdown("---")
st.subheader("Premium Membership 💎")
st.write("Monthly: ₹149 | Yearly: ₹999")
st.write("Subscribe to generate unlimited memes!")
