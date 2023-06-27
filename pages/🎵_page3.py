import streamlit as st
import fitz
import pandas as pd
import spacy
from spacy import displacy


def highlight_entities(doc, entity_label):
    html = displacy.render(doc, style="ent", options={"ents": [entity_label]}, page=True)
    st.components.v1.html(html, height=400, scrolling=True)

def extract_sentences_from_pdf(pdf_data):
    sentences = []
    nlp = spacy.load("en_core_web_sm")
    for page_num, page in enumerate(pdf_data, 1):
        text = page.get_text()
        doc = nlp(text)
        for sent in doc.sents:
            sentences.append((page_num, sent.text))
    return sentences
        
def main():
    st.title("Tabulating sentences")
    #Retrieve the PDF file from the session state
    if 'working_pdf' in st.session_state:
        working_pdf = st.session_state.working_pdf
        st.info("The PDF is here")
        sentences = extract_sentences_from_pdf(working_pdf)

        if len(sentences) > 0:
            st.write("Extracted Sentences:")
    
            csv_data = pd.DataFrame(sentences, columns= ["Page Number", "Sentence"])
            csv_string = csv_data.to_csv(index=False)
            st.write("CSV File:")
            st.write(csv_data)
            save_excel = st.download_button("Save to Excel", csv_data.to_excel, "extracted_sentences.xlsx", 
                                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                                             key="download-excel")
            if save_excel:
                st.write("Sentences saved to extracted_sentences.csv")
              
    else:
        st.warning("The PDF is not successfully uploaded. Please try again!")
    

if __name__ == "__main__":
    main()

