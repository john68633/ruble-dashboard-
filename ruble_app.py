import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import uuid, hashlib

# ✅ 설정
PASSWORD = "jei_only"
allowed_ids = ["c2cf7a8a6dd95e6e4f6c8f7b03b515f9"]  # 제이 기기 ID

# ✅ 현재 기기 ID 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 인증 처리
st.markdown("### 🔐 비밀번호를 입력하세요")
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")

if input_pwd == PASSWORD and device_id in allowed_ids:
    st.success("인증에 성공했습니다! ✅")

    # ✅ 파일 업로드
    st.markdown("### 📂 엑셀파일 업로드")
    uploaded_file = st.file_uploader("Drag and drop file here", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # ✅ 열 이름 확인 출력
        st.write("🧾 데이터 열 이름:", df.columns.tolist())

        # ✅ 위도/경도 컬럼 존재 여부 확인
        if "위도" in df.columns and "경도" in df.columns:
            center = [df["위도"].mean(), df["경도"].mean()]
            m = folium.Map(location=center, zoom_start=16)

            for _, row in df.iterrows():
                folium.Marker(
                    location=[row["위도"], row["경도"]],
                    tooltip=row.get("상호명", "매물"),
                    popup=row.get("비고", "정보 없음"),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)

            st_folium(m, width=700, height=500)

            # ✅ 지도 아래 매물 리스트 표출
            st.markdown("### 📋 매물 정보")
            st.dataframe(df)

        else:
            st.error("❌ '위도'와 '경도' 컬럼이 존재하지 않습니다.\n엑셀 열 이름을 확인해주세요.")

else:
    st.warning("접근 권한이 없습니다.")
