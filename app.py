# UI for asking questions on the knowledge base
import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings
import google.generativeai as genai
from simple_vector_store import SimpleVectorStore as MilvusVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pages.app_admin import get_vector_store, get_text_chunks
from langchain.chains.combine_documents import create_stuff_documents_chain
import boto3
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from utils.auth import require_login, show_user_info
from utils.user_store import get_user_store_path


genai.configure(api_key=os.getenv("GENAI_API_KEY"))
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

nvidia_api_key = st.secrets["NVIDIA_API_KEY"]

def get_prompt_template():
    return PromptTemplate()

def get_chat_chain():
    prompt_template="""
    Answer the questions based on local konwledge base honestly

    Context:\n {context} \n
    Questions: \n {questions} \n

    Answers:
"""
    model=ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.3)
    # This is too slow
    #model = ChatNVIDIA(
    #    model="deepseek-ai/deepseek-r1",
    #    api_key=nvidia_api_key,
    #    temperature=0.7,
    #    top_p=0.8,
    #    max_tokens=4096
    #)
    #
    prompt=PromptTemplate(template=prompt_template, input_variables=["context", "questions"], output_variables=["answers"])
    chain = create_stuff_documents_chain(llm=model, prompt=prompt, document_variable_name="context")
    return chain

def user_input(user_question):
    # Use user-specific vector store
    user_store_path = get_user_store_path("./vector_store")
    vector_store = MilvusVectorStore(store_path=user_store_path)
    docs = vector_store.similarity_search(user_question)

    chain = get_chat_chain()

    response = chain.invoke({"context": docs, "questions": user_question})

    print(response)
    st.write("Reply: ",response)


def download_s3_bucket(bucket_name, download_dir):
    s3 = boto3.client('s3')
    
    # Ensure the download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Pagination in case the bucket has many objects
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            key = obj['Key']
            local_file_path = os.path.join(download_dir, key)
            
            # Create local directories if they don't exist
            if not os.path.exists(os.path.dirname(local_file_path)):
                os.makedirs(os.path.dirname(local_file_path))
                
            print(f"Downloading {key} to {local_file_path}")
            s3.download_file(bucket_name, key, local_file_path)

def download_faiss_from_s3():
    # Milvus data is managed by the Milvus server
    # Migration from S3-stored FAISS can be done with MilvusVectorStore.migrate_from_faiss()
    print("Milvus uses its own persistence. Migration from FAISS can be done if needed.")

def main():
    # Check authentication
    if not require_login("AI Learning Repository"):
        return
    
    # Show user info in sidebar
    show_user_info()
    
    st.title("🤖 AI Learning Repository")
    st.header("Your Personal AI Learning Knowledge Base")
    st.markdown("""
    Welcome to your AI Learning Repository! This is your central hub for:
    - 📚 **Learning Materials**: URLs, research papers, tutorials
    - 📝 **Personal Notes**: Your thoughts, summaries, and insights
    - 🔍 **Smart Search**: Find content using AI-powered semantic search
    
    Use the sidebar to navigate to different sections.
    """)

    # fix the empty vector store issue - use user-specific store
    get_vector_store(get_text_chunks("Loading some documents to build your knowledge base"))

    st.markdown("---")
    st.subheader("💬 Ask Questions")
    st.markdown("Ask questions about the content in your learning repository:")
    
    user_question = st.text_input(
        "Ask a question",
        placeholder="e.g., 'What are transformers?' or 'Explain attention mechanisms'"
    )
    
    if st.button("🔍 Search", type="primary") or user_question:
        if user_question:
            user_input(user_question)
        else:
            st.info("Please enter a question to search your knowledge base")
    
    
    st.markdown("---")
    st.markdown("""
    ### 📖 Quick Navigation
    Use the sidebar to access:
    - **📥 Bulk Import**: Import multiple URLs at once
    - **📝 Notes Manager**: Add and manage your learning notes
    - **🔍 Content Browser**: Browse and search your repository
    - **⚙️ Admin**: Manage documents, PDFs, audio, and video
    """)
    
    st.markdown("<div style='height:200px;'></div>", unsafe_allow_html=True)
    with st.expander("ℹ️ Tech Stack"):
        st.markdown("""
        - **Web Framework**: [Streamlit](https://streamlit.io/)
        - **LLM Model**: Gemini 2.0 Flash
        - **Vector Store**: Milvus
        - **Embeddings**: OpenAI text-embedding-3-large
        - **Framework**: LangChain for RAG, memory, and reasoning
        - **Document Processing**: PyPDF2, python-docx
        - **Audio/Video**: AssemblyAI, MoviePy
        """)    

if __name__ == "__main__":
    main()