import re
import streamlit as st
from streamlit_extras.app_logo import add_logo
import fitz  # PyMuPDF
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import time

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6')
    summarizer = AutoModelForSeq2SeqLM.from_pretrained('sshleifer/distilbart-cnn-12-6')
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
        num_beams=6,
        length_penalty=2.0,
        max_length=maximum_tokens,
        min_length=minimum_tokens,
        no_repeat_ngram_size=3,
        early_stopping=True,
        do_sample=False,
        num_return_sequences=2
    )
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary

# Initialize Streamlit app
add_logo("https://i.imgur.com/amZoFFM.jpg")
st.title("Policy Text Summariser")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Summarize"):
    if pdf_file is not None:
        input_document = extract_text_from_pdf(pdf_file)
        tokenizer, summarizer = load_model()
        sentences = split_sentences(input_document)
        chunks = create_chunks(sentences, chunk_size=1024)

        progress_text = "Summarising in progress..."
        progress_bar = st.progress(0, text=progress_text)

        combined_summary = ''  # Initialize combined_summary
        for i, chunk in enumerate(chunks):
            combined_text = ' '.join(chunk)
            summary = generate_summary(combined_text, maximum_tokens=300, minimum_tokens=150)
            combined_summary += summary + ' '

            progress = (i + 1) / len(chunks) 
            progress_bar.progress(progress, text=progress_text)

        final_summary = generate_summary(combined_summary, maximum_tokens=800, minimum_tokens=600)
        final_summary_sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', final_summary.replace("\n", ' '))
        bullet_points = ["• " + sentence for sentence in final_summary_sentences]
        output = "\n".join(bullet_points)

        progress_bar.empty()  # Remove progress bar
        st.subheader("Final Summary:")
        st.write(output)

    else:
        st.warning("Please upload a PDF file.")
