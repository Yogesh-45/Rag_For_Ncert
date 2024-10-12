from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Weaviate
import weaviate


import os
from dotenv import load_dotenv

load_dotenv()
WEAVIATE_API_KEY= os.getenv('WEAVIATE_API_KEY')
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')


WEAVIATE_URL = 'https://npoxyaaxr5k1km0njkybta.c0.asia-southeast1.gcp.weaviate.cloud'

client = weaviate.Client(
    url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY)
)


embedding_model = OpenAIEmbeddings(api_key= OPENAI_API_KEY)


loader = PyPDFLoader("D:/yogi/LLM/sarvam/iesc111.pdf")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs = text_splitter.split_documents(pages)
vector_db = Weaviate.from_documents(docs, embedding_model, client=client, by_text=False)

def RAG(query, history= None):

    template="""You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    Try to keep the answer short and concise.
    Question: {question}
    Context: {context}
    Answer:
    """

    llm = ChatOpenAI(temperature=0, )

    prompt= ChatPromptTemplate.from_template(template)
    retriever = vector_db.as_retriever()
    output_parser=StrOutputParser()


    rag_chain = (
    {"context": retriever,  "question": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
    )

    answer= rag_chain.invoke(input= query)

    print(answer)

    return answer