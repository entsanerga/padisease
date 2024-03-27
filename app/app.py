# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="padisease",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Deteksi Penyakit pada Tanaman Padi")
st.text("Halo! website ini dirancang untuk membantu anda mengidentifikasi penyakit pada tanaman padi🌿")

# Sidebar
st.sidebar.header("konfigurasi🪸")

# Model Options
model_type = st.sidebar.radio(
    "Goal:", ['Detection'])

confidence = float(st.sidebar.slider(
    "pilih tingkat confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"ada yang salah. cek path: {model_path}")
    st.error(ex)

st.sidebar.header("input visual 🤖(gambar/kamera)")
source_radio = st.sidebar.radio(
    "pilih sumber", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "pilih gambar...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="contoh gambar",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="gambar input anda",
                         use_column_width=True)
        except Exception as ex:
            st.error("error hehe sorry.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='hasil deteksi',
                     use_column_width=True)
        else:
            if st.sidebar.button('Deteksi Penyakit'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='hasil identifikasi',
                         use_column_width=True)
                try:
                    with st.expander("detail"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("belum ada gambar dimasukkan!")

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

else:
    st.error("yang bener bang")
