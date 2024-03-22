from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st
from langchain_openai import ChatOpenAI
import random

# 스트림릿 앱의 제목 설정
st.title("영어 단어 퀴즈")

# OpenAI API 키 환경 변수에서 로드
api_key = os.getenv('OPENAI_API_KEY')

# 파일 업로더 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

# 퀴즈를 위한 세션 상태 초기화
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = None
    st.session_state['correct_answer'] = None
    st.session_state['user_answer'] = None
    st.session_state['show_answer'] = False

def load_new_question():
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        random_row = df.sample(n=1)
        st.session_state['current_question'] = random_row.iloc[0]['question']
        st.session_state['correct_answer'] = random_row.iloc[0]['answer'].strip().lower()
        st.session_state['show_answer'] = False

def check_answer():
    st.session_state['user_answer'] = st.session_state['answer_input'].strip().lower()
    st.session_state['show_answer'] = True

# 새로운 퀴즈를 로드하는 버튼
st.button("새 퀴즈 시작", on_click=load_new_question)

# 질문 표시
if st.session_state['current_question']:
    st.write("퀴즈:", st.session_state['current_question'])

    # 사용자 답변 입력 및 제출 버튼
    st.session_state['answer_input'] = st.text_input("답을 입력하세요.")
    st.button("답변 제출", on_click=check_answer)

    # 정답 확인
    if st.session_state['show_answer']:
        if st.session_state['user_answer'] == st.session_state['correct_answer']:
            st.success("정답입니다!")
        else:
            st.error(f"틀렸습니다. 정답은 {st.session_state['correct_answer']}입니다.")
