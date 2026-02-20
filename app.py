import streamlit as st
from PIL import Image
import io
import os
import openai

# -----------------------
# OpenAI Configuration
# -----------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="AI Real Estate Image Enhancer", layout="wide")
st.title("🏡 AI Real Estate Image Enhancer")
st.markdown("""
Enhance property images using AI:
- **Lighting correction**  
- **Object removal**  
- **Virtual staging**
""")

# Image uploader
uploaded_file = st.file_uploader("Upload property image", type=["jpg", "png"])
enhance_options = st.multiselect(
    "Select enhancement options",
    ["Lighting Correction", "Object Removal", "Virtual Staging"]
)

if st.button("Enhance Image") and uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    st.info("Enhancing image with AI...")

    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    # Prepare prompt for AI
    prompt_text = "Enhance this real estate image with: " + ", ".join(enhance_options)

    try:
        # Call OpenAI DALL·E Edit API
        response = openai.Image.create_edit(
            image=io.BytesIO(img_bytes),
            prompt=prompt_text,
            n=1,
            size="1024x1024"
        )
        enhanced_url = response['data'][0]['url']
        st.success("✅ Image enhanced successfully!")
        st.image(enhanced_url, caption="Enhanced Image", use_column_width=True)
        st.markdown(f"[Download Enhanced Image]({enhanced_url})")
    except Exception as e:
        st.error(f"Error enhancing image: {e}")
