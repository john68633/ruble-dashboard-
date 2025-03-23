import streamlit as st
import pandas as pd
import folium
import re
import uuid
import hashlib
from streamlit_folium import st_folium

# ✅ 고정 비밀번호
PASSWORD = "jei_only"

# ✅ 등록된 PC/Mobile만 허용
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",  # 제이 PC
    # 외부 사용자 기기 ID는 여기에 추가
]

# ✅ 현재 장치 고유값 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 비밀번호 입력
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")

# ✅ 인증
if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.markdown(f"🖥️ 현재 기기 ID: `{device_id}`")
    st.info("👉 위 기기 ID를 제이에게 전달해 주세요.")
    st.stop()
else:
    st.success("인증에 성공했습니다! 🎉")

# ✅ 본문 시작 --------------------------------------------------
st.markdown("## 💡 루블 상가 추천 대시보드")

# ✅ 엑셀 업로드
uploaded_file = st.file_uploader("상가 매물 엑셀 파일 업로드", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # 예시: 지도로 시각화
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
    for idx, row in df.iterrows():
        if '위도' in row and '경도' in row:
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=row.get('매물명', '상세정보 없음')
            ).add_to(m)

    st_folium(m, width=700, height=500)
