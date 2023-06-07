import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz #import PyMuPDF
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

def main() :
    #Create a side bar and format it
    with st.sidebar:
        st.title("Policy at a Glance")  
    add_logo("http://placekitten.com/120/120")
    
    st.header('A tool to mine and comprehend the policy')
    
    #File upload function    
    uploaded_pdf = st.file_uploader("Load pdf: ", type=['pdf'])
    if uploaded_pdf is not None:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        #1. Extract the Title and Author
        metadata = doc.metadata 
        page_count = doc.page_count
        title = metadata['title']
        author = metadata['author']
        if title == "":
            st.write("Title: N/A")
        else:
            st.write("Title:", title)
        if title == "":
            st.write("Author: N/A")
        else:
            st.write("Author:", author)           
        st.write("Total pages:", page_count)
                      
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
