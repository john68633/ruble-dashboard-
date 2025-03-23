import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import uuid, hashlib

# ✅ 고정 비밀번호
PASSWORD = "jei_only"

# ✅ 등록된 PC/Mobile 기기 ID
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9"  # ← 여기에 반드시 현재 기기 ID 포함돼야 함
]

# ✅ 현재 기기 고유값 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 인증 입력
st.markdown("🔐 비밀번호를 입력하세요")
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("인증에 성공했습니다! ✅")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("엑셀 매물 파일을 업로드하세요", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # 지도 초기 위치 설정
    map_center = [df["위도"].mean(), df["경도"].mean()]
    m = folium.Map(location=map_center, zoom_start=16)

    # 지도에 마커 추가
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=f"<b>{row['상가명']}</b><br>가격: {row['매매가']}<br>면적: {row['면적']}㎡<br><a href='{row['링크']}' target='_blank'>매물 보기</a>",
            tooltip=row["상가명"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    st_folium(m, width=800, height=600)

    # ⬇️ 지도 아래 매물 정보 표로 보여주기
    st.markdown("### 📋 업로드된 매물 정보")
    st.dataframe(df)
