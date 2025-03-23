
   import streamlit as st
import hashlib

# ✔️ 비밀번호 설정
PASSWORD = "jei_only"

# ✔️ Streamlit 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "device_id" not in st.session_state:
    st.session_state["device_id"] = None

# ✔️ 허용된 기기 해시값 목록 (PC 1대 + 모바일 1대만 등록)
# 실제 운영 시, 이 값은 서버 DB에서 관리해야 더 안전함
# ➤ 예시로 'john_pc'와 'john_mobile'의 해시값만 허용
ALLOWED_DEVICE_HASHES = [
    "e1faffb3e614e6c2fba74296962386b7",  # 예: john_pc
    "912ec803b2ce49e4a541068d495ab570"   # 예: john_mobile
]

# ✔️ 기기 ID를 생성하는 함수 (브라우저 정보 기반)
def generate_device_id():
    # Streamlit에서 직접 기기 정보 가져오기 어려움
    # ➤ 사용자에게 '기기 이름'을 한 번 입력받고 그걸 해시로 사용
    return st.text_input("기기 등록 이름 (예: john_pc 또는 john_mobile)").strip()

# ✔️ 비밀번호 입력
if not st.session_state["authenticated"]:
    input_pwd = st.text_input("비밀번호를 입력하세요", type="password")
    if input_pwd == PASSWORD:
        st.session_state["authenticated"] = True
        st.success("비밀번호 인증 완료 ✅")
    else:
        st.stop()

# ✔️ 기기 인증
if st.session_state["authenticated"]:
    if not st.session_state["device_id"]:
        input_device_name = generate_device_id()

        if input_device_name:
            device_hash = hashlib.md5(input_device_name.encode()).hexdigest()
            st.session_state["device_id"] = device_hash

            if device_hash in ALLOWED_DEVICE_HASHES:
                st.success("접속 기기 인증 완료 ✅")
            else:
                st.error("등록되지 않은 기기입니다 ❌")
                st.stop()
    else:
        if st.session_state["device_id"] not in ALLOWED_DEVICE_HASHES:
            st.error("등록되지 않은 기기입니다 ❌")
            st.stop()

# ✔️ 여기부터 본문 내용
st.title("🎉 루블 상가 추천 대시보드")
st.write("지정된 사용자만 접근 가능한 보안 페이지입니다.")
