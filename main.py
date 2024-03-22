import streamlit as st
import pandas as pd
import random

# 스트림릿 앱의 제목 설정
st.title("영어 단어 퀴즈")

# 파일 업로더 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # CSV 파일을 DataFrame으로 로드
    df = pd.read_csv(uploaded_file)
    
    # 세션 상태에 퀴즈 데이터와 현재 문제 번호, 정답 여부 기록이 없으면 초기화
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = df.to_dict('records')
        st.session_state.used_indexes = []  # 이미 사용된 문제의 인덱스를 저장할 리스트
        st.session_state.current_index = -1
        st.session_state.quiz_number = 0
        st.session_state.correct_answers = 0  # 정답 수
        st.session_state.incorrect_answers = 0  # 오답 수

    # 레이아웃을 두 개의 컬럼으로 나눔
    col1, col2 = st.columns([3, 1])

    with col1:
        # '새 퀴즈 시작' 버튼
        if st.button('새 퀴즈 시작'):
            if len(st.session_state.used_indexes) < len(st.session_state.quiz_data):
                # 이미 사용되지 않은 문제만 선택
                remaining_indexes = [i for i in range(len(st.session_state.quiz_data)) if i not in st.session_state.used_indexes]
                st.session_state.current_index = random.choice(remaining_indexes)
                st.session_state.used_indexes.append(st.session_state.current_index)
                # 입력 칸 초기화
                st.session_state.user_answer = ""
                # 퀴즈 번호 증가
                st.session_state.quiz_number += 1
            else:
                # 모든 문제를 다 풀었을 경우, 결과 요약
                st.write(f"모든 문제를 풀었습니다! 정답: {st.session_state.correct_answers}, 오답: {st.session_state.incorrect_answers}")
                # 사용된 인덱스와 정답/오답 수 초기화
                st.session_state.used_indexes = []  
                st.session_state.correct_answers = 0
                st.session_state.incorrect_answers = 0
                st.session_state.quiz_number = 0

    if st.session_state.current_index != -1:
        # 현재 질문과 정답 표시
        question = st.session_state.quiz_data[st.session_state.current_index]['question']
        answer = st.session_state.quiz_data[st.session_state.current_index]['answer'].strip().lower()

        st.write(f"문제 {st.session_state.quiz_number}: {question}")
        user_answer = st.text_input("답을 입력하세요.", value="", key=f"user_answer_{st.session_state.current_index}")

        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button('답변 제출', key=f"submit_{st.session_state.current_index}"):
                if user_answer.lower() == answer:
                    st.success("정답입니다!")
                    st.session_state.correct_answers += 1
                else:
                    st.error(f"틀렸습니다. 정답은 {answer}입니다.")
                    st.session_state.incorrect_answers += 1
