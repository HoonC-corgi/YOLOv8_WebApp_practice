# Python In-built packages
from pathlib import Path
from PIL import Image

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="홀로렌즈와 YOLOv8 알고리즘을 이용한 건축물 균열 검출",
    page_icon='/Users/gimseonghun/PycharmProjects/yolov8WebApp/images/ARMedia_logo.png',
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("홀로렌즈와 YOLOv8 알고리즘을 이용한 건축물 균열 검출")

# Sidebar
st.sidebar.header("모델 선택")

# Model Options
model_type = st.sidebar.radio(
    "Task 선택", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "예측 정확도 임계치", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video 타입 선택")
source_radio = st.sidebar.radio(
    "소스 선택", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "이미지 파일 선택", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = Image.open(default_image_path)
                st.image(default_image_path, caption="기본 이미지",
                         use_column_width=True)
            else:
                uploaded_image = Image.open(source_img)
                st.image(source_img, caption="업로드된 이미지",
                         use_column_width=True)
        except Exception as ex:
            st.error("파일 열기 중 오류 발생.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='검출된 이미지',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='검출된 이미지',
                         use_column_width=True)
                try:
                    with st.expander("검출 결과"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("이미지 업로딩 중")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("잘못된 확장자를 가지는 소스 파일")