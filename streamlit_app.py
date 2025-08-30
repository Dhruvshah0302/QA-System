import streamlit as st
import sys
import os
import logging
from pathlib import Path

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Try to import LlamaIndex
try:
    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
    from llama_index.core.node_parser import SimpleNodeParser
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False

# Alternative document processing without LlamaIndex
import PyPDF2  # Uncommented this line
import docx
from io import BytesIO

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        return file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return ""

def load_data_from_upload(uploaded_file):
    """Load data from uploaded file"""
    try:
        logging.info("Data loading started...")
        
        if uploaded_file is None:
            return ""
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            text = extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file format")
            return ""
        
        logging.info("Data loading completed...")
        return text
        
    except Exception as e:
        logging.error(f"Exception in loading data: {str(e)}")
        st.error(f"Error loading data: {str(e)}")
        return ""

def load_data_from_directory(data_path="Data"):
    """Load documents from directory using LlamaIndex if available"""
    try:
        logging.info("Directory data loading started...")
        
        if not LLAMA_INDEX_AVAILABLE:
            st.error("LlamaIndex not available. Please install it: pip install llama-index")
            return []
        
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            st.warning(f"Created directory: {data_path}")
            return []
            
        loader = SimpleDirectoryReader(data_path)
        documents = loader.load_data()
        logging.info("Directory data loading completed...")
        return documents
        
    except Exception as e:
        logging.error(f"Exception in loading directory data: {str(e)}")
        st.error(f"Error loading from directory: {str(e)}")
        return []

def simple_qa_system(document_text, question):
    """Simple Q&A system using text matching"""
    if not document_text or not question:
        return "Please upload a document and ask a question."
    
    # Convert to lowercase for better matching
    question_lower = question.lower()
    
    # Split document into sentences
    sentences = [s.strip() for s in document_text.split('.') if s.strip()]
    
    # Find sentences that contain keywords from the question
    question_words = set(question_lower.split())
    relevant_sentences = []
    
    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        # Check if question words appear in the sentence
        common_words = question_words.intersection(sentence_words)
        if len(common_words) > 0:
            relevance_score = len(common_words) / len(question_words)
            relevant_sentences.append((sentence, relevance_score))
    
    if relevant_sentences:
        # Sort by relevance and return top sentences
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in relevant_sentences[:3]]
        return '. '.join(top_sentences) + '.'
    else:
        return "I couldn't find specific information related to your question in the document. Try rephrasing your question or check if the document contains the information you're looking for."

def main():
    st.title("QA with Documents (Information Retrieval)")
    
    # Display LlamaIndex status
    if LLAMA_INDEX_AVAILABLE:
        st.success("✅ LlamaIndex is available")
    else:
        st.warning("⚠️ LlamaIndex not available - using basic text matching")
    
    # Initialize session state
    if 'document_text' not in st.session_state:
        st.session_state.document_text = ""
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    
    # File upload section
    st.header("📁 Upload File")
    
    # Two options: Upload or Directory
    tab1, tab2 = st.tabs(["📤 Upload File", "📂 Load from Directory"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Upload your document",
            type=['pdf', 'txt', 'docx'],
            help="Supported formats: PDF, TXT, DOCX"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing document..."):
                document_text = load_data_from_upload(uploaded_file)
                st.session_state.document_text = document_text
                
            if document_text:
                st.success(f"✅ Document processed successfully! ({len(document_text)} characters)")
                
                # Show preview
                with st.expander("📖 Document Preview"):
                    st.text_area("Document content (first 1000 characters):", 
                               value=document_text[:1000] + ("..." if len(document_text) > 1000 else ""),
                               height=200,
                               disabled=True)
    
    with tab2:
        data_directory = st.text_input("Data Directory Path", value="Data")
        
        if st.button("Load from Directory"):
            with st.spinner(f"Loading documents from {data_directory}..."):
                documents = load_data_from_directory(data_directory)
                st.session_state.documents = documents
                
                if documents:
                    # Combine all document texts
                    combined_text = "\n\n".join([doc.text for doc in documents])
                    st.session_state.document_text = combined_text
                    st.success(f"✅ Loaded {len(documents)} document(s) from directory")
                else:
                    st.warning(f"No documents found in {data_directory}")
    
    # Q&A Section
    if st.session_state.document_text:
        st.header("❓ Ask Questions")
        
        question = st.text_input("Enter your question about the document:")
        
        if st.button("Get Answer", type="primary"):
            if question:
                with st.spinner("Finding answer..."):
                    answer = simple_qa_system(st.session_state.document_text, question)
                    
                st.subheader("📝 Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question.")
        
        # Pre-defined questions
        st.subheader("💡 Quick Questions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 What is this document about?"):
                answer = simple_qa_system(st.session_state.document_text, "main topic subject about")
                st.write("**Answer:**", answer)
        
        with col2:
            if st.button("📊 What are the key points?"):
                answer = simple_qa_system(st.session_state.document_text, "key points important main findings")
                st.write("**Answer:**", answer)
        
        # Document stats
        st.header("📊 Document Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Characters", len(st.session_state.document_text))
        with col2:
            st.metric("Words", len(st.session_state.document_text.split()))
        with col3:
            sentences = len([s for s in st.session_state.document_text.split('.') if s.strip()])
            st.metric("Sentences", sentences)
    
    else:
        st.info("👆 Please upload a document to start asking questions.")
        
        # Instructions
        st.header("🚀 Getting Started")
        st.write("""
        **Option 1: Upload a single file**
        - Click on "Upload File" tab
        - Choose a PDF, TXT, or DOCX file
        - Start asking questions!
        
        **Option 2: Load from directory** 
        - Put your documents in the "Data" folder
        - Click "Load from Directory"
        - Ask questions about all documents
        """)
        
        if not LLAMA_INDEX_AVAILABLE:
            st.header("📦 Installation Required")
            st.code("""
            pip install llama-index PyPDF2 python-docx
            """)
            st.write("Run the above command in your terminal to get enhanced features.")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About This App")
        st.write("This QA system allows you to upload documents and ask questions about their content.")
        
        st.header("🔧 Features")
        st.write("- Upload PDF, TXT, DOCX files")
        st.write("- Load multiple documents from directory")
        st.write("- Intelligent text search")
        st.write("- Document statistics")
        
        if st.session_state.document_text:
            st.header("📈 Current Session")
            st.write(f"Document loaded: ✅")
            st.write(f"Length: {len(st.session_state.document_text)} chars")

if __name__ == "__main__":
    main()