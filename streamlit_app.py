import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz #import PyMuPDF
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

def load_spacy_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp

def preprocess_text(text, nlp):
    doc = nlp(text)
    filtered_token = [
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop and token.lemma_ not in STOP_WORDS
    ]
    processed_text = " ".join(filtered_tokens)
    return processed_text
        
def create_word_cloud(text):
    wordcloud = WordCloud(width=800, height = 400, max_words=100, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation ='bilinear')                    
    plt.axis('off')
    st.pyplot(plt)
    st.write('Check if it works?')
                          
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
        text = "AA"
        st.write(text)
        #Once the file is uploaded, convert into text and create a word cloud                  
        #text = "AA"
        #for page in doc:
            #text += page.get_text()
            #return text
        #st.write(text)
        #nlp=load_spacy_model()
        #processed_text = preprocess_text(text, nlp)
        #create_word_cloud(processed_text)     
        #st.write('Why it is up to this one?')
    
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
