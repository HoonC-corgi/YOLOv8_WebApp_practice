---------------------------------------------preSet---------------------------------------------
# 터미널에서 가상환경 생성
$ conda create --가상환경명
# 가상환경 연결
$ conda activate --가상환경명

# 필수 패키지 설치
$ pip install ultralytics
$ pip install streamlit
$ pip install pafy
$ pip install pytube

*no module "패키지 이름"과 같은 오류가 추가적으로 발생한다면
위와 같은 방식으로 $ pip install "패키지 이름"을 통해 설치

---------------------------------------------실행---------------------------------------------
# 가상환경 연결
$ conda activate --가상환경명
# 실행
$ streamlit run ./app.py

---------------------------------------------설정---------------------------------------------
소스의 video 1-5까지의 비디오를 변경하고 싶을 시
settings.py의 # Videos config에 정의되어 있는 VIDEO_PATH를 대상 비디오의 절대 경로로 변경

소스의 웹캠을 외장 카메라로 변경하고 싶을 시
settings.py의 # Webcam에 정의되어 있는 WEBCAM_PATH = 0을 1로 변경

