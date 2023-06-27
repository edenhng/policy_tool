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
    st.title("Tabulating sentences")
    #Retrieve the PDF file from the session state
    if 'working_pdf' in st.session_state:
        working_pdf = st.session_state.working_pdf
        st.info("The PDF is here")
    else:
        st.warning("The PDF is not successfully uploaded. Please try again!")
    

if __name__ == "__main__":
    main()

