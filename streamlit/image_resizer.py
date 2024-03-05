import streamlit as st
import logging

from PIL import Image
from io import BytesIO
from datetime import datetime

#setting up the application logger to log necessary information 
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

st.title('Dynamic Image resizer')
#mark down to create horizontal line
st.markdown('---')

def load_image(img, resizing_factor = None):
    '''
    Streamlit convert image to nd array while uploading, we need convert it back to
    byteIO to resize it and display on frontend UI. If resizing factor is None
    it will return image as it is else function will resize the image and return it.

    :param img: image - uploaded from front end of type numpy nd array
    :param resizing_factor: user provided input captured from form range between 10 to 100 %

    :returns: image as byteIO
    '''
    im = Image.open(img)
    if resizing_factor:
        #calculating resized width and height based on resizing factor
        width  = int((im.width * resizing_factor) / 100)
        height = int((im.height * resizing_factor) / 100)
        resized_im = im.resize((width, height))
    else:
        return im 
    return resized_im


with st.form("my_form"):
    '''
    Form supports multiple image upload along with resizing factor value ranging between 10 - 200%
    '''
    img_u = st.file_uploader("Select image to resize",
                     type=['apng', 'avif', 'gif', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'svg', 'webp'],
                     accept_multiple_files=True,
                     key="image_u",
                     help=None,
                     on_change=None,
                     args=None,
                     kwargs=None, disabled=False, label_visibility="visible")
    resizing_factor = st.slider("select resizing factor %",
                      min_value= 10,max_value= 200, key="image_w")
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        logging.info(f'Request received to resize images by {resizing_factor}%')
        start_time = datetime.utcnow()
        for i ,img in enumerate(img_u):
            #To display original and re-sized image side by side columns are used
            col1, col2 = st.columns(2)
            with col1:
                st.header("Original Image")
                bytes_data = Image.open(img)
                st.image(bytes_data, caption="Original image")
            with col2:
                st.header("Resized Image")
                img_r = load_image(img, resizing_factor)
                resized = st.image(img_r, caption="Resized image")
                with BytesIO() as buffer:
                    img_r.save(buffer, format="PNG")
                    byte_data = buffer.getvalue()
                st.download_button(
                    label="Download resized Image",
                    data=byte_data,
                    file_name=f'my{i}.png',
                    mime='image/png',
                    key=f"img-{i}"
                )
        end_time = datetime.utcnow()
        logging.info(f"Total time take to process image resizing request - {(end_time-start_time).total_seconds()}s")
    except Exception as ex:
        logging.error(f"Image processing failed - Error - {ex}")
