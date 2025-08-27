# query.py
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from . import transcribe
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

current_transcript = None
qa_chain = None

def initialize_qa_chain(transcript):
    """Initialize the QA chain with the given transcript."""
    global qa_chain
    vectorDB = FAISS.from_texts([transcript], embeddings)
    retriever = vectorDB.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain



def create_summary_from_chunks(transcript, max_chunk_size=2500):
    """Create a summary by processing transcript in chunks"""
    words = transcript.split()
    chunks = []
    current_chunk = []
    current_length = 0

    # Split into chunks
    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    # Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        try:
            # Create a temporary QA chain for this chunk
            temp_vectorDB = FAISS.from_texts([chunk], embeddings)
            temp_retriever = temp_vectorDB.as_retriever()
            temp_qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=temp_retriever,
                return_source_documents=True
            )

            response = temp_qa_chain.invoke({'query': f'Summarize this part of the video in 3-4 sentences'})
            chunk_summaries.append(response['result'])
        except Exception:
            # If AI fails, use first few sentences of the chunk
            sentences = chunk.split('.')[:3]
            chunk_summaries.append('. '.join(sentences) + '.')

    # Combine chunk summaries into final summary
    final_summary = "Video Summary:\n\n" + "\n\n".join(chunk_summaries)
    return final_summary

def transcribe_and_store(videoURL):
    global current_transcript, qa_chain
    result = transcribe.transcribe_func(videoURL)
    if 'Error' in result:
        return result

    current_transcript = result['summary']
    qa_chain = initialize_qa_chain(current_transcript)

    # Check if transcript is too long for direct processing
    if len(current_transcript) > 3000:
        try:
            # Try chunked summarization for large transcripts
            summary = create_summary_from_chunks(current_transcript)
            return {'summary': summary}
        except Exception as e:
            if "413" in str(e) or "Request too large" in str(e) or "rate_limit_exceeded" in str(e):
                # Create a manual summary from key parts
                words = current_transcript.split()
                # Take beginning, middle, and end portions
                beginning = ' '.join(words[:200])
                middle_start = len(words) // 2 - 100
                middle = ' '.join(words[middle_start:middle_start + 200])
                end = ' '.join(words[-200:])

                summary = f"Video Summary:\n\nBeginning: {beginning}...\n\nMiddle: {middle}...\n\nEnd: {end}..."
                return {'summary': summary}
            else:
                raise e
    else:
        # Normal processing for shorter transcripts
        try:
            response = qa_chain.invoke({'query': 'Provide a comprehensive summary of this video in 8-10 lines, highlighting the main topics, key points, and important information discussed.'})
            return {'summary': response['result']}
        except Exception as e:
            if "413" in str(e) or "Request too large" in str(e) or "rate_limit_exceeded" in str(e):
                # Create a basic summary from the transcript
                words = current_transcript.split()
                summary_text = ' '.join(words[:300]) + "..."
                return {'summary': f"Video Summary:\n\n{summary_text}"}
            else:
                raise e

def query_transcript(user_query):
    global current_transcript, qa_chain

    if not current_transcript:
        return {'error': "No transcript available. Please fetch a video first."}

    if not qa_chain:
        qa_chain = initialize_qa_chain(current_transcript)

    try:
        response = qa_chain.invoke({"query": user_query})
        return {'result': response["result"]}
    except Exception as e:
        if "413" in str(e) or "Request too large" in str(e) or "rate_limit_exceeded" in str(e):
            return {'result': "The transcript is too large for AI processing. Please try asking more specific questions or wait a moment for rate limits to reset."}
        else:
            return {'error': f"AI query failed: {str(e)}"}