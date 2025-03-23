import streamlit as st
import hashlib, uuid

# ✅ 고정 비밀번호
PASSWORD = "jei_only"

# ✅ 허용된 기기 고유 해시값 목록 (PC, 모바일 각각 추가 가능)
ALLOWED_DEVICE_HASHES = [
    "b2e0f2c8814f5d040db73f2fc2972959",  # john6 PC
    # "모바일 해시값도 여기에 추가 가능"
]

# ✅ 현재 기기 고유값 확인
device_id = hashlib.md5(uuid.getnode().to_bytes(6, 'big')).hexdigest()

# ✅ 로그인 체크
input_pwd = st.text_input("비밀번호를 입력하세요", type="password")
if input_pwd != PASSWORD:
    st.warning("비밀번호가 틀렸습니다.")
    st.stop()

# ✅ 기기 인증 체크
if device_id not in ALLOWED_DEVICE_HASHES:
    st.error("허용되지 않은 기기입니다. 접근이 차단되었습니다.")
    st.stop()

# 🔓 여기부터는 인증된 사용자만 접근 가능
st.success("접속 승인됨. 대시보드 시작합니다!")

# 🎯 여기에 본문 코드 삽입
