import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz #import PyMuPDF
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def load_spacy_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp

def preprocess_text(text, nlp):
    doc = nlp(text)
    filtered_token = [
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop and token.lemma_ not in STOP_WORDS
    ]
    processed_text = " ".join(filtered_token)
    return processed_text

def extracted_text_from_pdf(pdf_file):
    text = ""
    for page in pdf_file:
        text += page.get_text()
    return text
    
def create_word_cloud_and_bar_chart(text):
    wordcloud = WordCloud(width=800, height = 400, max_words=100, background_color='white').generate(text)
    word_frequencies = get_word_frequencies(text)
    df_word_frequencies = pd.DataFrame.from_dict(word_frequencies, orient='index', columns = ['Frequency'])
    df_word_frequencies = df_word_frequencies.sort_values(by='Frequency', ascending=False).head(10) 
    plt.figure(figsize=(15, 5))
    #Create a subplot for word cloud
    plt.subplot(1, 2, 1)
    plt.imshow(wordcloud, interpolation ='bilinear')                    
    plt.axis('off')
    #Create a subplot for bar chart
    plt.subplot(1, 2, 2)
    st.pyplot(plt)
    sns.barplot(data=df_word_frequencies, x = df_word_frequencies.index, y='Frequency', palette='viridis')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.title('Top 10 Word Frequencies')
    st.pyplot(plt)
    
def get_word_frequencies(processed_text):
    word_list = processed_text.split()
    word_counts = {}
    for word in word_list:
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts
                          
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
        #Once the file is uploaded, convert into text and create a word cloud                  
        extracted_text = extracted_text_from_pdf(doc)
        nlp=load_spacy_model()
        processed_text = preprocess_text(extracted_text, nlp)
        create_word_cloud_and_bar_chart(processed_text)     
        
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
