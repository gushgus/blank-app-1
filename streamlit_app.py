import streamlit as st
import random
import time # 시간 측정을 위해 time 라이브러리를 가져옵니다.
from st_keyup import st_keyup

# --- 앱 초기 설정 ---
st.set_page_config(page_title="분류하기 게임", page_icon="⏰")

# --- 게임 초기화 함수 ---
# 게임을 시작하거나 재시작할 때 호출되는 함수입니다.
def initialize_game():
    st.session_state.score = 0
    st.session_state.box_stack = [random.choice(['노란색', '파란색']) for _ in range(5)]
    # [추가됨] 게임 시작 시간을 기록합니다.
    st.session_state.start_time = time.time()
    # [추가됨] 게임 오버 상태를 관리하는 플래그를 False로 설정합니다.
    st.session_state.game_over = False

# --- 세션 상태(Session State) 최초 초기화 ---
# 앱이 처음 로드될 때만 게임을 초기화합니다.
if 'score' not in st.session_state:
    initialize_game()

# --- 분류 처리 함수 ---
def handle_classification(direction):
    if not st.session_state.box_stack:
        return

    current_box_color = st.session_state.box_stack[0]
    correct_condition = (current_box_color == '파란색' and direction == '왼쪽') or \
                        (current_box_color == '노란색' and direction == '오른쪽')

    if correct_condition:
        st.session_state.score += 1
        # 게임 오버 시에는 성공/실패 메시지를 보여주지 않습니다.
        # st.success("정답! 🎉") # 게임 속도감을 위해 잠시 비활성화
    # else:
        # st.warning("실수! 🤔") # 게임 속도감을 위해 잠시 비활성화

    st.session_state.box_stack.pop(0)
    new_color = random.choice(['노란색', '파란색'])
    st.session_state.box_stack.append(new_color)

# --- 앱 UI 구성 ---
st.title("⏰ 30초 타임어택! 분류하기")
st.write("파란색 박스는 왼쪽, 노란색 박스는 오른쪽으로 보내주세요!")
st.info("**⌨️ 키보드의 좌/우 방향키를 눌러서 빠르게 분류할 수 있어요!**")

# --- [수정됨] 시간 및 점수 표시 ---
# 남은 시간을 계산하고 게임오버 상태를 확인합니다.
if not st.session_state.game_over:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = 30 - elapsed_time
    if remaining_time <= 0:
        st.session_state.game_over = True
        # 시간이 다 되면 즉시 rerun하여 게임오버 화면을 표시합니다.
        st.rerun()
else:
    remaining_time = 0

# 점수와 시간을 나란히 보여주기 위해 컬럼을 사용합니다.
score_col, time_col = st.columns(2)
score_col.header(f"점수: {st.session_state.score}점")
# st.metric을 사용해 남은 시간을 시각적으로 강조합니다.
time_col.metric("남은 시간", f"{max(0, int(remaining_time))}초")


# --- [수정됨] 게임 상태에 따른 화면 분기 ---
if st.session_state.game_over:
    # 게임 오버 시 메시지를 보여줍니다.
    st.error(f"시간 종료! 최종 점수는 {st.session_state.score}점 입니다. 🏆")
    st.balloons()
else:
    # --- 게임이 진행 중일 때만 입력 및 박스를 표시합니다. ---
    pressed_key = st_keyup(key=["ArrowLeft", "ArrowRight"], debounce=200)

    if pressed_key == "ArrowLeft":
        handle_classification('왼쪽')
        st.rerun()
    elif pressed_key == "ArrowRight":
        handle_classification('오른쪽')
        st.rerun()

    # 박스 시각화
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        for i, color in enumerate(st.session_state.box_stack):
            background_color = "blue" if color == "파란색" else "yellow"
            text_color = "white" if color == "파란색" else "black"
            border_style = "4px solid #FF4B4B" if i == 0 else "2px solid grey"

            st.markdown(
                f"""
                <div style="background-color: {background_color}; color: {text_color}; padding: 20px;
                border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold;
                margin-bottom: 10px; border: {border_style};">
                    {color}
                </div>
                """, unsafe_allow_html=True
            )

    # 분류 버튼
    left_col, right_col = st.columns(2)
    if left_col.button('⬅️ 왼쪽', use_container_width=True):
        handle_classification('왼쪽')
        st.rerun()

    if right_col.button('오른쪽 ➡️', use_container_width=True):
        handle_classification('오른쪽')
        st.rerun()

# --- 게임 초기화 버튼 ---
# 게임 상태와 상관없이 항상 표시됩니다.
if st.button('게임 초기화 / 다시 시작', use_container_width=True):
    initialize_game() # 게임 초기화 함수 호출
    st.rerun()