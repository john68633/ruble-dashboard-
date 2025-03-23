import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import hashlib
import uuid

# ✅ 고정 비밀번호
PASSWORD = "jei_only"

# ✅ 등록된 PC/Mobile만 허용 (기기 ID 반드시 등록)
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",  # 👉 제이님 PC ID
]

# ✅ 현재 기기 고유값 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 인증
input_pwd = st.text_input("🔒 비밀번호를 입력하세요", type="password")
if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("✅ 인증에 성공했습니다!")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("📂 분석할 상가 리스트 파일을 업로드하세요 (.xlsx)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ✅ 지도 초기화 (첫 번째 매물 기준 중심)
    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    # ✅ 마커 추가
    for _, row in df.iterrows():
        name = row["단지"]
        lat = row["latitude"]
        lon = row["longitude"]
        desc = row["비고"]
        url = row["매물_URL"]
        
        popup_html = f"""
        <b>{name}</b><br>
        {desc}<br>
        <a href="{url}" target="_blank">매물 보기 🔗</a>
        """

        folium.Marker(
            location=[lat, lon],
            popup=popup_html,
            tooltip=name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # ✅ 지도 출력
    st_folium(m, width=800, height=600)

