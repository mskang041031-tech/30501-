import streamlit as st
from datetime import date
import random
import time

# ============================================================
# Streamlit 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="🔮 COSMIC KBO PREDICT",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"  # 사이드바 닫힘 기본 설정
)

# ============================================================
# 판타지 타이포그래피 & 아방가르드 코스믹 CSS (사이드바 제거)
# ============================================================

st.markdown("""
    <!-- 구글 폰트 Import: 판타지 뾰족한 스타일 폰트 -->
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');

    /* 사이드바 완전히 숨기기 */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* 은하수 아방가르드 배경화면 */
    .stApp {
        background: linear-gradient(135deg, #090014 0%, #15002b 25%, #2a004f 50%, #120033 75%, #03000a 100%) !important;
        background-attachment: fixed !important;
        color: #e6f2ff !important;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 이미지의 판타지 텍스트 타이틀 스타일 (그라데이션 + 3D 핑크 그림자 + 뾰족한 폰트) */
    .fantasy-title {
        font-family: 'Cinzel Decorative', 'Noto Sans KR', cursive, serif;
        font-size: 3rem !important;
        font-weight: 900;
        text-align: center;
        letter-spacing: 2px;
        background: linear-gradient(180deg, #e1ff75 0%, #00f0ff 45%, #0040ff 85%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        filter: drop-shadow(3px 4px 0px #ff007f) drop-shadow(0px 0px 18px rgba(0, 240, 255, 0.8));
        margin-bottom: 0.2rem;
    }

    .fantasy-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #00ffff;
        opacity: 0.85;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* 카드 헤더 스타일 */
    .cosmic-card {
        background: rgba(255, 255, 255, 0.06);
        border: 2px solid rgba(0, 240, 255, 0.5);
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(12px);
        text-align: center;
    }

    /* 카드 내 판타지 텍스트 */
    .cosmic-card h1 {
        font-family: 'Cinzel Decorative', 'Noto Sans KR', sans-serif;
        font-weight: 900;
        background: linear-gradient(180deg, #ff99ec 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 2px 0px #00ffff);
    }

    /* 수정구슬 애니메이션 컨테이너 */
    .crystal-ball-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem;
        margin: 2rem 0;
        background: rgba(12, 0, 25, 0.8);
        border-radius: 25px;
        border: 1px solid rgba(255, 0, 127, 0.4);
        box-shadow: 0 0 50px rgba(138, 43, 226, 0.7);
    }

    /* 광채 나는 회전 수정구슬 이펙트 */
    .glowing-orb {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #ffffff, #ff00a0 40%, #00ffff 75%, #0a001a 100%);
        box-shadow: 0 0 35px #ff007f, 0 0 70px #00ffff, inset 0 0 25px #ffffff;
        animation: pulseOrb 2s infinite alternate, spinOrb 6s linear infinite;
        margin-bottom: 1.8rem;
    }

    @keyframes pulseOrb {
        0% { transform: scale(0.95); box-shadow: 0 0 25px #ff007f, 0 0 50px #00ffff; }
        100% { transform: scale(1.1); box-shadow: 0 0 50px #ff00a0, 0 0 90px #00ffff; }
    }

    @keyframes spinOrb {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }

    /* 예언 메시지 텍스트 */
    .oracle-text {
        font-family: 'Cinzel Decorative', 'Noto Sans KR', sans-serif;
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e1ff75, #00ffff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glowText 1.5s ease-in-out infinite alternate;
        text-align: center;
    }

    @keyframes glowText {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }

    [data-testid="stMetricValue"] {
        color: #00ffff !important;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 미래 날짜 설정 (1년 뒤 ~ 100년 뒤)
# ============================================================

today = date.today()
one_year_later = date(today.year + 1, today.month, today.day)
hundred_years_later = date(today.year + 100, 12, 31)

st.markdown('<div class="fantasy-title">COSMIC KBO PREDICT</div>', unsafe_allow_html=True)
st.markdown('<div class="fantasy-subtitle">🌌 은하수의 코스믹 파동을 통해 미래 100년의 KBO 운명을 예언합니다.</div>', unsafe_allow_html=True)

st.divider()

col_date, col_search = st.columns([1, 1])

with col_date:
    selected_date = st.date_input(
        "📅 예언 시점 선택",
        value=one_year_later,
        min_value=one_year_later,
        max_value=hundred_years_later
    )

with col_search:
    user_input = st.text_input(
        "🔍 예언받을 팀명 입력",
        placeholder="팀명 입력 (예: LG, KIA, 삼성, KT)"
    )

search_button = st.button("✨ 미래 운명 예언받기", use_container_width=True)

# ============================================================
# 알고리즘 데이터 생성기
# ============================================================

def generate_kbo_rankings(target_date):
    base_teams = {
        "KT": {"name": "KT 위즈", "keywords": ["KT", "kt", "케이티", "KT 위즈", "ktwiz"]},
        "삼성": {"name": "삼성 라이온즈", "keywords": ["삼성", "삼성 라이온즈", "삼성라이온즈"]},
        "LG": {"name": "LG 트윈스", "keywords": ["LG", "lg", "엘지", "LG 트윈스", "LG트윈스"]},
        "KIA": {"name": "KIA 타이거즈", "keywords": ["KIA", "kia", "기아", "KIA 타이거즈", "KIA타이거즈"]},
        "두산": {"name": "두산 베어스", "keywords": ["두산", "두산 베어스", "두산베어스"]},
        "롯데": {"name": "롯데 자이언츠", "keywords": ["롯데", "롯데 자이언츠", "롯데자이언츠"]},
        "한화": {"name": "한화 이글스", "keywords": ["한화", "한화 이글스", "한화이글스"]},
        "NC": {"name": "NC 다이노스", "keywords": ["NC", "nc", "엔씨", "NC 다이노스", "NC다이노스"]},
        "SSG": {"name": "SSG 랜더스", "keywords": ["SSG", "ssg", "쓱", "SSG 랜더스", "SSG랜더스"]},
        "키움": {"name": "키움 히어로즈", "keywords": ["키움", "키움 히어로즈", "키움히어로즈"]}
    }

    seed_value = int(target_date.strftime("%Y%m%d"))
    rng = random.Random(seed_value)

    team_keys = list(base_teams.keys())
    rng.shuffle(team_keys)

    month = target_date.month
    total_games = 144 if month > 10 or month < 4 else min(144, int((month - 3) * 22 + (target_date.day * 0.7)))

    teams_data = {}
    for rank, key in enumerate(team_keys, start=1):
        wins = max(0, int(total_games * (0.64 - (rank * 0.028)))) if total_games > 0 else 0
        draws = rng.randint(0, 3) if total_games > 20 else 0
        losses = max(0, total_games - wins - draws) if total_games > 0 else 0

        win_rate = f"{(wins / (wins + losses)):.3f}" if (wins + losses) > 0 else ".000"
        gb = f"{(rank - 1) * 2.5:.1f}"

        teams_data[key] = {
            **base_teams[key],
            "rank": rank,
            "games": total_games,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": win_rate,
            "games_behind": gb,
            "streak": f"{rng.randint(1, 4)}승" if rank <= 5 else f"{rng.randint(1, 4)}패",
            "era": f"{3.40 + (rank * 0.18):.2f}",
            "batting_avg": f"{0.285 - (rank * 0.005):.3f}"
        }

    return teams_data

def find_team(query, teams_data):
    if not query:
        return None
    cleaned = query.replace(" ", "").lower()
    for team in teams_data.values():
        if cleaned in team["name"].lower().replace(" ", ""):
            return team
        for kw in team["keywords"]:
            if cleaned == kw.lower().replace(" ", ""):
                return team
    return None

current_teams = generate_kbo_rankings(selected_date)
selected_team = find_team(user_input, current_teams)

# ============================================================
# 약 10초간의 수정구슬 로딩 이펙트 및 결과 출력
# ============================================================

if search_button or user_input:
    if selected_team is None:
        st.error("은하수의 파동에서 해당 팀을 찾을 수 없습니다. 올바른 팀명을 입력하세요.")
    else:
        team = selected_team

        # 수정구슬 이펙트 placeholder
        loading_placeholder = st.empty()

        # 약 10초 동안 애니메이션 연출
        phrases = [
            "수정구슬이 하늘의 힘으로 예언중 입니다...",
            "🌌 은하수의 코스믹 에너지를 모으는 중...",
            "✨ 시공간을 넘어 미래 KBO의 기운을 감지하고 있습니다...",
            "🔮 별들의 배치가 완성되어 가고 있습니다...",
            "⚡ 최종 미래 궤적이 수정구슬에 투영됩니다!"
        ]

        for i in range(10):
            phrase = phrases[i % len(phrases)]
            progress_percent = (i + 1) * 10
            
            loading_placeholder.markdown(f"""
                <div class="crystal-ball-container">
                    <div class="glowing-orb"></div>
                    <div class="oracle-text">{phrase}</div>
                    <p style="margin-top: 1rem; color: #00ffff; font-size: 0.9rem;">공명률 {progress_percent}%</p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.0)

        # 10초 후 연출 제거
        loading_placeholder.empty()

        # 결과 화면 출력
        st.markdown(f"""
            <div class="cosmic-card">
                <h2 style="margin:0; color:#00ffff; font-family:'Noto Sans KR';">🔮 {team['name']}의 미래 예언</h2>
                <p style="font-size:1.1rem; opacity:0.9; margin-top:5px;">시점: {selected_date.year}년 {selected_date.month}월 {selected_date.day}일</p>
                <h1 style="font-size:2.8rem; margin: 15px 0;">예상 순위: {team['rank']}위</h1>
                <p style="font-size:1.2rem; font-weight:600;">{team['wins']}승 {team['draws']}무 {team['losses']}패 (승률 {team['win_rate']})</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🌌 세부 예언 지표", "🍂 가을야구 운명"])

        with tab1:
            c1, c2, c3 = st.columns(3)
            c1.metric("소화 경기수", f"{team['games']}경기")
            c2.metric("1위와 게임차", f"{team['games_behind']}경기")
            c3.metric("최근 기운", team["streak"])

            st.markdown("---")
            ca, cb = st.columns(2)
            ca.metric("예상 평균자책점(ERA)", team["era"])
            cb.metric("예상 팀 타율", team["batting_avg"])

        with tab2:
            prob = max(5, min(98, 100 - (team['rank'] - 1) * 10))
            st.markdown("##### 🔮 포스트시즌 진출 예언 확률")
            st.progress(prob / 100)
            st.metric("진출 확률", f"{prob}%")
            
            if prob >= 70:
                st.success("✨ 하늘의 기운이 포스트시즌 진출을 강하게 암시합니다!")
            elif prob >= 40:
                st.warning("⚡ 치열한 가을야구 경계선에서 운명이 엇갈리고 있습니다.")
            else:
                st.error("🌌 이번 시점의 운명은 리빌딩의 시련을 예고합니다.")

else:
    st.info("👆 상단에서 **미래 날짜**와 **팀명**을 입력하고 **'미래 운명 예언받기'** 버튼을 누르면 수정구슬의 예언이 시작됩니다.")
