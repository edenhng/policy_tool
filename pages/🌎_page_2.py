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

def extracted_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text
    
def preprocess_document(pdf_file):
    # Error handling &   # Extract text from the PDF file
    if 'working_file' in st.session_state:
        working_file = st.session_state['working_file']
        # Extract text from the PDF file
        text = extracted_text_from_pdf(working_file)
  
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
    st.write(corpus)
    # Create the LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, random_state=100, 
                                                update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

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
    if 'working_file' in st.session_state:
        working_file = st.session_state['working_file']
        st.write("Found a working File from Main Page")
        run_lda(working_file)
    else:
        st.info("No working file found from Page 1.")
    
        
if __name__ == "__main__":
    main()

