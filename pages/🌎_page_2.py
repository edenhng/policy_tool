import streamlit as st
import spacy
import fitz #import PyMUPDF
from spacy.lang.en.stop_words import STOP_WORDS
import string
import gensim
from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# Load the Spacy English model
nlp = spacy.load('en_core_web_sm')

def extracted_text_from_pdf(file):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    return st.write(text)
    
def preprocess_document(pdf_file):
    # Extract text from the PDF file
    text = extracted_text_from_pdf(pdf_file)

    # Tokenize the document
    doc = nlp(text)

    # Remove stop words, punctuation, and lemmatize the tokens
    processed_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct or token.is_space:
            continue
        lemma = token.lemma_.lower().strip()
        processed_tokens.append(lemma)

    return processed_tokens

def run_lda(pdf_file):
    # Preprocess the document
    tokens = preprocess_document(pdf_file)

    # Create a dictionary from the tokens
    dictionary = corpora.Dictionary([tokens])

    # Create a corpus using the dictionary
    corpus = [dictionary.doc2bow(tokens)]

    # Create the LDA model
    lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=10)

    # Compute the coherence score
    coherence_model = gensim.models.CoherenceModel(model=lda_model, texts=[tokens], dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()

    # Visualize the topics
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.display(vis_data)

    # Print the coherence score
    st.write("Coherence Score: ", coherence_score)

# Streamlit app
def main():
    st.title("LDA Topic Modeling")
    #Retrieve the stored PDF file from the session state
    session_state = get_session_state()
    pdf_file = session_state.get('pdf_file', None) #Retrieve the 'pdf_file' attribute from session state
    run_lda(pdf_file)

def get_session_state():
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = {'pdf_file': None}
    return st.session_state['session_state']

if __name__ == "__main__":
    main()

