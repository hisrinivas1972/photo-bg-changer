import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import requests

# ----------------- Helper Function -----------------
def download_image(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        img.load()
        return img.convert("RGBA")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return None

# ----------------- Background Options -----------------
paths = {
    "In Stars": "https://images.unsplash.com/photo-1464802686167-b939a6910659?raw=true&fit=crop&w=1280",
    "Eiffel Tower": "https://images.pexels.com/photos/19610172/pexels-photo-19610172.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260",
    "Taj Mahal": "https://images.pexels.com/photos/3881104/pexels-photo-3881104.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260",
    "Eiffel Tower Oth": "https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260",
    "Machu Picchu": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Machu_Picchu%2C_Peru.jpg/1280px-Machu_Picchu%2C_Peru.jpg"
}

# ----------------- Custom CSS for Responsiveness -----------------
st.markdown("""
    <style>
    /* Stretch layout on small devices */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        h2 {
            font-size: 22px !important;
        }
        .stButton>button {
            width: 100%;
            font-size: 16px !important;
        }
        .stSelectbox label {
            font-size: 16px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Header -----------------
st.markdown("""
    <h2 style='text-align: center; font-size: 30px;'>
    🌟 Transform Your Photo with Iconic Places
    </h2>
""", unsafe_allow_html=True)

# ----------------- Background Selection -----------------
st.write("Choose a background for your photo:")
bg_name = st.selectbox("Select Background", list(paths.keys()))
bg = download_image(paths[bg_name])
if not bg:
    st.error("❌ Error loading background image.")
    st.stop()

# ----------------- File Upload -----------------
uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])
if uploaded_file:
    with st.spinner("Processing your image..."):
        try:
            fg_bytes = remove(uploaded_file.read())
            fg_full = Image.open(BytesIO(fg_bytes)).convert("RGBA")

            # Resize background to match foreground
            bg = bg.resize((fg_full.width, fg_full.height))

            # Resize foreground to 50% and paste centered
            fg_resized = fg_full.resize((fg_full.width // 2, fg_full.height // 2), Image.LANCZOS)
            x_offset = (bg.width - fg_resized.width) // 2
            y_offset = bg.height - fg_resized.height
            bg.paste(fg_resized, (x_offset, y_offset), fg_resized)

            # Show result
            st.image(bg, caption="Your Edited Photo", use_container_width=True)

            # Enable download
            buf = BytesIO()
            bg.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Download Edited Photo",
                data=byte_im,
                file_name="edited_photo.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ Failed to process image: {e}")
