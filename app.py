import streamlit as st
import base64

# 1. 페이지 기본 설정
st.set_page_config(page_title="KAIF 2026", layout="centered", initial_sidebar_state="collapsed")

# URL 쿼리스트링을 통한 페이지 라우팅 동기화
if "page" in st.query_params:
    p = st.query_params["page"]
    st.session_state.active_page = p[0] if isinstance(p, list) else p

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_country' not in st.session_state:
    st.session_state.user_country = ""
if 'db_data' not in st.session_state:
    st.session_state.db_data = []
if 'active_page' not in st.session_state:
    st.session_state.active_page = "home"

# 이미지 파일을 Base64로 변환하는 함수 (아이콘용)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# 2. 커스텀 CSS 디자인
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0f172a 50%, #1e293b 100%);
        background-attachment: fixed;
        color: white;
    }
    /* 클릭 가능한 둥근 사각형 아이콘 카드 디자인 */
    .menu-card {
        background-color: #ffffff;
        border-radius: 20px;
        aspect-ratio: 1 / 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border: 2px solid #cbd5e1;
        transition: all 0.2s ease-in-out;
        margin-bottom: 15px;
    }
    .menu-card:hover {
        transform: translateY(-4px);
        border-color: #3b82f6;
        box-shadow: 0 6px 14px rgba(59,130,246,0.3);
        background-color: #f8fafc;
    }
    .menu-card img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        margin-bottom: 1px;
    }
    .menu-card span {
        color: #0f172a;
        font-weight: 800;
        font-size: 25px;
        text-align: center;
    }
    /* 로그인 버튼 글씨가 항상 선명하게 보이도록 색상 강제 고정 */
    div.stButton > button:first-child {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        border: 2px solid #cbd5e1 !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #f1f5f9 !important;
        border-color: #3b82f6 !important;
        color: #1d4ed8 !important;
    }
</style>
""", unsafe_allow_html=True)

# 🌟 3. 페이지 맨 위에 배치된 공식 플랫폼 문구 배너 (높이 축소)
st.markdown("""
<div style='
    text-align: center; 
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.5) 0%, rgba(15, 23, 42, 0.7) 100%); 
    padding: 12px 20px; 
    border-radius: 14px; 
    margin-bottom: 20px; 
    border: 1px solid rgba(59, 130, 246, 0.4);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
'>
    <h2 style='color: #93c5fd; font-weight: 800; font-size: 30px; margin: 0; letter-spacing: 0.5px;'>
        2026 KAIF Official mobile platform
    </h2>
