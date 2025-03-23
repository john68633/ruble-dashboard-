import streamlit as st
import pandas as pd
import re
import folium
import hashlib
import uuid
from streamlit_folium import st_folium

# ✅ 고정 비밀번호
PASSWORD = "jei_only"

# ✅ 등록된 PC/Mobile만 허용
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9"  # 🖥️ 현재 기기 ID 반드시 이 리스트에 포함되어야 실행됨
]

# ✅ 현재 장치 고유값 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 인증
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")
if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()

# ✅ 접근 허용 후 실행될 본문 코드
st.success("인증에 성공했습니다!")

# 예시 코드
st.title("루블 상가 추천 대시보드")
# 여기에 본문 기능 추가

