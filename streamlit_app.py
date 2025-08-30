import streamlit as st
from QAWithPDF.data_ingestion import load_data # type: ignore
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model
import logging

def main():
    st.set_page_config(
        page_title="QA with Documents",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("QA with Documents (Information Retrieval)")
    
    # UPLOAD FILE
    doc = st.file_uploader(
        "Upload your document", 
        type=['pdf', 'txt', 'docx'],
        help="Supported formats: PDF, TXT, DOCX"
    )
    
    # Display file info if uploaded
    if doc is not None:
        st.success(f"File uploaded: {doc.name} ({doc.size} bytes)")
    
    st.header("Ask Your Question")
    
    user_question = st.text_input(
        "Enter your question about the document:",
        placeholder="What is this document about?"
    )
    
    # Process button
    if st.button("Submit & Process", type="primary"):
        # Validation
        if doc is None:
            st.error("⚠️ Please upload a document first!")
            return
        
        if not user_question.strip():
            st.error("⚠️ Please enter a question!")
            return
        
        # Processing
        try:
            with st.spinner("Processing your document and question..."):
                # Step 1: Load document
                with st.status("Loading document...") as status:
                    document = load_data(doc)
                    if document is None:
                        raise ValueError("Failed to load document")
                    status.update(label="Document loaded successfully!", state="complete")
                
                # Step 2: Load model
                with st.status("Loading AI model...") as status:
                    model = load_model()
                    if model is None:
                        raise ValueError("Failed to load model")
                    status.update(label="Model loaded successfully!", state="complete")
                
                # Step 3: Create embeddings
                with st.status("Creating embeddings and query engine...") as status:
                    query_engine = download_gemini_embedding(model, document)
                    if query_engine is None:
                        raise ValueError("Failed to create query engine")
                    status.update(label="Query engine ready!", state="complete")
                
                # Step 4: Query
                with st.status("Processing your question...") as status:
                    response = query_engine.query(user_question)
                    if response is None or not hasattr(response, 'response'):
                        raise ValueError("No response generated")
                    status.update(label="Question processed!", state="complete")
            
            # Display results
            st.success("✅ Processing completed!")
            
            # Response section
            st.subheader("Answer:")
            st.write(response.response)
            
            # Optional: Display sources if available
            if hasattr(response, 'source_nodes') and response.source_nodes:
                with st.expander("📖 Source Information"):
                    for i, node in enumerate(response.source_nodes, 1):
                        st.write(f"**Source {i}:**")
                        st.write(node.text[:200] + "..." if len(node.text) > 200 else node.text)
                        st.write("---")
        
        except FileNotFoundError as e:
            st.error(f"❌ File error: {str(e)}")
            st.info("Make sure all required modules are in the correct location.")
        
        except ImportError as e:
            st.error(f"❌ Import error: {str(e)}")
            st.info("Check if all dependencies are installed: `pip install -r requirements.txt`")
        
        except ValueError as e:
            st.error(f"❌ Processing error: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.info("Please check the console for detailed error information.")
            logging.error(f"Streamlit app error: {str(e)}", exc_info=True)
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip**: Upload a document and ask specific questions about its content!")

if __name__ == "__main__":
    main()