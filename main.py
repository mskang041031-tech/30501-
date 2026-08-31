import streamlit as st
from datetime import date, timedelta
import random
import urllib.request
from html.parser import HTMLParser

# ============================================================
# Streamlit 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="KBO REAL-TIME DASHBOARD",
    page_icon="⚾",
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
# 날짜 컨트롤 & 검색 섹션 (2016~2026시즌 조회)
# ============================================================

today = date.today()
ten_years_ago = date(today.year - 10, 1, 1)

st.title("⚾ KBO REAL-TIME DASHBOARD")
st.caption("2016년~2026년 KBO 정규시즌 공식 데이터 및 가을야구 예측")

st.divider()

col_date, col_search = st.columns([1, 1])

with col_date:
    selected_date = st.date_input(
        "📅 기준일 선택",
        value=today,
        min_value=ten_years_ago,
        max_value=today,
        help="2016년부터 현재(2026년)까지의 성적을 선택하여 조회할 수 있습니다."
    )

with col_search:
    user_input = st.text_input(
        "🔍 팀명 검색",
        placeholder="팀명 입력 (예: LG, KIA, 삼성, KT)"
    )

# ============================================================
# 백업(Fallback) 데이터 생성기
# ============================================================

def get_fallback_kbo_rankings(target_date):
    """
    네트워크 차단, 비시즌, 크롤링 실패 시 앱 다운을 방지하는 백업 데이터입니다.
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

    seed_value = int(target_date.strftime("%Y%m%d"))
    rng = random.Random(seed_value)
    team_keys = list(base_teams.keys())
    rng.shuffle(team_keys)

    teams_data = {}
    for rank, key in enumerate(team_keys, start=1):
        games = 144 if target_date.month > 10 else max(10, int(target_date.month * 12))
        wins = int(games * (0.62 - (rank * 0.025)))
        losses = max(0, games - wins)
        draws = rng.randint(0, 3)
        win_rate = f"{(wins / (wins + losses)):.3f}" if (wins + losses) > 0 else ".000"
        gb = f"{(rank - 1) * 2.0:.1f}"

        teams_data[key] = {
            **base_teams[key],
            "rank": rank,
            "games": games,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": win_rate,
            "games_behind": gb,
            "streak": f"{rng.randint(1, 3)}승" if rank <= 5 else f"{rng.randint(1, 3)}패"
        }
    return teams_data

# ============================================================
# 파이썬 내장 라이브러리 기반 안전 크롤러
# ============================================================

class KBOTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_target_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table" and attrs_dict.get("id") == "regularTeamRecordList_table":
            self.in_target_table = True
        elif self.in_target_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in ["th", "td"]:
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_target_table = False
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag in ["th", "td"]:
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            text = data.strip()
            if text:
                self.current_row.append(text)

@st.cache_data(ttl=1800)
def fetch_kbo_rankings(target_date):
    """
    외부 라이브러리 없이 네이버 KBO 기록실을 안전하게 크롤링합니다.
    """
    date_str = target_date.strftime("%Y%m%d")
    url = f"https://sports.news.naver.com/kbaseball/record/index?category=kbo&date={date_str}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://sports.news.naver.com/kbaseball/index"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            html_content = response.read().decode('utf-8', errors='ignore')

        parser = KBOTableParser()
        parser.feed(html_content)

        if not parser.rows:
            return get_fallback_kbo_rankings(target_date), True

        keywords_map = {
            "KT": ["kt", "케이티", "kt위즈", "kt wiz"],
            "삼성": ["삼성라이온즈"],
            "LG": ["엘지", "lg트윈스"],
            "KIA": ["기아", "kia타이거즈"],
            "두산": ["두산베어스"],
            "롯데": ["롯데자이언츠"],
            "한화": ["한화이글스"],
            "NC": ["엔씨", "nc다이노스"],
            "SSG": ["쓱", "ssg랜더스", "SK", "sk와이번스"],
            "키움": ["키움히어로즈", "넥센", "넥센히어로즈"]
        }

        teams_data = {}
        for row in parser.rows:
            if len(row) >= 8:
                team_name = row[1]
                short_key = team_name
                for key, k_list in keywords_map.items():
                    if key in team_name or any(k in team_name.lower().replace(" ", "") for k in k_list):
                        short_key = key
                        break

                try:
                    games = int(row[2])
                    wins = int(row[3])
                    losses = int(row[4])
                    draws = int(row[5])
                    win_rate = row[6]
                    gb = row[7]
                    streak = row[8] if len(row) > 8 else "-"

                    teams_data[short_key] = {
                        "name": team_name,
                        "rank": len(teams_data) + 1,
                        "games": games,
                        "wins": wins,
                        "losses": losses,
                        "draws": draws,
                        "win_rate": win_rate,
                        "games_behind": gb,
                        "streak": streak,
                        "keywords": [short_key, team_name] + keywords_map.get(short_key, [])
                    }
                except ValueError:
                    continue

        if len(teams_data) >= 8:
            return teams_data, False
        else:
            return get_fallback_kbo_rankings(target_date), True

    except Exception:
        return get_fallback_kbo_rankings(target_date), True

# 데이터 로드
current_teams, is_fallback = fetch_kbo_rankings(selected_date)

# ============================================================
# 포스트시즌 확률 계산 및 검색 함수
# ============================================================

def calculate_playoff_probability(team, teams_data):
    if not teams_data:
        return 50
    
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
        score += (6 - rank) * 6
        score -= gb_from_5th * 3
    else:
        score -= (rank - 5) * 7
        score -= gb_from_5th * 4

    score = max(1, min(99, score))
    return round(score)

def find_team(query, teams_data):
    if not query or not teams_data:
        return None
    cleaned = query.replace(" ", "").lower()
    for team in teams_data.values():
        if cleaned in team["name"].lower().replace(" ", ""):
            return team
        for kw in team.get("keywords", []):
            if cleaned == kw.lower().replace(" ", ""):
                return team
    return None

selected_team = find_team(user_input, current_teams)

# ============================================================
# 사이드바 (전체 10개 구단 순위 요약)
# ============================================================

with st.sidebar:
    st.header("🏆 KBO 순위표")
    st.caption(f"기준일: {selected_date.strftime('%Y-%m-%d')}")
    
    if is_fallback:
        st.caption("⚠️ 네트워크 상태 또는 비시즌으로 예비 데이터가 전환되었습니다.")
    else:
        st.caption("🟢 네이버 실시간 데이터 반영 중")
        
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
        st.caption(f"승률: {win_rate} | 게임차: {gb}")
        
        if rank == 5:
            st.markdown("--- 🔻 **포스트시즌 커트라인** 🔻 ---")
        else:
            st.markdown("<hr style='margin: 3px 0 6px 0; border: none; border-top: 1px dashed #cccccc;'>", unsafe_allow_html=True)

# ============================================================
# 메인 대시보드 화면
# ============================================================

if user_input:
    if selected_team is None:
        st.error("해당 팀을 찾을 수 없습니다.")
        st.info("💡 **입력 가능 예시:** KT, 삼성, LG, KIA, 두산, 롯데, 한화, NC, SSG, 키움")
    else:
        team = selected_team
        
        st.markdown(f"""
            <div class="team-header-card">
                <h2 style="margin:0; padding-bottom: 5px;">⚾ {team['name']} <span style="font-size:0.9rem; font-weight:normal; opacity:0.8;">({selected_date.year} 시즌)</span></h2>
                <p style="margin:0; font-size:1rem; font-weight:600;">현재 순위: <strong>{team['rank']}위</strong> | {team['wins']}승 {team['draws']}무 {team['losses']}패 (승률 {team['win_rate']})</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📊 팀 성적 상세", "🍂 가을야구 예측"])

        with tab1:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("순위", f"{team['rank']}위")
            c2.metric("전적", f"{team['wins']}승 {team['draws']}무 {team['losses']}패")
            c3.metric("승률", team["win_rate"])
            c4.metric("연속 기록", team.get("streak", "-"))

            st.markdown("---")
            c_a, c_b = st.columns(2)
            c_a.metric("소화 경기수", f"{team['games']}경기")
            c_b.metric("1위와 게임차", f"{team['games_behind']}경기")

        with tab2:
            probability = calculate_playoff_probability(team, current_teams)
            st.markdown("##### 🏆 포스트시즌 예상 진출 확률")
            st.progress(probability / 100)
            
            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                st.metric("예상 진출 확률", f"{probability}%")
            with p_col2:
                if probability >= 70:
                    st.success("포스트시즌 진출 가능성이 매우 높습니다!")
                elif probability >= 40:
                    st.warning("치열한 5위 싸움이 진행 중입니다.")
                else:
                    st.error("가을야구 진출을 위해 반등이 필요합니다.")

else:
    st.info("👆 상단에서 **기준일**을 선택하고 **팀명**을 검색해 주세요. (사이드바에서 순위를 실시간으로 확인할 수 있습니다.)")
