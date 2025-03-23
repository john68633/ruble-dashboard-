import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import hashlib, uuid
# ✅ 비밀번호 & 허용된 기기 ID 목록
PASSWORD = "jei_only"
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",  # 기존 PC
    "5f3eafdfdec9e92337a1cb731c650a86",  # 이전 기기
    "314ac74caaf70fc9ff885afed82a880d"   # ✅ 새 기기 추가!
]

# ✅ 비밀번호 & 허용된 기기 ID 목록
PASSWORD = "jei_only"
allowed_ids = [
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",  # 예시: 제이의 PC
    "5f3eafdfdec9e92337a1cb731c650a86"   # 예시: 다른 인증된 기기 (추가)
]

# ✅ 현재 기기 ID 확인
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()
st.write("🖥️ 현재 기기 ID:", device_id)  # 👉 필요시 삭제해도 됨

# ✅ 비밀번호 입력
input_pwd = st.text_input("🔐 비밀번호를 입력하세요", type="password")

# ✅ 인증 조건 확인
if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("인증에 성공했습니다! ✅")

# --------------------------------------
# ✅ 인증 완료 후 앱 본문 시작
# --------------------------------------

st.header("📂 엑셀파일 업로드")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # 위도/경도 평균으로 중심 위치 설정
    try:
        center = [df["위도"].mean(), df["경도"].mean()]
    except KeyError:
        st.error("❌ 엑셀 파일에 '위도' 또는 '경도' 컬럼이 없습니다.")
        st.stop()

    # 지도 생성
    m = folium.Map(location=center, zoom_start=15)

    # 마커 추가
    for idx, row in df.iterrows():
        popup_html = f"""
        <b>{row.get('매물명', '정보 없음')}</b><br>
        유형: {row.get('유형', '')}<br>
        가격: {row.get('금액', '')}<br>
        ⛳ <a href='{row.get('링크', '#')}' target='_blank'>매물보기</a>
        """
        folium.Marker(
            [row["위도"], row["경도"]],
            popup=popup_html,
            tooltip=row.get("매물명", "매물")
        ).add_to(m)

    # 지도 출력
    st_data = st_folium(m, width=900, height=600)

    # 📊 매물 정보 요약 표
    st.subheader("📋 업로드한 매물 목록")
    st.dataframe(df)
