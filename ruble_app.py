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
allowed_ids = ["b2e0f2c8814ff5d04db73f2fc2972959"]  # 여기에 등록된 장비 ID만 허용

# ✅ 현재 장치 고유값 가져오기
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 인증
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")
if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()

# ✅ 앱 본문 시작
st.set_page_config(page_title="루블 상가 추천 대시보드", layout="wide")
uploaded_file = st.file_uploader("상가 매물 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df[["단지", "건물유형", "층", "매매가", "비고", "부동산", "latitude", "longitude", "매물_URL"]].copy()

    def parse_price(val):
        if pd.isna(val): return None
        val = str(val).replace(',', '')
        match = re.search(r'(\d+)억\s*(\d+)?', val)
        if match:
            억 = int(match.group(1))
            천 = int(match.group(2)) if match.group(2) else 0
            return 억 * 10000 + 천
        return int(re.sub(r'\D', '', val))

    def extract_yield(text):
        if pd.isna(text): return None
        match = re.search(r'연\s?(\d+(\.\d+)?)', text)
        if match:
            return float(match.group(1))
        return None

    def lubble_score(row):
        score = 50
        if row["추정_수익률(%)"] and row["추정_수익률(%)"] >= 6.0:
            score += 20
        if str(row["층"]) == "1":
            score += 20
        if "복합상가" in str(row["건물유형"]):
            score += 10
        return score

    df["매매가_만원"] = df["매매가"].apply(parse_price)
    df["추정_수익률(%)"] = df["비고"].apply(extract_yield)
    df["루블점수"] = df.apply(lubble_score, axis=1)
    df = df.sort_values(by="루블점수", ascending=False).reset_index(drop=True)

    st.title("📊 루블식 상가 추천 대시보드")
    st.markdown("### 📍 지도 기반 추천 상가 보기")

    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            tooltip=f"{row['단지']} | {row['매매가']} | 루블 {row['루블점수']}점",
            popup=folium.Popup(f'<a href="{row["매물_URL"]}" target="_blank">매물 상세 보기</a>', max_width=200)
        ).add_to(m)

    st_folium(m, width=700, height=500)

    st.markdown("---")
    st.markdown("### 📝 추천 매물 리스트")

    for idx, row in df.iterrows():
        with st.container():
            st.markdown(f"**{row['단지']}** | {row['건물유형']} | {row['층']}층")
            st.markdown(f"- 매매가: {row['매매가']}")
            st.markdown(f"- 추정 수익률: {row['추정_수익률(%)']}%")
            st.markdown(f"- 부동산: {row['부동산']}")
            st.markdown(f"- **루블 점수**: {row['루블점수']}점")
            st.markdown(f"[매물 링크 바로가기]({row['매물_URL']})")
            st.markdown("---")
