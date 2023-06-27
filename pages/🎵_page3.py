import streamlit as st
import fitz
import pandas as pd
import spacy
from spacy import displacy
from io import BytesIO

#Get data from the stored pdf file in session state
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
    # Retrieve the PDF file from the session state
    if 'working_pdf' in st.session_state:
        working_pdf = st.session_state.working_pdf
        st.info("The PDF is here")
        sentences = extract_sentences_from_pdf(working_pdf)

        if len(sentences) > 0:
            st.write("Extracted Sentences:")

            csv_data = pd.DataFrame(sentences, columns=["Page Number", "Sentence"])
            st.write("CSV File:")
            st.write(csv_data)

            # Save DataFrame to Excel file
            excel_data = BytesIO()
            with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
                csv_data.to_excel(writer, sheet_name='Sheet1', index=False)
            excel_data.seek(0)

            save_excel = st.download_button("Save to Excel", excel_data, 
                                             file_name="extracted_sentences.xlsx", 
                                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                                             key="download-excel")

            if save_excel:
                st.write("Sentences saved to extracted_sentences.xlsx")
        else:
            st.warning("The code is wrong to produce the sentences!")
    else:
        st.warning("The PDF is not successfully uploaded. Please try again!")


if __name__ == "__main__":
    main()
