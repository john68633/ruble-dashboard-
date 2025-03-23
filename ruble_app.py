import streamlit as st
import uuid, hashlib
import pandas as pd
import folium
from streamlit_folium import st_folium

# -----------------------------
# ✅ 1. 인증: 비밀번호 + 기기 ID 제한
# -----------------------------
PASSWORD = "jei_only"
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",  # 기존 등록된 PC
    "5f3eafdfdec9e92337a1cb731c650a86",  # 추가 기기 1
    "314ac74caaf70fc9ff885afed82a880d",  # ✅ 지금 접속한 기기
]

device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()
st.write("💻 현재 기기 ID:", device_id)

input_pwd = st.text_input("🔐 비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("인증에 성공했습니다!")

# -----------------------------
# ✅ 2. 엑셀 업로드
# -----------------------------
st.header("📂 엑셀파일 업로드")
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # -----------------------------
        # ✅ 3. 지도 시각화
        # -----------------------------
        st.subheader("📍 매물 지도 시각화")

        # 위도 경도 평균값으로 지도 중심 설정
        center_lat = df["위도"].mean()
        center_lon = df["경도"].mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

        for i, row in df.iterrows():
            name = row.get("이름", "매물")
            price = row.get("가격", "")
            info = row.get("평가", "")

            popup_text = f"{name}<br>💰 {price}<br>📊 {info}"
            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip=name,
                popup=popup_text,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        st_folium(m, width=700, height=500)

        # -----------------------------
        # ✅ 4. 매물 평가 테이블 출력
        # -----------------------------
        st.subheader("📄 매물 평가표 보기")
        st.dataframe(df)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
