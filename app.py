import streamlit as st
from PIL import Image

def add_selfie_to_template(selfie, template_path, output_path):
    try:
        template = Image.open('PnbONE_Template.jpg')

        box_x, box_y = 462, 450  # Top-left corner coordinates of the white box
        box_width, box_height = 490, 500  # Dimensions of the white box
        selfie = selfie.resize((box_width, box_height))

        template.paste(selfie, (box_x, box_y))

        template.save()
        st.success(f"Image saved to {output_path}")

    except FileNotFoundError:
        st.error(f"Error: Template image file not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title('Selfie to Template Adder')

uploaded_selfie = st.file_uploader("Upload your selfie", type=["jpg", "jpeg", "png"])

if uploaded_selfie is not None:
    selfie_image = Image.open(uploaded_selfie)
    template_image_path = 'PnbONE_Template.jpg'  # Path to your template image
    output_image_path = 'output.jpg'  # Desired output path

    if st.button("Add Selfie to Template"):
        add_selfie_to_template(selfie_image, template_image_path, output_image_path)
