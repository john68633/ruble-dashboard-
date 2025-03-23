import streamlit as st
import pandas as pd
import re
import folium
from streamlit_folium import st_folium
import uuid
import hashlib

# ✅ 고정 비밀번호
PASSWORD = "jei_only"

# ✅ 현재 기기 고유 ID 구하기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 허용된 기기 리스트 (이 리스트 안에 있어야 실행 가능)
# 👉 현재 접속 기기 ID도 자동으로 포함되도록 설정
allowed_ids = [
    "5f3eafdfdec9e92337a1cb731c650a86",  # 예시 등록 기기
    device_id  # 현재 접속 중인 기기 자동 등록
]

# ✅ 현재 기기 ID 표시 (개발 시 확인용)
st.write("🖥️ 현재 기기 ID:", device_id)

# ✅ 인증 (비밀번호 + 기기 확인)
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()

# 🔓 인증 완료 후 실행되는 대시보드 본문
st.success("접근 권한 확인 완료! 대시보드를 시작합니다.")
st.title("루블 상가 추천 대시보드")

uploaded_file = st.file_uploader("상가 매물 엑셀 파일 업로드", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

