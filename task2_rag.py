import os
import warnings
from dotenv import load_dotenv

# Hide annoying deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 🔒 KEY SAFETY CHECK
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("🔒 API key not found. Please check your .env file.")

print("🚀 Starting RAG Pipeline...\n")

# --- 1. LOAD THE DOCUMENT ---
pdf_file = "document.pdf"
if not os.path.exists(pdf_file):
    print(f"❌ Error: {pdf_file} not found. Please add a PDF to this folder!")
    exit()

print(f"📂 Loading {pdf_file}...")
loader = PyPDFLoader(pdf_file)
docs = loader.load()
print(f"✅ Loaded {len(docs)} pages.\n")

# --- 2. SPLIT TEXT INTO CHUNKS ---
print("✂️ Splitting text into manageable chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(f"✅ Created {len(splits)} text chunks.\n")

# --- 3. CREATE EMBEDDINGS & VECTOR STORE ---
print("🧠 Creating embeddings and storing in local ChromaDB...")
# ✅ UPDATED: Using the newest, officially supported Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=API_KEY)

vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)
print("✅ Vector store created and saved locally!\n")

# --- 4. SETUP THE MODERN RAG CHAIN ---
print("🔗 Setting up the Retrieval-Augmented Generation chain...")
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=API_KEY, temperature=0)

system_prompt = (
    "You are a helpful assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If the answer is not in the context, say 'I cannot find that information in the document'. "
    "Keep the answer concise and direct."
    "\n\nContext: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# --- 5. TEST THE RAG PIPELINE ---
# Change this question based on what's in your PDF!
query = "What is the vendor name and total amount mentioned in this document?" 
# (If it's a resume, change to: "What are the candidate's main skills and years of experience?")

print(f"❓ Asking: '{query}'\n")
response = rag_chain.invoke({"input": query})

print("✅ RAG Answer:")
print("-" * 50)
print(response["answer"])
print("-" * 50)