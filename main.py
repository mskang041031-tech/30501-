import streamlit as st
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ============================================================
# Streamlit 페이지 설정
# ============================================================

st.set_page_config(
    page_title="KBO REAL-TIME DASHBOARD",
    page_icon="⚾",
    layout="centered"
)

# ============================================================
# 커스텀 CSS (카드 스타일)
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
# 날짜 선택 설정 (오늘 ~ 10년 전)
# ============================================================

today = date.today()
ten_years_ago = date(today.year - 10, 1, 1)

st.title("⚾ KBO REAL-TIME DASHBOARD")
st.caption("KBO 공식/실시간 성적 기반 10년 데이터 조회")

st.divider()

col_date, col_search = st.columns([1, 1])

with col_date:
    selected_date = st.date_input(
        "📅 기준일 선택",
        value=today,
        min_value=ten_years_ago,
        max_value=today,
        help="2016년부터 2026년 현재까지의 성적을 조회할 수 있습니다."
    )

with col_search:
    user_input = st.text_input(
        "🔍 팀명 검색",
        placeholder="팀명 입력 (예: LG, KIA, 삼성, KT)"
    )

# ============================================================
# 네이버 스포츠 KBO 실시간/과거 성적 크롤링 함수
# ============================================================

@st.cache_data(ttl=1800) # 30분 캐싱
def fetch_real_kbo_rankings(target_date):
    """
    선택한 날짜(YYYYMMDD)의 실제 KBO 순위 데이터를 네이버 스포츠에서 크롤링합니다.
    """
    date_str = target_date.strftime("%Y%m%d")
    url = f"https://sports.news.naver.com/kbaseball/record/index?category=kbo&date={date_str}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 순위 테이블 파싱
        rows = soup.select("#regularTeamRecordList_table tr")
        teams_data = {}
        
        # 팀별 키워드 매핑
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

        for row in rows:
            cols = row.find_all(["th", "td"])
            if len(cols) >= 9:
                team_name = cols[1].text.strip()
                
                # 팀 식별 키 찾기
                short_key = team_name
                for key, k_list in keywords_map.items():
                    if key in team_name or any(k in team_name.lower().replace(" ", "") for k in k_list):
                        short_key = key
                        break

                games = int(cols[2].text.strip() or 0)
                wins = int(cols[3].text.strip() or 0)
                losses = int(cols[4].text.strip() or 0)
                draws = int(cols[5].text.strip() or 0)
                win_rate = cols[6].text.strip()
                gb = cols[7].text.strip()
                streak = cols[8].text.strip() if len(cols) > 8 else "-"

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
                
        return teams_data
    except Exception as e:
        return None

# 실제 데이터 로드
current_teams = fetch_real_kbo_rankings(selected_date)

# ============================================================
# 가을야구 확률 계산 함수
# ============================================================

def calculate_playoff_probability(team, teams_data):
    if not teams_data:
        return 50
    
    rank = team["rank"]
    try:
        win_rate = float(team["win_rate"])
    except ValueError:
        win_rate = 0.500

    # 5위 팀의 게임차 찾기
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

# 팀 검색
def find_team(query, teams_data):
    if not query or not teams_data:
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
# 사이드바: 10개 구단 전체 순위표 (실제 데이터)
# ============================================================

with st.sidebar:
    st.header("🏆 KBO 공식 순위표")
    st.caption(f"기준일: {selected_date.strftime('%Y-%m-%d')}")
    st.divider()

    if current_teams:
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
    else:
        st.warning("선택한 날짜의 순위 데이터를 불러올 수 없습니다. (비시즌이거나 네트워크 연결 오류)")

# ============================================================
# 메인 화면
# ============================================================

if not current_teams:
    st.error("⚠️ 선택한 날짜에 해당하는 실제 KBO 경기/순위 데이터를 찾을 수 없습니다.")
    st.info("💡 KBO 정규시즌 기간(보통 3월 말 ~ 10월) 내 날짜를 선택해 보세요.")

elif user_input:
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
            c4.metric("연속", team["streak"])

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
    st.info("👆 상단에서 **기준일**을 선택하고 **팀명**을 검색해 주세요. (사이드바에서 실제 순위를 실시간으로 조회할 수 있습니다.)")
