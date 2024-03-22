__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
import pandas as pd
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import tempfile

API_KEY = os.getenv('OPENAI_API_KEY')

# 제목 설정
st.title("영어단어 공부하기")
st.write("---")

# 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 올려주세요!", type=['csv'])
st.write("---")

if uploaded_file is not None:
    # CSV 파일 로드
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    
    # 데이터 프레임에서 특정 열의 텍스트를 조합
    combined_texts = df.apply(lambda x: f"{x['question number']}. {x['question']} Answer: {x['answer']}", axis=1).tolist()

    # Embeddings 모델 초기화 (API 키 직접 사용)
    embeddings_model = OpenAIEmbeddings(api_key=API_KEY)

    # Chroma 객체로 문서 임베딩
    db = Chroma.from_documents(combined_texts, embeddings_model)

    # 질문 입력 및 처리
    st.header("궁금한 단어를 입력해보세요.")
    question = st.text_input('질문을 입력하세요')
    
    if st.button('질문하기') and question:
        with st.spinner('Wait for it...'):
            chat_model = ChatOpenAI(api_key=API_KEY, model_name="gpt-3.5-turbo", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(chat_model, retriever=db.as_retriever())
            result = qa_chain({"query": question})
            st.write(result["result"])
