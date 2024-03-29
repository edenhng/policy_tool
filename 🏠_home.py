import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz #import PyMuPDF
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tabulate import tabulate
import openpyxl
import io

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def load_spacy_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp

def preprocess_text(text, nlp):
    doc = nlp(text)
    processed_tokens = []
    for token in doc:
        if token.is_alpha and not token.is_stop and token.lemma_ not in STOP_WORDS:
            lemma = token.lemma_.lower().strip()
            processed_tokens.append(lemma)
    processed_text = " ".join(processed_tokens) 
    return processed_text, processed_tokens

def get_top_org_entities(text, nlp):
    doc = nlp(text)
    org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    org_frequency_counts = {}
    
    for entity in org_entities:
        if entity in org_frequency_counts:
            org_frequency_counts[entity] += 1
        else:
            org_frequency_counts[entity] = 1
    
    sorted_org_frequencies = sorted(org_frequency_counts.items(), key=lambda x: x[1], reverse=True)
    top_org_entities = [entity for entity, frequency in sorted_org_frequencies[:5]]
    return top_org_entities

def extracted_text_from_pdf(pdf_file):
    text = ""
    for page in pdf_file:
        text += page.get_text()
    return text
    
def create_word_cloud_and_bar_chart(text):
    wordcloud = WordCloud(width=800, height=800, max_words=100, background_color='white').generate(text)
    word_frequencies = get_word_frequencies(text)
    df_word_frequencies = pd.DataFrame.from_dict(word_frequencies, orient='index', columns=['Frequency'])
    df_word_frequencies = df_word_frequencies.sort_values(by='Frequency', ascending=False).head(10)
    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    # Create a subplot for word cloud
    axes[0].imshow(wordcloud, interpolation='bilinear')
    axes[0].axis('off')
    # Create a subplot for bar chart
    sns.barplot(ax=axes[1], data=df_word_frequencies, x=df_word_frequencies.index, y='Frequency', palette='viridis')
    axes[1].set_xlabel('Word')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Top 10 Word Frequencies')
    # Rotate and align x-axis labels diagonally
    axes[1].tick_params(axis='x', pad=0)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    
def get_word_frequencies(processed_text):
    word_list = processed_text.split()
    word_counts = {}
    for word in word_list:
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts   

def main() :
    session_state = SessionState(pdf_file=None)
    #Create a side bar and format it
    add_logo("https://i.imgur.com/amZoFFM.jpg")
    
    st.title('Policy Overview Extractor')
    
    #File upload function    
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=['pdf'])
    if uploaded_pdf is not None:
        session_state.pdf_file = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    if session_state.pdf_file is not None:
        doc = session_state.pdf_file
        #1. Extract the Title and Author
        metadata = doc.metadata 
        page_count = doc.page_count
        modDate = metadata['modDate']
        year = modDate[2:6]
        title = metadata['title']
        author = metadata['author']
        if title is None:
            st.write("Title: N/A")
        else:
            st.write("Title:", title)
        if author is None:
            st.write("Author: N/A")
        else:
            st.write("Author:", author)           
        st.write("Total pages:", page_count)
        #Once the file is uploaded, convert into text and create a word cloud                  
        extracted_text = extracted_text_from_pdf(doc)
        nlp=load_spacy_model()
        processed_text = preprocess_text(extracted_text, nlp)[0]
        processed_tokens = preprocess_text(extracted_text, nlp)[1]
        working_pdf = session_state.pdf_file
        if 'processed_tokens' not in st.session_state:
            st.session_state.processed_tokens = processed_tokens
        if 'working_pdf' not in st.session_state:
            st.session_state.working_pdf = working_pdf
        create_word_cloud_and_bar_chart(processed_text)     
        word_frequencies = get_word_frequencies(processed_text)
        sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, frequency in sorted_word_frequencies[:5]]

        # Calculate top organization entities
        top_org_entities = get_top_org_entities(processed_text, nlp)
        # Format the top organization entities as a numbered list
        formatted_entities = "\n".join([f"{i+1}. {entity}" for i, entity in enumerate(top_org_entities)])

        # Display the new table with the specified columns
        table_data = {
            "Author": [author],
            "Year": [year],
            "Title": [title],
            "Page count": [page_count],
            "Region": [""],
            "Scope": [""],
            "Key words": [", ".join(top_keywords)],  # Join top_keywords into a single string
            "Summary": [""],
            "Top Mentioned Entities": [formatted_entities]  # Join top_org_entities into a single string
        }
        df = pd.DataFrame(table_data)
        st.table(df)
        
        # Save the Excel file to a BytesIO buffer
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)  # Move the buffer cursor to the beginning

        # Create the download button using the saved Excel file
        st.download_button(label="Download Excel File", data=excel_buffer, file_name="policy_overview.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


        
if __name__ == "__main__":
    st.set_page_config(page_title="Testing Policy Tool", layout="wide")
    main()
