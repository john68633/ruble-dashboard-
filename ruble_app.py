import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import uuid, hashlib

# ✅ 비밀번호
PASSWORD = "jei_only"

# ✅ 기기 인증용 현재 기기 ID
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 여기에 👇 본인 기기 ID를 넣어야 함 (예: "c2cf7a8a6dd95e6e4f6c8f7b03b515f9")
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",   # 예시: 제이의 PC
    device_id  # ← 이걸 넣어두면 실행 중 기기 자동 포함됨 (개발용)
]

# ✅ 인증
st.markdown("🔐 비밀번호를 입력하세요")
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("인증에 성공했습니다!")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("📂 엑셀 파일 업로드", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 지도 중앙
    center = [df["위도"].mean(), df["경도"].mean()]
    m = folium.Map(location=center, zoom_start=16)

    # 마커 추가
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            tooltip=row["상가명"],
            popup=f"<b>{row['상가명']}</b><br>면적: {row['면적']}㎡<br>매매가: {row['매매가']}<br><a href='{row['링크']}' target='_blank'>매물 보기</a>",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    st_folium(m, width=800, height=600)
    st.markdown("### 📋 매물 리스트")
    st.dataframe(df)

