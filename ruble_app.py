import streamlit as st
import pandas as pd
import hashlib, uuid
import folium
from streamlit_folium import st_folium

# ✅ 인증 설정
PASSWORD = "jei_only"
allowed_ids = ["c2cf7a8a6dd95e6e4f6c8f7b03b515f9"]  # 현재 PC ID

device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()
input_pwd = st.text_input("🔐 비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("인증에 성공했습니다! 🎉")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("📂 매물 파일을 업로드하세요 (.xlsx)", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ✅ 위도, 경도 있는 매물만 필터
    df = df.dropna(subset=['위도', '경도'])

    # ✅ 추천 점수 계산
    def get_score(row):
        score = 0
        if '대형주차장' in str(row['상세정보']): score += 1
        if '코너' in str(row['상세정보']): score += 1
        if '1층' in str(row['상세정보']): score += 1
        return score
    df['추천점수'] = df.apply(get_score, axis=1)

    # ✅ 지도에 마커 표시
    center = [df['위도'].mean(), df['경도'].mean()]
    m = folium.Map(location=center, zoom_start=16)
    for _, row in df.iterrows():
        popup = f"{row['상호명']}<br>추천점수: {row['추천점수']}<br><a href='{row['링크']}' target='_blank'>매물 보기</a>"
        folium.Marker(location=[row['위도'], row['경도']], popup=popup, tooltip=row['상호명']).add_to(m)
    st_folium(m, width=1000)

    # ✅ 매물 테이블 표시 (추천점수 높은 순)
    st.markdown("### 📋 추천 매물 리스트 (추천점수순 정렬)")
    st.dataframe(df[['상호명', '주소', '추천점수', '링크']].sort_values(by='추천점수', ascending=False))

