import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz #import PyMuPDF

def main() :
    #Create a side bar and format it
    with st.sidebar:
        st.title("Policy at a Glance")  
    add_logo("http://placekitten.com/120/120")
    
    st.header('A tool to mine and comprehend the policy')
    
    #File upload function    
    uploaded_file = st.file_uploader("Load pdf: ", type=['pdf'])
    if uploaded_pdf is not None:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        #1. Extract the Title and Author
        metadata = doc.metadata                                               
        title = metadata['title']
        author = metadata['author']
        st.write("Title:", title)
        st.write("Author:", author)                                                        
                      
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
