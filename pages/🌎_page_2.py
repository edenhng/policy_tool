import streamlit as st
from streamlit import components
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


def run_lda(tokens):
    # Preprocess the document
    # Create a dictionary from the tokens
    dictionary = corpora.Dictionary([tokens])
 
    # Create a corpus using the dictionary
    corpus = [dictionary.doc2bow(tokens)]
    
    # Create the LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, random_state=100, 
                                                update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

    # Compute the coherence score
    coherence_model = gensim.models.CoherenceModel(model=lda_model, texts=[tokens], dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()

    # Visualize the topics
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    html_string = pyLDAvis.prepared_data_to_html(vis_data)
    components.v1.html(html_string, width=1300, height=800, scrolling=True)

    # Print the coherence score
    st.write("Coherence Score: ", coherence_score)


# Streamlit app
def main():
    st.title("LDA Topic Modeling")
    #Retrieve the stored PDF file from the session state
    if 'processed_tokens' in st.session_state:
        processed_tokens = st.session_state.processed_tokens
        st.write("Found a working File from Main Page")
    else:
        st.info("No working file found from Page 1.")
    run_lda(processed_tokens)
    
        
if __name__ == "__main__":
    main()
