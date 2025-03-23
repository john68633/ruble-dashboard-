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
    "c2cf7a8a6dd95e6e4f6c8f7b03b515f9",
    "5f3eafdfdec9e92337a1cb731c650a86",
    "314ac74caaf70fc9ff885afed82a880d",
]

device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()
st.write("💻 현재 기기 ID:", device_id)

input_pwd = st.text_input("🔐 비밀번호를 입력하세요", type="password")

if input_pwd != PASSWORD or device_id not in allowed_ids:
    st.warning("접근 권한이 없습니다.")
    st.stop()
else:
    st.success("✅ 인증에 성공했습니다!")

# -----------------------------
# ✅ 2. 엑셀 업로드
# -----------------------------
st.header("📂 엘셀파일 업로드")
uploaded_file = st.file_uploader("엘셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # -----------------------------
        # ✅ 3. 컬럼명 정리 (한글/영문 대응)
        # -----------------------------
        df.columns = df.columns.str.strip().str.replace(" ", "")
        col_map = {
            '위도': '위도', 'latitude': '위도',
            '경도': '경도', 'longitude': '경도',
            '이름': '이름', 'name': '이름',
            '가격': '매매가', 'price': '매매가',
            '전용면적(평)': '전용평', 'area': '전용평',
            '수익률': '수익률', 'rate': '수익률',
            '보증금': '보증금', 'deposit': '보증금',
            '월세': '월세', 'monthly': '월세'
        }
        df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

        # -----------------------------
        # ✅ 4. 수익률 및 평가 점수 계산 함수
        # -----------------------------
        def calculate_score(row):
            score = 0

            # 수익률 계산 (환산월세 기준)
            try:
                total_price = row.get("매매가", 0)
                monthly_rent = row.get("월세", 0)
                deposit = row.get("보증금", 0)
                if total_price > 0:
                    monthly_income = monthly_rent + (deposit * 0.04 / 12)
                    row["수익률"] = round((monthly_income * 12) / total_price * 100, 1)
                else:
                    row["수익률"] = 0
            except:
                row["수익률"] = 0

            # 수익률 점수
            if row["수익률"] >= 6:
                score += 40
            elif row["수익률"] >= 3:
                score += 25
            else:
                score += 10

            # 매매가 점수
            if row.get("매매가", 999999) <= 10000:
                score += 30
            elif row.get("매매가", 999999) <= 20000:
                score += 20
            else:
                score += 10

            # 전용평 점수
            if row.get("전용평", 0) >= 8:
                score += 20
            elif row.get("전용평", 0) >= 5:
                score += 10

            return pd.Series([row["수익률"], score])

        df[["수익률", "평가점수"]] = df.apply(calculate_score, axis=1)

        # -----------------------------
        # ✅ 5. 지도 시각화
        # -----------------------------
        st.subheader("📍 매무 지도 시각화")
        center_lat = df["위도"].mean()
        center_lon = df["경도"].mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

        for _, row in df.iterrows():
            name = row.get("이름", "매물")
            price = row.get("매매가", "")
            score = row.get("평가점수", "")
            popup_text = f"{name}<br>💰 {price}만<br>🔢 점수: {score}점"

            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip=name,
                popup=popup_text,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        st_folium(m, width=700, height=500)

        # -----------------------------
        # ✅ 6. 매물 평가표
        # -----------------------------
        st.subheader("📄 매무 평가표 보기")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
