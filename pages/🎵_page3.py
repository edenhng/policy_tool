import spacy
import streamlit as st
from spacy import displacy

def highlight_money_entities(doc):
    html = displacy.render(doc, style="ent", options={"ents": ["MONEY"]}, page=True)
    st.components.v1.html(html, height=400, scrolling=True)

def main():
    st.title("Named Entity Recognition with spaCy")
    document = st.text_area("Enter your document text here", height=200)

    if st.button("Extract Sentences"):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(document)
        money_sentences = []

        for sent in doc.sents:
            sent_entities = [ent for ent in sent.ents if ent.label_ == "MONEY"]
            if sent_entities:
                money_sentences.append(sent)

        if money_sentences:
            st.subheader("Sentences with 'MONEY' entities:")
            for sentence in money_sentences:
                st.write(sentence.text)
                highlight_money_entities(sentence)
                st.write("---")
        else:
            st.write("No sentences with 'MONEY' entities found.")

if __name__ == "__main__":
    main()
