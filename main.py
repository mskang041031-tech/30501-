import streamlit as st
from datetime import date, timedelta
import random

# ============================================================
# Streamlit 기본 설정
# ============================================================

st.set_page_config(
    page_title="KBO TEAM INFO",
    page_icon="⚾",
    layout="centered"
)

# ============================================================
# 날짜 선택 설정 (오늘 ~ 10년 전)
# ============================================================

today = date.today()
ten_years_ago = today - timedelta(days=365 * 10)

st.title("⚾ KBO TEAM INFO")

# 날짜 선택 피커 (Sidebar 또는 상단 배치)
selected_date = st.date_input(
    "📅 조회할 기준일을 선택하세요",
    value=today,
    min_value=ten_years_ago,
    max_value=today,
    help="오늘부터 최대 10년 전까지의 KBO 성적을 조회할 수 있습니다."
)

st.caption(f"선택된 기준일: **{selected_date.strftime('%Y년 %m월 %d일')}**")
st.divider()

# ============================================================
# 동적 팀 데이터 생성 함수 (날짜 연동 시뮬레이션)
# ============================================================

def get_teams_by_date(target_date):
    """
    선택된 날짜에 따라 팀 성적 데이터를 가공하는 함수.
    (실제 운영 환경에서는 DB나 KBO API와 연동하여 호출)
    """
    # 기본 10개 구단 프로필
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

    # 날짜 시드값으로 일관성 있는 난수 성적 생성 (테스트용)
    seed_value = int(target_date.strftime("%Y%m%d"))
    rng = random.Random(seed_value)

    # 임의 순위 할당
    team_keys = list(base_teams.keys())
    rng.shuffle(team_keys)

    teams_data = {}
    for rank, key in enumerate(team_keys, start=1):
        # 시즌 진행 상황 반영 (월에 따른 경기 수 차등)
        month = target_date.month
        if month < 4 or month > 10:
            games = 144 if month > 10 else 0
        else:
            games = min(144, int((month - 3) * 22 + (target_date.day * 0.7)))

        wins = int(games * (0.65 - (rank * 0.03))) if games > 0 else 0
        draws = rng.randint(0, 4) if games > 10 else 0
        losses = max(0, games - wins - draws)
        
        win_rate = f"{(wins / (wins + losses)):.3f}" if (wins + losses) > 0 else ".000"
        gb = f"{(rank - 1) * 2.5:.1f}"

        teams_data[key] = {
            **base_teams[key],
            "rank": rank,
            "games": games,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": win_rate,
            "games_behind": gb,
            "streak": f"{rng.randint(1, 5)}승" if rank <= 5 else f"{rng.randint(1, 5)}패",
            "batting_avg": f"{0.250 + (rng.randint(0, 40) / 1000):.3f}",
            "era": f"{3.50 + (rank * 0.2):.2f}",
            "recent_game": f"{target_date.month}월 {max(1, target_date.day - 1)}일 경기 완료"
        }

    return teams_data

# 선택된 날짜 기준 데이터 세트 생성
current_teams = get_teams_by_date(selected_date)

# ============================================================
# 가을야구 예상 확률 계산
# ============================================================

def calculate_playoff_probability(team, teams_data):
    rank = team["rank"]
    try:
        win_rate = float(team["win_rate"])
    except ValueError:
        win_rate = 0.500

    fifth_place_gb = next(float(t["games_behind"]) for t in teams_data.values() if t["rank"] == 5)
    current_gb = float(team["games_behind"])
    gb_from_5th = current_gb - fifth_place_gb

    score = win_rate * 100

    if rank <= 5:
        score += (6 - rank) * 5
        score -= gb_from_5th * 2
    else:
        score -= (rank - 5) * 6
        score -= gb_from_5th * 4

    score = max(1, min(99, score))
    return round(score)

# ============================================================
# 팀 검색 함수
# ============================================================

def find_team(user_input, teams_data):
    cleaned_input = user_input.replace(" ", "").lower()
    for team_code, team in teams_data.items():
        if cleaned_input == team_code.lower():
            return team
        for keyword in team["keywords"]:
            if cleaned_input == keyword.replace(" ", "").lower():
                return team
    return None

# ============================================================
# 메인 검색 UI
# ============================================================

user_input = st.text_input(
    "🔍 팀 이름을 입력하세요",
    placeholder="예: LG / KIA / 삼성 / 한화"
)

if user_input:
    team = find_team(user_input, current_teams)

    if team is None:
        st.error("해당 팀을 찾을 수 없습니다.")
        st.info("💡 **입력 가능한 팀:** KT, 삼성, LG, KIA, 두산, 롯데, 한화, NC, SSG, 키움")
    else:
        # 팀 Header
        st.header(f"⚾ {team['name']} ({selected_date.year} 시즌)")
        if team["rank"] <= 5:
            st.success(f"🔥 기준일 당시 **{team['rank']}위** · 포스트시즌 진출권")
        else:
            st.warning(f"⚡ 기준일 당시 **{team['rank']}위** · 가을야구 경쟁 중")

        # 1. 순위 및 성적
        st.subheader("🏆 순위 & 시즌 성적")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("순위", f"{team['rank']}위")
        col2.metric("전적", f"{team['wins']}승 {team['draws']}무 {team['losses']}패")
        col3.metric("승률", team["win_rate"])
        col4.metric("연속", team["streak"])

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("소화 경기수", f"{team['games']}경기")
        col_b.metric("1위와 게임차", f"{team['games_behind']}경기")
        col_c.metric("팀 평균자책 / 타율", f"{team['era']} / {team['batting_avg']}")

        st.divider()

        # 2. 가을야구 예상 확률
        st.subheader("🍂 가을야구 예상 확률")
        probability = calculate_playoff_probability(team, current_teams)

        st.progress(probability / 100)
        st.markdown(f"### **{probability}%**")
        st.caption(f"※ {selected_date.strftime('%Y-%m-%d')} 기준 순위, 승률, 게임차를 반영한 수치입니다.")

        st.divider()

        # 3. 최근 경기 결과
        st.subheader("📰 최근 경기 결과")
        st.info(f"📌 **{team['recent_game']}**")

        st.caption(f"데이터 기준일: {selected_date.strftime('%Y년 %m월 %d일')}")
