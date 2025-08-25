import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ← 여기 바로 밑 (라이브러리 import 밑)
def parse_times(value):
    if not value:
        return []
    if isinstance(value, str):
        return [x.strip() for x in value.split(",")]
    elif isinstance(value, list):
        return value
    else:
        return []

def parse_levels(value):
    if not value:
        return []
    if isinstance(value, int):
        return [value]
    elif isinstance(value, str):
        return [int(x.strip()) for x in value.split(",") if x.strip().isdigit()]
    elif isinstance(value, list):
        return [int(x) for x in value]
    else:
        return []

# ------------------ 페이지 설정 ------------------
st.set_page_config(page_title="코칭 매칭", layout="wide")

# ------------------ 구글 시트 연동 ------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_dict = {
  "type": "service_account",
  "project_id": "streamlit-badminton",
  "private_key_id": "05c46b2ff12bf6691ed8e05802d6a262f957937f",
  "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDwjleXvs12Fgn
zOb0KhS1m6Wx9XXc4nuav3kxr+1YL1wedXUsAH5DehY1KSZF4zb7n9YzexsMQTpG
Hcccb/2pvPJEo+Iwlm20kacs77h30buThHVHHzi50QOUBo8jooaZ6QM97SyMir8L
WrO/Q+x7rFv3Zfx7dhScYVF1P7STrwwlQjZ+H4ALdK1tASBTcMlfCOGeclJuvyxb
C0BjJSk182Naa28Wx/Q+iN7Tjxokd/u6GA09ZHSjBpZwepRmy3Q46sU4BIfhsVgN
m/sg08qDIXN9WNhGgXzau8WOLjDlIqRKZAUOKqzjQTEBuYAXY3nxXjuUwh7Xg/4I
4Mx8TEo1AgMBAAECggEATlzA70yRPhg5DdGhwCraOGqylP7f7AiDl0o/nwrANXVb
6Ft3iKI36RYFrskmp4JRn793lQsaJDk2NRw1eOZBwkE/MAf0gyOsjcRiigP6MYi1
EFPNSKewYv3O82H+ybKFNDZJFHCNTUM7P7XSz2VG1KkF9Y6PV/LIRGNWottaE2Wj
efVO2/L4dYsTl5GNq9BEw0j+dculGMJMUMKpX0qwTGF14sc9FaCDu4S+/i20YeJ6
Dn2Y0RRnLew5iyQBfNly9C2Xn19c0/rEVEKsH6Rcu3CAeCmtE6FWTUy1TvK2VQk4
hn7nKNlDZkCnX+u8C1F+uwTAwQhD6+cxlyf2l+HXfwKBgQDg3MUmoRNzJmK8u04C
oEuNkxE8mnGSHuclnnjIlDc6ONpzW5gCyceyZHeo/glwQ+U1PatlEmDtUzex0p3L
Ge0J+zTn1m8AfxXlHY8RLURBq2Qy8qdUzmfDDYuHawE16RD9zctFHxzlsyzCaPjG
TGyvwguCzzPXl03+584vSa8E0wKBgQDe3b8NndhhxCBRSKCges6xV8KQEmPqHeDY
0bBhWvQL0EQXG80sntYyNY4OTLiFvfFszdwJyWkjOCQHPWcY1J6tPn2YrKiUZPLA
h4BukP5q5F0wYDR9aUYaArY2Eh5G64sDAuTRXUDXC21+S/wFfbkaa8ok5h5Wlsd3
V1oTTBGv1wKBgF8Rd9kJKOv6QqyAlE7P7qGAmD0DHxkkL53cDjzfTSo0d0dmZjJn
lSJ7D4xHOz5XtkR4OkqVJp2wHU/1N/lykKEzr/6EzpFrKZqgkKg2dzE8gTR5Gv3j
9kKlK2SpfO2KCEEGDPbAXLtQsY/QSb2s+hak97DqYYS416T55FZh1Lk5AoGBAJQD
5g2fFcTowyX4/GVY6smxpZCWBjHJIjoeGeyuwYLPEUnftwa5fzzdgLlSjwKUQjGn
D0qYr/EqKhN83moJXFFnPXcWxOe5m9fupofIWJCZlqK4YmQgdOR1hJqosd8cNLkN
RPcf3h50goXs5TaoZzV6/UhAZUnQ3i0OoM5MKTsFAoGAKbVezmwTBa2nOECoU8UL
MsIw8edthaCinW/nJLtQb769Es/X7rHrQ5nplAPgls3Y3jlNwZEzFRl7dbFpMbCp
8X+9sZdYqg8It26dkLHpvSnHCwO434qPGOPLUWgblBRYdXdrInEXuEcVVY7/i1kr
CzyjDtjgwa6aiLPMyniPHSc=
-----END PRIVATE KEY-----""",
  "client_email": "badminton@streamlit-badminton.iam.gserviceaccount.com",
  "client_id": "115918370315226724362",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/badminton%40streamlit-badminton.iam.gserviceaccount.com"
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
@st.cache_resource
def get_sheet():
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1CT5AC_bNhWHm3YxPuI00xhdgYrYu2XMNZVFBT31R0aw/edit?usp=sharing")
sheet = get_sheet()

# 워크시트 불러오기
ws_participants = sheet.worksheet("참가자")
ws_absentees = sheet.worksheet("불참자")
ws_matches = sheet.worksheet("매치")
ws_feedbacks = sheet.worksheet("후기")

# ---- 각 워크시트별 캐싱 로더 ----
@st.cache_data(ttl=60)
def load_participants_cached():
    return ws_participants.get_all_records()

@st.cache_data(ttl=60)
def load_absentees_cached():
    return ws_absentees.get_all_records()

@st.cache_data(ttl=60)
def load_matches_cached():
    return ws_matches.get_all_records()

@st.cache_data(ttl=60)
def load_feedbacks_cached():
    return ws_feedbacks.get_all_records()


# ------------------ 🎨 스타일 ------------------
st.markdown("""
    <style>
    .title {text-align: center; color: teal; font-size: 36px; font-weight: bold; margin-bottom: 10px;}
    .subtitle {text-align: center; font-size: 20px; margin-bottom: 30px;}
    .team-box {border: 2px solid #00bcd4; border-radius: 10px; padding: 10px; margin-bottom: 20px; background-color: #f0f9fb;}
    .waiting {font-size: 14px; color: gray;}
    </style>
    <div class="title">🏸 기술 코칭 매칭</div>
    <hr>
""", unsafe_allow_html=True)

# ------------------ 세션 상태 초기화 ------------------
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "password" not in st.session_state:
    st.session_state.password = ""
if "finalized" not in st.session_state:
    st.session_state.finalized = False
if "show_participants" not in st.session_state:
    st.session_state.show_participants = False
if "show_absentees" not in st.session_state:
    st.session_state.show_absentees = False
if "show_matching" not in st.session_state:
    st.session_state.show_matching = False
if "show_feedbacks" not in st.session_state:
    st.session_state.show_feedbacks = False

# ------------------ 🔐 관리자 로그인 ------------------
with st.sidebar:
    st.markdown("### 🔐 관리자 모드")

    password = st.text_input("비밀번호 입력", type="password", value=st.session_state.get("password", ""), key="password_input")
    st.session_state.password = password

    if password == "04281202":
        st.session_state.is_admin = True
        st.success("관리자 모드 활성화됨")
    else:
        st.session_state.is_admin = False
        if password != "":
            st.error("비밀번호가 틀립니다")

    if st.session_state.is_admin:
        if st.sidebar.button("🔓 관리자 모드 종료", key="admin_exit_btn"):
            st.session_state.is_admin = False
            st.session_state.password = ""
            st.rerun()

        if st.sidebar.button("👥 참가자 현황", key="show_participants_btn"):
            st.session_state.show_participants = not st.session_state.get("show_participants", False)
            st.session_state.show_absentees = False
            st.session_state.show_matching = False
            st.session_state.show_feedbacks = False

        if st.sidebar.button("🚫 불참자 확인", key="show_absentees_btn"):
            st.session_state.show_participants = False
            st.session_state.show_matching = False
            st.session_state.show_feedbacks = False
            st.session_state.show_absentees = not st.session_state.get("show_absentees", False)
        
        if st.sidebar.button("🎲 코칭 매칭", key="show_matching_btn"):
            st.session_state.show_matching = not st.session_state.get("show_matching", False)
            st.session_state.show_participants = False
            st.session_state.show_absentees = False
            st.session_state.show_feedbacks = False

        if st.sidebar.button("📝 후기 확인", key="show_feedbacks_btn"):
            st.session_state.show_feedbacks = not st.session_state.get("show_feedbacks", False)
            st.session_state.show_participants = False
            st.session_state.show_absentees = False
            st.session_state.show_matching = False

        if st.sidebar.button("🔄 초기화", key="reset_btn"):

            def reset_all():
                # 구글 시트 초기화 및 헤더 재설정
                ws_participants.clear()
                ws_participants.append_row(["이름", "역할", "코칭 가능 레벨", "코칭 가능 시간대", "학생 레벨", "희망 기술", "기타 기술", "레슨 희망 시간대"])

                ws_absentees.clear()
                ws_absentees.append_row(["이름", "불참 사유"])

                ws_matches.clear()
                ws_matches.append_row(["시간", "코칭자", "레슨자", "기술"])

                ws_feedbacks.clear()
                ws_feedbacks.append_row(["역할", "이름", "시간", "후기", "작성시간"])

                load_participants_cached.clear()
                load_absentees_cached.clear()
                load_matches_cached.clear()
                load_feedbacks_cached.clear()

                # 세션 상태 중 초기화할 키만 선택적으로 초기화
                keys_to_reset = ["participants", "non_attendees", "attendance", "game_results",
                                "teams", "team_pairs", "match_scores", "partner_selections"]

                for key in keys_to_reset:
                    if key in st.session_state:
                        if isinstance(st.session_state[key], dict):
                            st.session_state[key] = {}
                        elif isinstance(st.session_state[key], list):
                            st.session_state[key] = []
                        else:
                            st.session_state[key] = None

                # 초기화 완료 플래그 설정
                st.session_state["just_reset"] = True

            reset_all()
            st.rerun()

        if st.session_state.get("just_reset"):
            st.success("초기화 완료")
            del st.session_state["just_reset"]

# 📌 구글 시트와 세션 상태를 함께 확인하는 최종 매칭 여부 판별
def is_finalized():
    match_data = load_matches_cached()
    if len(match_data) > 0:
        return True
    return st.session_state.get("finalized", False)

# ------------------ 관리자 모드 메인 영역 ------------------
if st.session_state.is_admin:
    # 참가자 현황
    if st.session_state.get("show_participants", False):
        participants_data = load_participants_cached()
        st.subheader("👥 참가자 현황")
        if participants_data:
            st.dataframe(participants_data)
        else:
            st.info("참가자 데이터가 없습니다.")


    # 불참자 현황
    if st.session_state.get("show_absentees", False):
        absentees_data = load_absentees_cached()  # 참가자 워크시트가 아니라 불참자 워크시트 확인
        if absentees_data:
            st.subheader("🚫불참자 현황")
            st.dataframe(absentees_data)
        else:
            st.info("불참자 데이터가 없습니다.")

    # ------------------ 코칭 매칭 (관리자) ------------------
    if st.session_state.get("show_matching", False):
        participants = load_participants_cached()
        coaches = [p for p in participants if "코칭자" in p["역할"]]
        students = [p for p in participants if "레슨자" in p["역할"]]

        timeslots = ["1:10~1:20", "1:20~1:30", "1:30~1:40", "1:40~1:50"]
        courts = [f"{i}코트" for i in range(1, 8)]
        matches = []
        assigned_students_global = set()
        participants_dict = {p["이름"]: p for p in participants}

        # 매칭 로직 (기존 그대로)
        for t in timeslots:
            court_assignment = {c: {"코칭자": "", "레슨자": "", "기술": ""} for c in courts}
            assigned_coaches_local = set()

            # 1️⃣ 학생-코치 배치
            for student in students:
                if student["이름"] in assigned_students_global:
                    continue
                student_times = parse_times(student.get("레슨 희망 시간대"))
                student_levels = parse_levels(student.get("학생 레벨"))
                student_skill = student.get("희망 기술", "")
                matched = False

                for coach in coaches:
                    if coach["이름"] in assigned_coaches_local:
                        continue
                    coach_times = parse_times(coach.get("코칭 가능 시간대"))
                    coach_levels = parse_levels(coach.get("코칭 가능 레벨"))

                    if t in student_times and t in coach_times and any(l <= cl for l in student_levels for cl in coach_levels):
                        for court in courts:
                            if court_assignment[court]["레슨자"] == "":
                                court_assignment[court]["레슨자"] = student["이름"]
                                court_assignment[court]["코칭자"] = coach["이름"]
                                court_assignment[court]["기술"] = student_skill
                                assigned_students_global.add(student["이름"])
                                assigned_coaches_local.add(coach["이름"])
                                matched = True
                                break
                        if matched:
                            break

            # 2️⃣ 남은 학생 배치
            for student in students:
                if student["이름"] in assigned_students_global:
                    continue
                if t in parse_times(student.get("레슨 희망 시간대")):
                    for court in courts:
                        if court_assignment[court]["레슨자"] == "":
                            court_assignment[court]["레슨자"] = student["이름"]
                            court_assignment[court]["코칭자"] = ""
                            court_assignment[court]["기술"] = student.get("희망 기술", "")
                            assigned_students_global.add(student["이름"])
                            break

            # 3️⃣ 빈 코트에 코치만 배치
            for coach in coaches:
                if t in parse_times(coach.get("코칭 가능 시간대")) and coach["이름"] not in assigned_coaches_local:
                    for court in courts:
                        if court_assignment[court]["레슨자"] == "":
                            court_assignment[court]["코칭자"] = coach["이름"]
                            court_assignment[court]["레슨자"] = "빈 코트"
                            court_assignment[court]["기술"] = ""
                            assigned_coaches_local.add(coach["이름"])
                            break

            # matches 리스트 생성
            for court in courts:
                matches.append({
                    "시간": t,
                    "코트": court,
                    "코칭자": court_assignment[court]["코칭자"],
                    "레슨자": court_assignment[court]["레슨자"],
                    "기술": court_assignment[court]["기술"]
                })

         # ================== 시간대별 출력 ==================
        st.subheader("🎲 시간대별 코칭 매칭 (관리자)")
        for t in timeslots:
            with st.expander(f"🕒 {t}", expanded=True):
                t_matches = [m for m in matches if m["시간"] == t]
                for m in t_matches:
                    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,2])
                    
                    # 코트
                    with col1:
                        st.write(m["코트"])

                    # 코칭자 선택
                    with col2:
                        coach_options = [c["이름"] for c in coaches] + [""]
                        coach_edit = st.selectbox(
                            f"{m['시간']}_{m['코트']}_코칭자",
                            options=coach_options,
                            index=coach_options.index(m["코칭자"]) if m["코칭자"] in coach_options else 0,
                            key=f"coach_edit_{m['시간']}_{m['코트']}"
                        )

                    # 코칭자 레벨 (관리자 모드 전용)
                    with col3:
                        if coach_edit in participants_dict:
                            coach_levels = participants_dict[coach_edit].get("코칭 가능 레벨", "")
                            st.markdown(f"레벨: {coach_levels}" if coach_levels else "레벨: -")

                    # 레슨자 선택
                    with col4:
                        student_options = [s["이름"] for s in students] + ["빈 코트", ""]
                        student_edit = st.selectbox(
                            f"{m['시간']}_{m['코트']}_레슨자",
                            options=student_options,
                            index=student_options.index(m["레슨자"]) if m["레슨자"] in student_options else 0,
                            key=f"student_edit_{m['시간']}_{m['코트']}"
                        )

                    # 레슨자 레벨 (관리자 모드 전용)
                    with col5:
                        if student_edit in participants_dict:
                            student_level = participants_dict[student_edit].get("학생 레벨", "")
                            st.markdown(f"레벨: {student_level}" if student_level else "레벨: -")

                    # 기술 입력
                    with col6:
                        skill_default = participants_dict.get(student_edit, {}).get("희망 기술", "")
                        skill_edit = st.text_input(
                            f"{m['시간']}_{m['코트']}_기술",
                            value=skill_default,
                            key=f"skill_edit_{m['시간']}_{m['코트']}"
                        )
        # ------------------ ✅ 배정 상태 확인 버튼 ------------------
        if st.button("배정 상태 확인", key="check_assignment_btn"):
            issues = []  # 문제 메시지 모음

            # 시간대별 코칭자/레슨자 체크
            for t in timeslots:
                assigned_coaches = []
                assigned_students = []
                for court in courts:
                    coach_val = st.session_state.get(f"coach_edit_{t}_{court}", "")
                    student_val = st.session_state.get(f"student_edit_{t}_{court}", "")

                    # 빈 코트, 빈 문자열 제외
                    if coach_val not in ["", "빈 코트"]:
                        assigned_coaches.append(coach_val)
                    if student_val not in ["", "빈 코트"]:
                        assigned_students.append(student_val)

                # 1️⃣ 중복 체크
                dup_coaches = [c for c in set(assigned_coaches) if assigned_coaches.count(c) > 1]
                dup_students = [s for s in set(assigned_students) if assigned_students.count(s) > 1]

                if dup_coaches:
                    issues.append(f"⚠️ 시간대 {t}: 중복 코칭자 - {', '.join(dup_coaches)}")
                if dup_students:
                    issues.append(f"⚠️ 시간대 {t}: 중복 레슨자 - {', '.join(dup_students)}")

            # 2️⃣ 모든 레슨자 배정 여부 체크
            all_students = [s["이름"] for s in students if s["이름"] not in ["", "빈 코트"]]
            assigned_students_global = []
            for t in timeslots:
                for court in courts:
                    student_val = st.session_state.get(f"student_edit_{t}_{court}", "")
                    if student_val not in ["", "빈 코트"]:
                        assigned_students_global.append(student_val)
            unassigned_students = [s for s in all_students if s not in assigned_students_global]
            if unassigned_students:
                issues.append(f"⚠️ 배정되지 않은 레슨자: {', '.join(unassigned_students)}")

            # 결과 표시
            if not issues:
                st.success("✅ 모든 레슨자가 배정되었고, 중복 배정도 없습니다.")
            else:
                for msg in issues:
                    st.warning(msg)

        # ✅ 최종 제출 버튼
        if st.button("최종 제출", key="submit_matches_btn"):
            ws_matches.clear()
            ws_matches.append_row(["시간","코트","코칭자","레슨자","기술"])
            
            for t in timeslots:
                for m in [mm for mm in matches if mm["시간"] == t]:
                    coach_val = st.session_state.get(f"coach_edit_{m['시간']}_{m['코트']}", "")
                    student_val = st.session_state.get(f"student_edit_{m['시간']}_{m['코트']}", "")
                    skill_val = st.session_state.get(f"skill_edit_{m['시간']}_{m['코트']}", "")
                    
                    # ⬅ 수정: 레슨자/코칭자 값이 유효할 때만 기록
                    if student_val and student_val != "빈 코트":
                        ws_matches.append_row([m["시간"], m["코트"], coach_val if coach_val else "", student_val, skill_val])
            
            load_matches_cached.clear()
            st.session_state.finalized = True
            st.success("최종 매칭 완료! 모든 코트가 반영되었습니다.")


    # 후기 확인
    if st.session_state.get("show_feedbacks", False):
        feedbacks_data = load_feedbacks_cached()
        if feedbacks_data:
            st.subheader("코칭 후기")
            st.dataframe(feedbacks_data)
        else:
            st.info("등록된 코칭 후기가 없습니다.")


# 비관리자 모드에서 참가자 제출 전 입력 부분
if not st.session_state.is_admin and not st.session_state.finalized:
    name = st.text_input("성명을 입력하시오")
    lunch = st.radio("오늘 점심에 오나요?", ["예", "아니오"])

    # 여기에 reason 변수를 미리 빈 문자열로 선언
    reason = ""

    if lunch == "예":
        role = st.radio("역할 선택", ["코칭자", "레슨자"], index=None)
        roles = [role] if role else []

        coach_level_max = None
        coach_times = []
        student_level = []
        skills = []
        other_skill = ""
        student_times = []

        if role == "코칭자":
            coach_level_max = st.slider("코칭 가능 최대 레벨 선택", 1, 5, 3, key="coach_level_max_slider")
            st.markdown(
                '<div style="display:flex; justify-content: space-between; color: gray; font-size: 12px; margin-top: 4px;">'
                '<span>1</span><span>2</span><span>3</span><span>4</span><span>5</span></div>',
                unsafe_allow_html=True
            )

            st.write("코칭 가능 시간대 선택 (중복 가능):")
            times = ["1:10~1:20", "1:20~1:30", "1:30~1:40", "1:40~1:50"]
            coach_times = []
            for t in times:
                if st.checkbox(t, key=f"coach_time_{t}"):
                    coach_times.append(t)

        elif role == "레슨자":
            student_level = st.radio("본인 레벨 선택", [1, 2, 3, 4, 5], key="student_level_radio")
            skills = st.multiselect(
                "희망 기술",
                ["스텝", "클리어", "스매쉬", "헤어핀", "드롭", "언더", "드라이브", "푸쉬", "기타"],
                key="skills_multiselect"
            )
            if "기타" in skills:
                other_skill = st.text_input("기타 기술 입력", key="other_skill_text")
            student_times = st.radio(
                "레슨 희망 시간대 선택",
                ["1:10~1:20", "1:20~1:30", "1:30~1:40", "1:40~1:50"],
                key="student_times_radio"
            )

    else:
        reason = st.text_area("불참 사유를 작성하세요")  # lunch == "아니오"일 때 reason 입력 받기

    # 제출 버튼 (비관리자)
    if st.button("제출", key="submit_participant_btn"):
        if lunch == "예":
            ws_participants.append_row([
                str(name),
                ", ".join(roles) if roles else "",
                str(coach_level_max) if coach_level_max else "",
                ", ".join(coach_times) if coach_times else "",
                str(student_level) if student_level else "",
                ", ".join(skills) if skills else "",
                str(other_skill),
                str(student_times) if student_times else "",
            ])
            load_participants_cached.clear()
            st.success("제출 완료! 참가자 현황에 반영되었습니다.")
            st.session_state.show_participants = True
            st.rerun()

        else:
            ws_absentees.append_row([str(name), str(reason)])
            load_absentees_cached.clear()
            st.success("제출 완료! 불참자 목록에 반영되었습니다.")
            st.session_state.show_absentees = True
            st.rerun()


# ------------------ 비관리자 화면 ------------------
if not st.session_state.is_admin:
    if not is_finalized():
        st.subheader("👥 참가자 현황")
        participants_data = load_participants_cached()

        if participants_data:
            # 시간대 집합 생성 (코칭자와 레슨자 시간 합치기)
            coach_times = sorted(set(
                t.strip()
                for p in participants_data if p.get("코칭 가능 시간대")
                for t in p["코칭 가능 시간대"].split(",")
            ))
            student_times = sorted(set(
                t.strip()
                for p in participants_data if p.get("레슨 희망 시간대")
                for t in p["레슨 희망 시간대"].split(",")
            ))
            all_times = sorted(set(coach_times + student_times))

            for t in all_times:
                with st.expander(f"🕒 {t}", expanded=True):
                    # 시간대별 코칭자
                    coaches = [p["이름"] for p in participants_data
                               if p.get("역할") == "코칭자" and t in parse_times(p.get("코칭 가능 시간대"))]
                    # 시간대별 레슨자
                    students = [p["이름"] for p in participants_data
                                if p.get("역할") == "레슨자" and t in parse_times(p.get("레슨 희망 시간대"))]

                    st.markdown("**⭐ 코칭자**")
                    st.write("\n".join([f"- {c}" for c in coaches]) if coaches else "없음")

                    st.markdown("**💡 레슨자**")
                    st.write("\n".join([f"- {s}" for s in students]) if students else "없음")

        else:
            st.info("참가자 데이터가 없습니다.")

        st.warning("⚠️ 아직 최종 매칭이 완료되지 않았습니다.")

    else:
        # ✅ 최종 매칭 결과
        matches = load_matches_cached()
        timeslots = sorted(set([m.get("시간") for m in matches if m.get("시간")]))

        if not timeslots:
            st.warning("최종 매칭 데이터가 없습니다.")
        else:
            st.subheader("✅ 최종 매칭 결과")
            for t in timeslots:
                with st.expander(f"🕒 {t}", expanded=True):
                    t_matches = [m for m in matches if m.get("시간") == t]
                    for m in t_matches:
                        coach = m.get("코칭자", "")
                        student = m.get("레슨자", "")
                        skill = m.get("기술", "")
                        st.markdown(
                            f"**{m.get('코트', '')}**  \n"
                            f"- ⭐ 코칭자: {coach if coach else '없음'}  \n"
                            f"- 💡 레슨자: {student if student and student != '빈 코트' else '없음'}  \n"
                            f"- 🏸 기술: {skill if skill else '-'}"
                        )

        # 코칭 후기 작성
        st.subheader("📝 코칭 후기 작성")
        name = st.text_input("이름 입력", key="feedback_name")
        role = st.selectbox("역할", ["코칭자", "레슨자"], key="feedback_role")
        time = st.selectbox("시간대 선택", ["1:10~1:20", "1:20~1:30", "1:30~1:40", "1:40~1:50"], key="feedback_time")
        feedback = st.text_area("코칭 후기 작성", key="feedback_text")

        if st.button("코칭 완료", key="complete_feedback_btn"):
            if name and feedback:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ws_feedbacks.append_row([role, name, time, feedback, now])
                load_feedbacks_cached.clear()
                st.success("코칭 완료! 출석이 기록되었습니다.")
            else:
                st.warning("이름과 후기는 반드시 입력해야 합니다.")
