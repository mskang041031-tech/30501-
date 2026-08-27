import streamlit as st

# ============================================================
# KBO TEAM INFO
# 기준일 : 2026-08-27
# 데이터 출처 : KBO 공식 홈페이지
# ============================================================

st.set_page_config(
    page_title="KBO TEAM INFO",
    page_icon="⚾",
    layout="centered"
)

# ============================================================
# 2026 KBO 팀 데이터
# ============================================================

teams = {

    "KT": {
        "name": "KT 위즈",
        "keywords": ["KT", "kt", "케이티", "KT 위즈"],

        "rank": 1,
        "games": 110,
        "wins": 65,
        "losses": 42,
        "draws": 3,
        "win_rate": "0.607",
        "games_behind": "0.0",
        "streak": "1승",

        "batting_avg": "0.279",
        "era": "4.37",

        "recent_game": "8월 26일 | 두산 4 : 5 KT | 승리"
    },

    "삼성": {
        "name": "삼성 라이온즈",
        "keywords": ["삼성", "삼성 라이온즈", "삼성라이온즈"],

        "rank": 2,
        "games": 113,
        "wins": 66,
        "losses": 44,
        "draws": 3,
        "win_rate": "0.600",
        "games_behind": "0.5",
        "streak": "3승",

        "batting_avg": "0.278",
        "era": "4.22",

        "recent_game": "8월 26일 | 삼성 12 : 2 키움 | 승리"
    },

    "LG": {
        "name": "LG 트윈스",
        "keywords": ["LG", "lg", "엘지", "LG 트윈스", "LG트윈스"],

        "rank": 3,
        "games": 114,
        "wins": 63,
        "losses": 50,
        "draws": 1,
        "win_rate": "0.558",
        "games_behind": "5.0",
        "streak": "3승",

        "batting_avg": "0.269",
        "era": "4.87",

        "recent_game": "8월 26일 | NC 0 : 8 LG | 승리"
    },

    "KIA": {
        "name": "KIA 타이거즈",
        "keywords": ["KIA", "kia", "기아", "KIA 타이거즈", "KIA타이거즈"],

        "rank": 4,
        "games": 114,
        "wins": 62,
        "losses": 50,
        "draws": 2,
        "win_rate": "0.554",
        "games_behind": "5.5",
        "streak": "2승",

        "batting_avg": "0.274",
        "era": "4.45",

        "recent_game": "8월 26일 | 롯데 11 : 16 KIA | 승리"
    },

    "두산": {
        "name": "두산 베어스",
        "keywords": ["두산", "두산 베어스", "두산베어스"],

        "rank": 5,
        "games": 114,
        "wins": 59,
        "losses": 51,
        "draws": 4,
        "win_rate": "0.536",
        "games_behind": "7.5",
        "streak": "1패",

        "batting_avg": "0.270",
        "era": "3.68",

        "recent_game": "8월 26일 | 두산 4 : 5 KT | 패배"
    },

    "롯데": {
        "name": "롯데 자이언츠",
        "keywords": ["롯데", "롯데 자이언츠", "롯데자이언츠"],

        "rank": 6,
        "games": 112,
        "wins": 50,
        "losses": 60,
        "draws": 2,
        "win_rate": "0.455",
        "games_behind": "16.5",
        "streak": "3패",

        "batting_avg": "0.270",
        "era": "4.60",

        "recent_game": "8월 26일 | 롯데 11 : 16 KIA | 패배"
    },

    "한화": {
        "name": "한화 이글스",
        "keywords": ["한화", "한화 이글스", "한화이글스"],

        "rank": 7,
        "games": 111,
        "wins": 49,
        "losses": 59,
        "draws": 3,
        "win_rate": "0.454",
        "games_behind": "16.5",
        "streak": "3패",

        "batting_avg": "0.274",
        "era": "5.02",

        "recent_game": "8월 26일 | 한화 1 : 6 SSG | 패배"
    },

    "NC": {
        "name": "NC 다이노스",
        "keywords": ["NC", "nc", "엔씨", "NC 다이노스", "NC다이노스"],

        "rank": 8,
        "games": 108,
        "wins": 48,
        "losses": 58,
        "draws": 2,
        "win_rate": "0.453",
        "games_behind": "16.5",
        "streak": "4패",

        "batting_avg": "0.271",
        "era": "4.81",

        "recent_game": "8월 26일 | NC 0 : 8 LG | 패배"
    },

    "SSG": {
        "name": "SSG 랜더스",
        "keywords": ["SSG", "ssg", "쓱", "SSG 랜더스", "SSG랜더스"],

        "rank": 9,
        "games": 116,
        "wins": 47,
        "losses": 64,
        "draws": 5,
        "win_rate": "0.423",
        "games_behind": "20.0",
        "streak": "2승",

        "batting_avg": "0.262",
        "era": "5.46",

        "recent_game": "8월 26일 | 한화 1 : 6 SSG | 승리"
    },

    "키움": {
        "name": "키움 히어로즈",
        "keywords": ["키움", "키움 히어로즈", "키움히어로즈"],

        "rank": 10,
        "games": 118,
        "wins": 42,
        "losses": 73,
        "draws": 3,
        "win_rate": "0.365",
        "games_behind": "27.0",
        "streak": "1패",

        "batting_avg": "0.245",
        "era": "5.23",

        "recent_game": "8월 26일 | 삼성 12 : 2 키움 | 패배"
    }
}


