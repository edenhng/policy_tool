'''
import spacy
import streamlit as st
from spacy import displacy
import fitz

def highlight_entities(doc, entity_label):
    html = displacy.render(doc, style="ent", options={"ents": [entity_label]}, page=True)
    st.components.v1.html(html, height=400, scrolling=True)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
        
def main():
    st.title("Named Entity Recognition with spaCy")
    file = st.file_uploader("Upload a PDF file", type="pdf")
    entity_option = st.selectbox("Select entity to highlight", ("MONEY", "PERSON"))

    if file is not None:
        document = extract_text_from_pdf(file)
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(document)
        entity_label = entity_option.upper()

        if st.button("Extract Sentences"):
            entity_sentences = [sent for sent in doc.sents if any(ent.label_ == entity_label for ent in sent.ents)]

            if entity_sentences:
                st.subheader(f"Sentences with '{entity_label}' entities:")
                for sentence in entity_sentences:
                    st.write(sentence.text)
                    highlight_entities(sentence, entity_label)
                    st.write("---")
            else:
                st.write(f"No sentences with '{entity_label}' entities found.")

if __name__ == "__main__":
    main()
'''
