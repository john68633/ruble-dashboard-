import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import uuid, hashlib

# ---------------------- 보안 인증 ----------------------
PASSWORD = "jei_only"
allowed_ids = ["c2cf7a8a6dd95e6e4f6c8f7b03b515f9"]

device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("인증에 성공했습니다!")

# ---------------------- 제목 ----------------------
st.title("🏪 루블 상가 추천 대시보드")

# ---------------------- 파일 업로드 ----------------------
file = st.file_uploader("매물 엑셀 파일을 업로드하세요", type=["xlsx"])
if file is not None:
    df = pd.read_excel(file)

    # ---------------- 지도 그리기 ----------------
    st.subheader("📍 매물 지도 시각화")
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=15)

    for _, row in df.iterrows():
        popup_text = f"<b>{row['단지']}</b><br>{row['현재업종']}<br>{row['비고']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text,
            tooltip="매물 보기",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    st_folium(m, width=700, height=500)

    # ---------------- 매물 표시 ----------------
    st.subheader("📋 매물 리스트 및 요약")

    def evaluate_row(row):
        score = 0
        if row['수익률'] >= 6:
            score += 2
        elif row['수익률'] >= 4:
            score += 1

        if '역세권' in str(row['비고']):
            score += 2
        if row['전용평'] >= 30:
            score += 1
        return score

    df['추천점수'] = df.apply(evaluate_row, axis=1)
    df_sorted = df.sort_values(by='추천점수', ascending=False)

    st.dataframe(df_sorted[['단지', '전용평', '매매가', '월세', '수익률', '현재업종', '비고', '추천점수']])
