import streamlit as st

# 1. 페이지 및 상태 초기화 (데이터베이스 역할)
st.set_page_config(page_title="KAIF 2026", layout="centered")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'db_data' not in st.session_state:
    st.session_state.db_data = []

# 2. 커스텀 CSS (이전 디자인 유지)
st.markdown("""
<style>
    .stApp { background-color: #070B19; color: white; }
    .main-title { font-size: 34px; font-weight: 900; line-height: 1.1; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. 상단 헤더 및 [이메일 로그인] 시스템 구현
col1, col2 = st.columns([2.5, 1.5])
with col1:
    st.markdown('<div class="main-title">KOREA-ASEAN<br>INTERNATIONAL FORUM<br>OF LOGISTICS</div>', unsafe_allow_html=True)
with col2:
    if not st.session_state.logged_in:
        login_email = st.text_input("이메일로 시작하기", placeholder="example@gmail.com")
        if st.button("Log In 👤"):
            if login_email:
                st.session_state.logged_in = True
                st.session_state.current_user = login_email
                st.rerun()
            else:
                st.warning("이메일을 입력해주세요.")
    else:
        st.success(f"접속중:\n{st.session_state.current_user}")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

st.write("---")

# 4. 기능별 탭 구성
tab_home, tab_user, tab_admin = st.tabs(["📱 홈 (메뉴)", "📝 참가자 정보 등록", "🛡️ 관리자 모니터링"])

with tab_home:
    st.write("원하시는 아이콘 메뉴들입니다. (추후 상세 페이지 연결 가능)")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("📅 Program", use_container_width=True)
    with c2: st.button("🗺️ Floor Plan", use_container_width=True)
    with c3: st.button("ℹ️ Information", use_container_width=True)

with tab_user:
    st.subheader("참가자 정보 및 파일 제출")
    
    if not st.session_state.logged_in:
        st.info("👆 정보를 등록하려면 화면 우측 상단에서 이메일로 먼저 로그인해 주세요.")
    else:
        with st.form("user_submit_form"):
            st.write(f"**작성자 계정:** {st.session_state.current_user}")
            user_name = st.text_input("성명 및 소속 (예: 육군본부 최지영 대위)")
            user_message = st.text_area("건의사항 및 문의내용")
            
            uploaded_file = st.file_uploader("여기에 파일이나 사진을 업로드하세요", type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx'])
            submit_btn = st.form_submit_button("정보 등록하기")
            
            if submit_btn:
                file_name = uploaded_file.name if uploaded_file else "첨부파일 없음"
                st.session_state.db_data.append({
                    "이메일": st.session_state.current_user,
                    "성명/소속": user_name,
                    "내용": user_message,
                    "첨부파일": file_name
                })
                st.success("✅ 성공적으로 등록되었습니다! 관리자가 확인 후 안내해 드립니다.")

with tab_admin:
    st.subheader("관리자 전용 대시보드")
    
    # 관리자 계정 업데이트 완료
    ADMIN_EMAIL = "superbjy12@gmail.com"
    
    if not st.session_state.logged_in:
        st.warning("로그인이 필요합니다.")
    elif st.session_state.current_user != ADMIN_EMAIL:
        st.error(f"🚫 접근 불가: 이 페이지는 관리자 계정({ADMIN_EMAIL})으로 로그인해야만 볼 수 있습니다.")
    else:
        st.success("✅ 관리자 인증 완료. 현재 등록된 참가자 데이터를 실시간으로 모니터링합니다.")
        
        if len(st.session_state.db_data) > 0:
            st.dataframe(st.session_state.db_data, use_container_width=True)
        else:
            st.info("아직 등록된 참가자 정보가 없습니다.")