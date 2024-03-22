__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
# import getpass
# import os
# import pandas as pd


#loder
loader = CSVLoader(file_path='./1-100.csv', encoding='utf-8')  
pages = loader.load_and_split()

# df = pd.read_csv('./1-100.csv', encoding='utf-8')
# pages = df

#Split
text_splitter = RecursiveCharacterTextSplitter(    
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.split_documents(pages)

#Embedding
embeddings_model = OpenAIEmbeddings()

# load it into Chroma
db = Chroma.from_documents(texts, embeddings_model)

# Question
question = "question number는 몇 개 있어?"
llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm,retriever=db.as_retriever())
result = qa_chain({"query": question})
print(result)

  
