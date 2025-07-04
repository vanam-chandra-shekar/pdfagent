import streamlit as st
import PyPDF2
import time
from agent import GeminiSummarizerAgent
from typing import Dict, List, Optional

st.set_page_config(
    page_title="PDF Summarizer with Gemini",
    page_icon="📄",
    layout="wide"
)

class PDFSummarizerUI:
    
    
    def __init__(self):
        self.agent = None
        self.initialize_session_state()
    
    def initialize_session_state(self):
        
        if 'extracted_text' not in st.session_state:
            st.session_state.extracted_text = None
        if 'current_result' not in st.session_state:
            st.session_state.current_result = None
    
    def extract_text_from_pdf(self, pdf_file, max_pages: int = 1) -> Optional[Dict]:
        
        try:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            total_pages = len(pdf_reader.pages)
            pages_to_process = min(max_pages, total_pages) if max_pages else total_pages
            
            full_text = ""
            for page_num in range(pages_to_process):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                full_text += page_text + "\n" if page_text else ""
            
            return {
                "full_text": full_text.strip(),
                "total_pages": total_pages,
                "pages_processed": pages_to_process,
                "total_words": len(full_text.split()) if full_text else 0
            }
            
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def render_sidebar(self) -> Optional[Dict]:
        
        st.sidebar.header("⚙️ Configuration")
        
        st.sidebar.info("🔑 Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
        
        api_key = st.sidebar.text_input(
            "Google Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        if not api_key:
            st.sidebar.warning("⚠️ Please enter your API key")
            return None
        
        
        if not self.agent or self.agent.api_key != api_key:
            self.agent = GeminiSummarizerAgent(api_key=api_key)
        
        
        if st.sidebar.button("🔍 Test API Key"):
            with st.spinner("Testing API key..."):
                if self.agent.validate_api_key():
                    st.sidebar.success("✅ API key is valid!")
                else:
                    st.sidebar.error("❌ Invalid API key")
        
        st.sidebar.markdown("---")
        
        
        st.sidebar.subheader("📝 Summary Settings")
        
        summary_type = st.sidebar.selectbox(
            "Summary Type",
            self.agent.get_supported_summary_types(),
            help="Choose the type of summary"
        )
        
        summary_length = st.sidebar.selectbox(
            "Summary Length",
            self.agent.get_supported_lengths(),
            index=1,
            help="Choose the length of summary"
        )
        
        focus_areas = st.sidebar.multiselect(
            "Focus Areas (Optional)",
            [
                "Key findings",
                "Recommendations", 
                "Data analysis",
                "Methodology",
                "Conclusions",
                "Future work"
            ],
            help="Select areas to focus on"
        )
        
        max_pages = st.sidebar.slider(
            "Max Pages to Process",
            min_value=1,
            max_value=50,
            value=10,
            help="Limit pages to process"
        )
        
        return {
            'api_key': api_key,
            'summary_type': summary_type,
            'summary_length': summary_length,
            'focus_areas': focus_areas,
            'max_pages': max_pages
        }
    
    def render_main_content(self, config: Optional[Dict]):
        
        st.title("📄 PDF Summarizer with Google Gemini")
        st.markdown("Upload a PDF file and get an AI-powered summary!")
        
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a PDF file to summarize"
        )
        
        if uploaded_file is not None:
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📄 File Name", uploaded_file.name)
            with col2:
                st.metric("📊 File Size", f"{uploaded_file.size / 1024:.1f} KB")
            
            
            if st.button("📝 Extract Text from PDF", type="secondary"):
                with st.spinner("Extracting text..."):
                    extraction_result = self.extract_text_from_pdf(
                        uploaded_file, 
                        config['max_pages'] if config else 10
                    )
                    
                    if extraction_result:
                        st.session_state.extracted_text = extraction_result
                        st.success(f"✅ Text extracted! Pages: {extraction_result['pages_processed']}")
                    else:
                        st.error("❌ Failed to extract text")
            
            
            if st.session_state.extracted_text:
                ext_data = st.session_state.extracted_text
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Pages Processed", ext_data['pages_processed'])
                with col2:
                    st.metric("Total Words", ext_data['total_words'])
                with col3:
                    st.metric("Characters", len(ext_data['full_text']))
                
                
                with st.expander("📄 Text Preview"):
                    st.text_area(
                        "Extracted Text",
                        ext_data['full_text'][:1000] + "..." if len(ext_data['full_text']) > 1000 else ext_data['full_text'],
                        height=200
                    )
                
                
                if config and st.button("🤖 Generate Summary", type="primary"):
                    with st.spinner("Generating summary..."):
                        result = self.agent.summarize_text(
                            ext_data['full_text'],
                            summary_type=config['summary_type'],
                            focus_areas=config['focus_areas'],
                            summary_length=config['summary_length']
                        )
                        
                        if result and result.get('success'):
                            st.session_state.current_result = result
                            st.success("✅ Summary generated!")
                        else:
                            st.error(f"❌ Failed to generate summary: {result.get('error', 'Unknown error')}")
        
        
        if st.session_state.current_result:
            result = st.session_state.current_result
            
            st.subheader("📋 Summary")
            st.write(result['summary'])
            
            
            with st.expander("ℹ️ Summary Information"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Summary Type:** {result['summary_type']}")
                    st.write(f"**Length:** {result['summary_length']}")
                with col2:
                    st.write(f"**Original Length:** {result['original_text_length']} chars")
                    st.write(f"**Summary Length:** {result['summary_text_length']} chars")
                
                if result['focus_areas']:
                    st.write(f"**Focus Areas:** {', '.join(result['focus_areas'])}")
            
            
            st.download_button(
                "💾 Download Summary",
                result['summary'],
                file_name=f"summary_{int(time.time())}.txt",
                mime="text/plain"
            )
    
    def run(self):
        
        config = self.render_sidebar()
        self.render_main_content(config)
