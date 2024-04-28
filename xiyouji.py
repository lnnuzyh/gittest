from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import ModelScopeEmbeddings
from langchain.vectorstores import Chroma


raw_documents_1 = TextLoader('./file/text.txt').load()
raw_documents_2 = TextLoader('./file/sanguo.txt').load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)

documents_1 = text_splitter.split_documents(raw_documents_1)
documents_2 = text_splitter.split_documents(raw_documents_2)

documents = documents_1 + documents_2

print("documents nums:", documents.__len__())

model_id = "damo/nlp_corom_sentence-embedding_chinese-base"
embeddings = ModelScopeEmbeddings(model_id=model_id)

db = Chroma.from_documents(documents, embedding=embeddings, persist_directory='./file/chroma')

# 搜索
query = "小红是哪家的孩子？"
docs = db.similarity_search(query, k=5)

for doc in docs:
    print("===")
    print("metadata:", doc.metadata)
    print("page_content:", doc.page_content)