# ============================================================
# 가을야구 예상 확률
# ============================================================
# KBO 공식 통계가 아니라 앱 자체 계산값.
#
# 기준:
# - 현재 순위
# - 승률
# - 5위와의 게임차
#
# 따라서 "공식 확률"이 아니라 "예상 확률"로 표시한다.
# ============================================================

def calculate_playoff_probability(team):

    rank = team["rank"]
    win_rate = float(team["win_rate"])
    games_behind = float(team["games_behind"])

    # 기본 점수
    score = win_rate * 100

    # 순위 보정
    if rank == 1:
        score += 25
    elif rank == 2:
        score += 20
    elif rank == 3:
        score += 15
    elif rank == 4:
        score += 10
    elif rank == 5:
        score += 5
    else:
        score -= (rank - 5) * 5

    # 게임차 보정
    score -= games_behind * 1.5

    # 0~99% 범위
    score = max(1, min(99, score))

    return round(score)


# ============================================================
# 팀 검색
# ============================================================

def find_team(user_input):

    user_input = user_input.strip().lower()

    for team_code, team in teams.items():

        # 팀 코드 검색
        if user_input == team_code.lower():
            return team

        # 팀 이름 및 별칭 검색
        for keyword in team["keywords"]:

            if user_input == keyword.lower():
                return team

    return None


# ============================================================
# 화면
# ============================================================

st.title("⚾ KBO TEAM INFO")

st.write(
    "팀 이름을 입력하면 2026 KBO 시즌 팀 정보를 확인할 수 있습니다."
)

st.caption("기준일: 2026년 8월 27일")

st.divider()


# ============================================================
# 검색창
# ============================================================

user_input = st.text_input(
    "🔍 팀 이름을 입력하세요",
    placeholder="예: LG / KIA / 삼성 / 한화"
)


if user_input:

    team = find_team(user_input)

    if team is None:

        st.error(
            "해당 팀을 찾을 수 없습니다."
        )

        st.write(
            "입력 가능한 팀: "
            "KT, 삼성, LG, KIA, 두산, 롯데, 한화, NC, SSG, 키움"
        )

    else:

        # ================================================
        # 팀 이름
        # ================================================

        st.header(f"⚾ {team['name']}")

        if team["rank"] <= 5:
            st.success(
                f"현재 {team['rank']}위 · 포스트시즌 진출권"
            )
        else:
            st.warning(
                f"현재 {team['rank']}위"
            )


        # ================================================
        # 순위 정보
        # ================================================

        st.subheader("🏆 순위 정보")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "현재 순위",
                f"{team['rank']}위"
            )

        with col2:
            st.metric(
                "1위와의 게임차",
                team["games_behind"]
            )

        with col3:
            st.metric(
                "연속",
                team["streak"]
            )


        # ================================================
        # 시즌 성적
        # ================================================

        st.subheader("📊 시즌 성적")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "경기",
                team["games"]
            )

        with col2:
            st.metric(
                "승",
                team["wins"]
            )

        with col3:
            st.metric(
                "무",
                team["draws"]
            )

        with col4:
            st.metric(
                "패",
                team["losses"]
            )


        # ================================================
        # 승률
        # ================================================

        st.subheader("📈 승률")

        st.metric(
            "승률",
            team["win_rate"]
        )


        # ================================================
        # 팀 기록
        # ================================================

        st.subheader("⚾ 팀 기록")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "팀 타율",
                team["batting_avg"]
            )

        with col2:
            st.metric(
                "팀 평균자책점",
                team["era"]
            )


        # ================================================
        # 가을야구 예상 확률
        # ================================================

        st.subheader("🍂 가을야구 예상 확률")

        probability = calculate_playoff_probability(team)

        st.progress(
            probability / 100
        )

        st.write(
            f"### {probability}%"
        )

        st.caption(
            "※ KBO 공식 확률이 아닌 현재 순위·승률·게임차를 "
            "이용한 앱 자체 예상값입니다."
        )


        # ================================================
        # 최근 경기
        # ================================================

        st.subheader("📰 가장 최근 경기")

        st.info(
            team["recent_game"]
        )


        # ================================================
        # 데이터 출처
        # ================================================

        st.divider()

        st.caption(
            "순위·팀 타율·팀 평균자책점·경기 결과: KBO 공식 홈페이지"
        )

        st.caption(
            "데이터 기준일: 2026-08-27"
        )
