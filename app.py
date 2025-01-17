import streamlit as st
from PIL import Image, ExifTags
import io

def correct_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            exif = dict(exif.items())
            orientation = exif.get(orientation, None)

            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
    return image

def add_selfie_to_template(selfie, template_path, output_path):
    try:
        template = Image.open('PnbONE_Teamplate.jpg')

        box_x, box_y = 462, 450  # Top-left corner coordinates of the white box
        box_width, box_height = 490, 500  # Dimensions of the white box

        # Correct orientation of the selfie
        selfie = correct_orientation(selfie)
        selfie = selfie.resize((box_width, box_height))

        template.paste(selfie, (box_x, box_y))

        # Save the combined image
        template.save(output_path)
        st.success(f"Image saved to {output_path}")

    except FileNotFoundError:
        st.error(f"Error: Template image file not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title('Selfie to Template Adder')

if 'uploaded_selfie' not in st.session_state:
    st.session_state.uploaded_selfie = None

uploaded_selfie = st.file_uploader("Upload your selfie", type=["jpg", "jpeg", "png"])

if uploaded_selfie is not None:
    st.session_state.uploaded_selfie = uploaded_selfie
    st.image(uploaded_selfie, caption='Uploaded Selfie', use_column_width=True)

if st.session_state.uploaded_selfie is not None and st.button("Add Selfie to Template"):
    selfie_image = Image.open(st.session_state.uploaded_selfie)
    output_image_path = 'output.jpg'  # Desired output path

    add_selfie_to_template(selfie_image, 'PnbONE_Template.jpg', output_image_path)

    with open(output_image_path, "rb") as file:
        btn = st.download_button(
            label="Download Combined Image",
            data=file,
            file_name="combined_image.jpg",
            mime="image/jpeg"
        )
    st.image(output_image_path, caption='Combined Image', use_column_width=True)
