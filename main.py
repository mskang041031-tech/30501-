import streamlit as st


# ==========================================
# KBO 팀 데이터
# ==========================================
# 실제 제출 전 KBO 공식 홈페이지에서 최신 데이터를 확인하여
# 아래 숫자들을 수정하면 됩니다.

teams = {

    "LG 트윈스": {
        "keywords": ["LG", "엘지", "LG트윈스", "LG 트윈스"],

        "rank": 1,
        "games": 100,
        "wins": 60,
        "draws": 2,
        "losses": 38,
        "win_rate": "0.612",
        "games_behind": "0.0",
        "streak": "3승",
        "batting_average": "0.280",
        "era": "3.45",
        "playoff": 95,
        "recent_game": "LG 5 : 3 KT — 승리"
    },

    "KT 위즈": {
        "keywords": ["KT", "케이티", "KT위즈", "KT 위즈"],

        "rank": 2,
        "games": 100,
        "wins": 58,
        "draws": 2,
        "losses": 40,
        "win_rate": "0.592",
        "games_behind": "2.0",
        "streak": "1승",
        "batting_average": "0.275",
        "era": "3.60",
        "playoff": 90,
        "recent_game": "KT 3 : 5 LG — 패배"
    },

    "KIA 타이거즈": {
        "keywords": ["KIA", "기아", "KIA타이거즈", "KIA 타이거즈"],

        "rank": 3,
        "games": 100,
        "wins": 55,
        "draws": 2,
        "losses": 43,
        "win_rate": "0.561",
        "games_behind": "5.0",
        "streak": "2승",
        "batting_average": "0.270",
        "era": "3.80",
        "playoff": 85,
        "recent_game": "KIA 6 : 2 삼성 — 승리"
    },

    "삼성 라이온즈": {
        "keywords": ["삼성", "삼성라이온즈", "삼성 라이온즈"],

        "rank": 4,
        "games": 100,
        "wins": 52,
        "draws": 3,
        "losses": 45,
        "win_rate": "0.536",
        "games_behind": "7.5",
        "streak": "1패",
        "batting_average": "0.268",
        "era": "4.05",
        "playoff": 75,
        "recent_game": "삼성 2 : 6 KIA — 패배"
    },

    "두산 베어스": {
        "keywords": ["두산", "두산베어스", "두산 베어스"],

        "rank": 5,
        "games": 100,
        "wins": 50,
        "draws": 2,
        "losses": 48,
        "win_rate": "0.510",
        "games_behind": "10.0",
        "streak": "1승",
        "batting_average": "0.260",
        "era": "4.20",
        "playoff": 65,
        "recent_game": "두산 4 : 3 NC — 승리"
    },

    "롯데 자이언츠": {
        "keywords": ["롯데", "롯데자이언츠", "롯데 자이언츠"],

        "rank": 6,
        "games": 100,
        "wins": 48,
        "draws": 2,
        "losses": 50,
        "win_rate": "0.490",
        "games_behind": "12.0",
        "streak": "2패",
        "batting_average": "0.258",
        "era": "4.35",
        "playoff": 50,
        "recent_game": "롯데 2 : 5 SSG — 패배"
    },

    "한화 이글스": {
        "keywords": ["한화", "한화이글스", "한화 이글스"],

        "rank": 7,
        "games": 100,
        "wins": 47,
        "draws": 2,
        "losses": 51,
        "win_rate": "0.480",
        "games_behind": "13.0",
        "streak": "1승",
        "batting_average": "0.255",
        "era": "4.40",
        "playoff": 45,
        "recent_game": "한화 3 : 4 키움 — 패배"
    },

    "SSG 랜더스": {
        "keywords": ["SSG", "쓱", "SSG랜더스", "SSG 랜더스"],

        "rank": 8,
        "games": 100,
        "wins": 45,
        "draws": 3,
        "losses": 52,
        "win_rate": "0.464",
        "games_behind": "15.0",
        "streak": "1승",
        "batting_average": "0.250",
        "era": "4.50",
        "playoff": 30,
        "recent_game": "SSG 5 : 2 롯데 — 승리"
    },

    "NC 다이노스": {
        "keywords": ["NC", "엔씨", "NC다이노스", "NC 다이노스"],

        "rank": 9,
        "games": 100,
        "wins": 42,
        "draws": 2,
        "losses": 56,
        "win_rate": "0.429",
        "games_behind": "18.0",
        "streak": "3패",
        "batting_average": "0.245",
        "era": "4.70",
        "playoff": 20,
        "recent_game": "NC 3 : 4 두산 — 패배"
    },

    "키움 히어로즈": {
        "keywords": ["키움", "키움히어로즈", "키움 히어로즈"],

        "rank": 10,
        "games": 100,
        "wins": 35,
        "draws": 3,
        "losses": 62,
        "win_rate": "0.361",
        "games_behind": "25.0",
        "streak": "2승",
        "batting_average": "0.235",
        "era": "5.00",
        "playoff": 5,
        "recent_game": "키움 4 : 3 한화 — 승리"
    }
}


