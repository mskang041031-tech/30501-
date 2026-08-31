import streamlit as st
from datetime import date
import random

# ============================================================
# Streamlit 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="🔮 KBO 100년 미래 예언 시뮬레이터",
    page_icon="🔮",
    layout="centered"
)

# ============================================================
# 커스텀 UI 디자인 (CSS)
# ============================================================

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 700;
    }
    .team-header-card {
        background-color: var(--background-secondary-color);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 미래 날짜 선택 & 검색 섹션 (1년 뒤 ~ 100년 뒤)
# ============================================================

today = date.today()
one_year_later = date(today.year + 1, today.month, today.day)
hundred_years_later = date(today.year + 100, 12, 31)

st.title("🔮 KBO 100년 미래 예언 시뮬레이터")
st.caption(f"미래 타임라인({one_year_later.year}년 ~ {hundred_years_later.year}년)의 KBO 성적 및 가을야구 예언")

st.divider()

col_date, col_search = st.columns([1, 1])

with col_date:
    selected_date = st.date_input(
        "🔮 예언할 미래 날짜 선택",
        value=one_year_later,
        min_value=one_year_later,
        max_value=hundred_years_later,
        help="현재로부터 1년 뒤부터 100년 뒤까지의 미래 날짜를 지정해 성적을 예언합니다."
    )

with col_search:
    user_input = st.text_input(
        "🔍 팀명 검색",
        placeholder="팀명 입력 (예: LG, KIA, 삼성, KT)"
    )

# ============================================================
# 독립형 데이터 엔진 (날짜 시드 기반 시뮬레이션)
# ============================================================

def generate_kbo_rankings(target_date):
    """
    미래 날짜 시드(Seed)를 기반으로 언제 조회하든 일관된 미래 성적을 예언합니다.
    """
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

    # 미래 날짜를 난수 시드로 사용
    seed_value = int(target_date.strftime("%Y%m%d"))
    rng = random.Random(seed_value)

    team_keys = list(base_teams.keys())
    rng.shuffle(team_keys)

    # 월별 소화 경기수 계산
    month = target_date.month
    if month < 4:
        total_games = 0
    elif month > 10:
        total_games = 144
    else:
        total_games = min(144, int((month - 3) * 22 + (target_date.day * 0.7)))

    teams_data = {}
    for rank, key in enumerate(team_keys, start=1):
        if total_games > 0:
            wins = max(0, int(total_games * (0.64 - (rank * 0.028))))
            draws = rng.randint(0, 3) if total_games > 20 else 0
            losses = max(0, total_games - wins - draws)
        else:
            wins, losses, draws = 0, 0, 0

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

# 데이터 생성
current_teams = generate_kbo_rankings(selected_date)

# ============================================================
# 알고리즘 & 검색 함수
# ============================================================

def calculate_playoff_probability(team, teams_data):
    rank = team["rank"]
    try:
        win_rate = float(team["win_rate"])
    except ValueError:
        win_rate = 0.500

    fifth_team = next((t for t in teams_data.values() if t["rank"] == 5), None)
    
    try:
        current_gb = float(team["games_behind"])
        fifth_gb = float(fifth_team["games_behind"]) if fifth_team else 0.0
        gb_from_5th = current_gb - fifth_gb
    except ValueError:
        gb_from_5th = 0.0

    score = win_rate * 100

    if rank <= 5:
        score += (6 - rank) * 5
        score -= gb_from_5th * 2.5
    else:
        score -= (rank - 5) * 6
        score -= gb_from_5th * 3.5

    score = max(1, min(99, score))
    return round(score)

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

selected_team = find_team(user_input, current_teams)

# ============================================================
# 사이드바: 미래 10개 구단 순위 예언
# ============================================================

with st.sidebar:
    st.header("🔮 미래 순위 예언표")
    st.caption(f"예언 타임라인: {selected_date.strftime('%Y-%m-%d')}")
    st.divider()

    sorted_teams = sorted(current_teams.values(), key=lambda x: x["rank"])
    for item in sorted_teams:
        rank = item["rank"]
        name = item["name"]
        win_rate = item["win_rate"]
        gb = item["games_behind"]
        
        is_selected = selected_team and selected_team["name"] == name
        highlight = "👈" if is_selected else ""
        rank_badge = f"**{rank}위**" if rank <= 5 else f"{rank}위"
        
        st.write(f"{rank_badge} **{name}** {highlight}")
        st.caption(f"예상 승률: {win_rate} | 게임차: {gb}")
        
        if rank == 5:
            st.markdown("--- 🔻 **가을야구 커트라인** 🔻 ---")
        else:
            st.markdown("<hr style='margin: 3px 0 6px 0; border: none; border-top: 1px dashed #cccccc;'>", unsafe_allow_html=True)

# ============================================================
# 메인 화면
# ============================================================

if user_input:
    if selected_team is None:
        st.error("해당 팀을 찾을 수 없습니다.")
        st.info("💡 **입력 가능 예시:** KT, 삼성, LG, KIA, 두산, 롯데, 한화, NC, SSG, 키움")
    else:
        team = selected_team
        
        st.markdown(f"""
            <div class="team-header-card">
                <h2 style="margin:0; padding-bottom: 5px;">🔮 {team['name']} <span style="font-size:0.9rem; font-weight:normal; opacity:0.8;">({selected_date.year}년 예언)</span></h2>
                <p style="margin:0; font-size:1rem; font-weight:600;">예상 순위: <strong>{team['rank']}위</strong> | {team['wins']}승 {team['draws']}무 {team['losses']}패 (승률 {team['win_rate']})</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📊 미래 예상 성적", "🍂 가을야구 확률 예언"])

        with tab1:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("예상 순위", f"{team['rank']}위")
            c2.metric("예상 전적", f"{team['wins']}승 {team['draws']}무 {team['losses']}패")
            c3.metric("예상 승률", team["win_rate"])
            c4.metric("연속 기록", team["streak"])

            st.markdown("---")
            c_a, c_b, c_c = st.columns(3)
            c_a.metric("소화 경기수", f"{team['games']}경기")
            c_b.metric("1위와 게임차", f"{team['games_behind']}경기")
            c_c.metric("팀 ERA / 타율", f"{team['era']} / {team['batting_avg']}")

        with tab2:
            probability = calculate_playoff_probability(team, current_teams)
            st.markdown("##### 🔮 포스트시즌 진출 예언 확률")
            st.progress(probability / 100)
            
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                st.metric("진출 예언 확률", f"{probability}%")
            with p_col2:
                if probability >= 70:
                    st.success("미래의 가을야구 진출 가능성이 매우 명확합니다!")
                elif probability >= 40:
                    st.warning("미래의 치열한 5위 싸움이 예견됩니다.")
                else:
                    st.error("미래 성적 반등을 위한 과감한 리빌딩이 필요합니다.")

else:
    st.info("👆 상단에서 **예언할 미래 날짜**를 선택하고 **팀명**을 검색해 보세요. (좌측 사이드바에서 미래 순위표를 확인할 수 있습니다.)")
