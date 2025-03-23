
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
allowed_ids = ["5f3eafdfdec9e92337a1cb731c650a86"]

# ✅ 현재 장치 고유값 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 인증
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")
if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()

# ✅ 위 인증 통과 시, 여기 아래부터 본문 실행
st.success("접속 성공!")
# 여기에 앱 본문 로직 넣으시면 됩니다.
