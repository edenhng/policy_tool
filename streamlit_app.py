import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz #import PyMuPDF
    
def read_pdf(file):
    with fitz.open(file) as doc:
        doc = fitz.open(pdf_file)
        metadata = doc.metadata
        title = metadata['title']
        author = metadata['author']
        st.write("Title:", title)
        st.write("Author:", author)

def main() :
    #Create a side bar and format it
    with st.sidebar:
        st.title("Policy at a Glance")  
    add_logo("http://placekitten.com/120/120")
    
    st.header('A tool to mine and comprehend the policy')
    
    #File upload function    
    uploaded_file = st.file_uploader("Upload a pdf, docx or txt file")
    doc = fitz.open(uploaded_file)
 
      
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