</div>
""", unsafe_allow_html=True)

# 4. 상단 헤더 영역 (좌측: logo.png 및 WELCOME 문구, 우측: 슬림해진 로그인 패널)
col_title, col_login = st.columns([1.8, 2.2])

with col_title:
    try:
        st.image("logo.png", width=220)
    except:
        st.markdown("<h3 style='color:white;'>KAIF 2026</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:20px; font-weight:800; color:#93c5fd; margin-top:-16px; margin-bottom:0px; letter-spacing: 0.5px;'>WELCOME TO 2026 KAIF</p>", unsafe_allow_html=True)

with col_login:
    if not st.session_state.logged_in:
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#93c5fd; margin-bottom:4px; text-align:right;'>👤 참가자 정보 등록 및 로그인 / Login & Register</p>", unsafe_allow_html=True)
        login_email = st.text_input("이메일", placeholder="이메일 / Email", label_visibility="collapsed")
        c_name, c_country = st.columns(2)
        with c_name:
            input_name = st.text_input("성명", placeholder="성명 / Name", label_visibility="collapsed")
        with c_country:
            input_country = st.text_input("국가", placeholder="국가 / Country", label_visibility="collapsed")
            
        st.markdown("""
        <style>
            div.stButton > button:first-child {
                min-height: 38px !important;
                height: 38px !important;
                padding-top: 4px !important;
                padding-bottom: 4px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("로그인 / 등록 완료 (Login / Register Complete)", use_container_width=True):
            if login_email and input_name and input_country:
                st.session_state.logged_in = True
                st.session_state.current_user = login_email
                st.session_state.user_name = input_name
                st.session_state.user_country = input_country
                st.rerun()
            else:
                st.warning("이메일, 성명, 국가를 모두 입력해주세요.")
    else:
        st.markdown(f"""
        <div style='text-align:right; background-color:rgba(30, 41, 59, 0.8); padding:10px; border-radius:12px; border:1px solid #3b82f6;'>
            <p style='font-size:12px; color:#93c5fd; margin:0;'>접속 계정: <b>{st.session_state.current_user}</b></p>
            <p style='font-size:12px; color:#ffffff; margin:2px 0 4px 0;'>등록 정보: <b>{st.session_state.user_name} ({st.session_state.user_country})</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_user == "superbjy12@gmail.com":
            if st.button("🛡️ 관리자 대시보드 열기", use_container_width=True):
                st.session_state.active_page = "admin"
                st.rerun()
                
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.session_state.user_name = ""
            st.session_state.user_country = ""
            st.rerun()

st.write("---")

# 5. 화면 라우팅 (메인 홈 vs 상세 페이지)
if st.session_state.active_page == "home":
    # 2x3 클릭 가능한 커스텀 이미지 아이콘 카드 그리드 생성 함수
    def render_card(title, img_filename, page_name):
        b64_img = get_base64_image(img_filename)
        img_tag = f'<img src="data:image/png;base64,{b64_img}" alt="{title}">' if b64_img else f'<div style="font-size:32px; margin-bottom:8px;">📌</div>'
        html_code = f"""
        <a href="?page={page_name}" target="_self" style="text-decoration: none;">
            <div class="menu-card">
                {img_tag}
                <span>{title}</span>
            </div>
        </a>
        """
        st.markdown(html_code, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_card("Program", "icon_program.png", "program")
    with col2:
        render_card("Floor Plan", "icon_floor.png", "floor")
    with col3:
        render_card("Information", "icon_info.png", "info")
            
    col4, col5, col6 = st.columns(3)
    with col4:
        render_card("Photo", "icon_photo.png", "photo")
    with col5:
        render_card("Video", "icon_video.png", "video")
    with col6:
        render_card("Survey", "icon_survey.png", "survey")

else:
    if st.button("⬅️ 메인 홈으로 가기"):
        st.session_state.active_page = "home"
        st.query_params["page"] = "home"
        st.rerun()
    st.write("---")
    
    if st.session_state.active_page == "program":
        st.subheader("📅 행사 프로그램 (Program)")
        st.markdown("""
        * **10:00 - 11:00** : 개회식 및 기조연설
        * **11:00 - 12:00** : 글로벌 군수협력 파트너십 세션
        * **14:00 - 16:00** : MRO 발전 세미나 및 토론
        """)
        
    elif st.session_state.active_page == "floor":
        st.subheader("🗺️ 행사장 안내도 (Floor Plan)")
        st.info("행사장 메인 홀 및 세미나실 위치 안내입니다.")
        st.write("• 본관 대강당 (개회식 및 기조연설)")
        st.write("• 2층 세미나실 A·B (분과 세션)")
        
    elif st.session_state.active_page == "info":
        st.subheader("ℹ️ 포럼 소개 (Information)")
        st.write("한·아세안 국제군수포럼(KAIF 2026)은 아세안 회원국 간의 군수 협력 강화 및 미래 발전 방안을 모색하는 공식 포럼입니다.")
        
    elif st.session_state.active_page == "photo":
        st.subheader("📸 행사 포토 갤러리 (Photo)")
        st.info("KAIF 2026 주요 행사의 현장 사진을 확인하실 수 있습니다.")
        st.write("• 추후 현장 사진이 업로드될 예정입니다.")
        
    elif st.session_state.active_page == "video":
        st.subheader("▶️ 관련 영상 자료 (Video)")
        st.info("포럼 소개 영상 및 주요 세션 다시보기 서비스입니다.")
        st.write("• 공식 홍보 영상 및 세션 녹화본이 제공됩니다.")
        
    elif st.session_state.active_page == "survey":
        st.subheader("📝 참가자 정보 등록 및 파일 업로드 (Survey)")
        if not st.session_state.logged_in:
            st.warning("⚠️ 정보를 등록하려면 우측 상단의 입력란에 [이메일, 성명, 국가]를 입력하고 로그인해 주세요.")
        else:
            with st.form("user_submit_form"):
                st.write(f"**접속자:** {st.session_state.user_name} ({st.session_state.user_country} / {st.session_state.current_user})")
                user_message = st.text_area("건의사항 및 사전 질의내용")
                uploaded_file = st.file_uploader("관련 자료 또는 사진 업로드", type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx'])
                
                submit_btn = st.form_submit_button("정보 제출하기")
                if submit_btn:
                    file_name = uploaded_file.name if uploaded_file else "첨부파일 없음"
                    st.session_state.db_data.append({
                        "이메일": st.session_state.current_user,
                        "성명": st.session_state.user_name,
                        "국가": st.session_state.user_country,
                        "내용": user_message,
                        "첨부파일": file_name
                    })
                    st.success("✅ 성공적으로 등록되었습니다!")
                    
    elif st.session_state.active_page == "admin":
        st.subheader("🛡️ 관리자 모니터링 대시보드")
        ADMIN_EMAIL = "superbjy12@gmail.com"
        
        if not st.session_state.logged_in:
            st.warning("로그인이 필요합니다.")
        elif st.session_state.current_user != ADMIN_EMAIL:
            st.error(f"🚫 접근 불가: 지정된 관리자 계정({ADMIN_EMAIL})으로 로그인해야만 확인할 수 있습니다.")
        else:
            st.success("✅ 관리자 인증 완료. 실시간 등록 데이터를 확인합니다.")
            if len(st.session_state.db_data) > 0:
                st.dataframe(st.session_state.db_data, use_container_width=True)
            else:
                st.info("아직 등록된 참가자 정보가 없습니다.")
