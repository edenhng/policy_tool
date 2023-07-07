import re
import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache(allow_output_mutation=True)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')
    summarizer = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large-cnn')
    return tokenizer, summarizer
    
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def split_sentences(document):
    sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', document.replace("\n", ' '))
    return sentences

def create_chunks(sentences, chunk_size):
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        tokenized_sentence = tokenizer(sentence, truncation=False, padding=False)[0]
        sentence_length = len(tokenized_sentence)

        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append(current_chunk)
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def generate_summary(sequence, maximum_tokens, minimum_tokens):
    input_ids = tokenizer.encode(sequence, truncation=True, max_length=1024, return_tensors="pt")
    output = summarizer.generate(
        input_ids,
        num_beams=4,
        length_penalty=2.0,
        max_length=maximum_tokens,
        min_length=minimum_tokens,
        no_repeat_ngram_size=3,
        early_stopping=True,
        do_sample=False,
        num_return_sequences=1
    )
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary

# Initialize Streamlit app
st.title("Text Summarization with BART")
st.subheader("Upload your PDF document")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Summarize"):
    if pdf_file is not None:
        input_document = extract_text_from_pdf(pdf_file)

        sentences = split_sentences(input_document)
        chunks = create_chunks(sentences, chunk_size=1024)

        combined_summary = ''
        for chunk in chunks:
            combined_text = ' '.join(chunk)
            summary = generate_summary(combined_text, maximum_tokens=150, minimum_tokens=40)
            combined_summary += summary + ' '

        final_summary = generate_summary(combined_summary, maximum_tokens=500, minimum_tokens=300)
        final_summary_sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', final_summary.replace("\n", ' '))
        bullet_points = ["• " + sentence for sentence in final_summary_sentences]
        output = "\n".join(bullet_points)

        st.subheader("Final Summary:")
        st.write(output)
    else:
        st.warning("Please upload a PDF file.")
