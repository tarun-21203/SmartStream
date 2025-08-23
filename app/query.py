# query.py
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from . import transcribe
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

current_transcript = None

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
TRANSCRIPT_FILE_PATH = './current_transcript.txt'
# Initialize embeddings and LLM
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0
)

# In-memory store for the current transcript and its vector database
current_transcript = None
qa_chain = None

def initialize_qa_chain(transcript):
    """Initialize the QA chain with the given transcript."""
    vectorDB = FAISS.from_texts([transcript], embeddings)
    retriever = vectorDB.as_retriever()
    QA_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return QA_chain

def write_transcript_to_file(transcript):
    """Write the transcript to a file."""
    with open(TRANSCRIPT_FILE_PATH, 'w') as file:
        file.write(transcript)

def read_transcript_from_file():
    """Read the transcript from a file."""
    if os.path.exists(TRANSCRIPT_FILE_PATH):
        with open(TRANSCRIPT_FILE_PATH, 'r') as file:
            return file.read()
    return None

def transcribe_and_store(videoURL):
    global current_transcript
    result = transcribe.transcribe_func(videoURL)
    if 'Error' in result:
        return result
    current_transcript = result['summary']
    qa_chain = initialize_qa_chain(current_transcript)
    response = qa_chain.invoke({'query':'summarise the above information in 10 lines'})
    return {'summary':response['result']}

def query_transcript(user_query):
    global current_transcript
    if not current_transcript:
        return {'error': "No transcript available"}
    qa_chain = initialize_qa_chain(current_transcript)
    response = qa_chain.invoke({"query": user_query})
    return {'result': response["result"]}