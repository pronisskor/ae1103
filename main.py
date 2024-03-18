import streamlit as st
from langchain_openai import ChatOpenAI


chat_model = ChatOpenAI()

st.title('AI English')

content = st.text_input('공부할 주제를 회화와 단어 중에 선택해주세요.')

if st.button('영어공부하기'):
    with st.spinner('Wait for it...'):
          result = chat_model.predict(content + "란 영어 단어 뜻을 간단히 설명해줘")
          st.write(result)