# ==========================================
# 페이지 설정
# ==========================================

st.set_page_config(
    page_title="KBO 팀 정보",
    page_icon="⚾",
    layout="centered"
)


# ==========================================
# 화면 디자인
# ==========================================

st.title("⚾ KBO TEAM INFO")

st.write(
    "한국프로야구 팀의 시즌 기록을 검색해보세요."
)

st.divider()


# ==========================================
# 팀 이름 입력
# ==========================================

team_input = st.text_input(
    "🔍 팀 이름을 입력하세요",
    placeholder="예: LG, KIA, 한화, 삼성"
)


# ==========================================
# 팀 검색 함수
# ==========================================

def find_team(user_input):

    user_input = user_input.strip().lower()

    for team_name, team in teams.items():

        # 정식 팀 이름으로 검색
        if user_input == team_name.lower():
            return team_name, team

        # 별칭으로 검색
        for keyword in team["keywords"]:

            if user_input == keyword.lower():
                return team_name, team

    return None, None


# ==========================================
# 검색
# ==========================================

if team_input:

    team_name, team = find_team(team_input)

    if team:

        # -----------------------------
        # 팀 이름
        # -----------------------------

        st.header(f"⚾ {team_name}")

        st.success(
            f"현재 {team['rank']}위"
        )


        # -----------------------------
        # 기본 순위 정보
        # -----------------------------

        st.subheader("🏆 순위 정보")

        col1, col2 = st.columns(2)

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


        # -----------------------------
        # 시즌 성적
        # -----------------------------

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


        # -----------------------------
        # 승률 / 연속
        # -----------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "승률",
                team["win_rate"]
            )

        with col2:
            st.metric(
                "연속 기록",
                team["streak"]
            )


        # -----------------------------
        # 팀 기록
        # -----------------------------

        st.subheader("⚾ 팀 기록")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "팀 타율",
                team["batting_average"]
            )

        with col2:
            st.metric(
                "팀 평균자책점",
                team["era"]
            )


        # -----------------------------
        # 가을야구 확률
        # -----------------------------

        st.subheader("🍂 가을야구 예상 확률")

        probability = team["playoff"]

        st.progress(
            probability / 100
        )

        st.write(
            f"**{probability}%**"
        )


        # -----------------------------
        # 최근 경기
        # -----------------------------

        st.subheader("📰 가장 최근 경기")

        st.info(
            team["recent_game"]
        )


        # -----------------------------
        # 출처
        # -----------------------------

        st.divider()

        st.caption(
            "순위 및 팀 기록 데이터는 KBO 공식 홈페이지를 기준으로 입력합니다."
        )

        st.caption(
            "가을야구 확률은 KBO 공식 통계가 아닌 앱 자체 예상값입니다."
        )

    else:

        st.error(
            "❌ 해당 팀을 찾을 수 없습니다."
        )

        st.write(
            "예: LG, KIA, 삼성, 두산, 롯데, 한화, SSG, NC, KT, 키움"
        )
