import streamlit as st
import nltk
from nltk import FreqDist, Text as nltk_text, ngrams
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import chardet  # For encoding detection
import os

# Download required NLTK data (punkt) if not already present
def ensure_punkt_download():
    nltk_data_path = nltk.data.path
    st.write(f"NLTK data path: {nltk_data_path}")
    try:
        nltk.data.find('tokenizers/punkt')
        st.write("Punkt resource already available.")
    except LookupError:
        st.warning("Downloading 'punkt' resource. Please wait...")
        nltk.download('punkt', quiet=False, download_dir=nltk_data_path[0])  # Explicitly set download directory
        try:
            nltk.data.find('tokenizers/punkt')
            st.success("Punkt resource downloaded successfully.")
        except LookupError:
            st.error(f"Failed to download 'punkt' resource. Checked paths: {nltk_data_path}. Please ensure internet access or run 'nltk.download('punkt')' manually.")
            st.stop()

ensure_punkt_download()

# Initialize tokenizer
tokenizer = RegexpTokenizer(r'\w+')

# Streamlit app
st.title("Uhlelo Lokuhlaziya Ikhophasi YesiZulu")
st.write("Co-written by: Mr Mthuli Percival Buthelezi 🎓 (PhD Linguistics [IsiZulu] Candidate) and Mr Sakhile Marcus Zungu 🎓 (MSc Applied Mathematics [Astronomy] Candidate) for Mthuli's PhD research.")
st.write("Upload a .txt file to analyze an IsiZulu corpus.")

# File upload
uploaded_file = st.file_uploader("Khetha ikhophasi", type="txt")
reference_file = None  # For keyness analysis

# Session state to store tokenized text
if 'tokens' not in st.session_state:
    st.session_state.tokens = None
    st.session_state.text = None

if uploaded_file:
    # Detect encoding
    raw_data = uploaded_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    
    try:
        # Decode with detected encoding or fallback to latin-1
        if encoding is None:
            st.session_state.text = raw_data.decode('latin-1')
        else:
            st.session_state.text = raw_data.decode(encoding)
        st.session_state.tokens = tokenizer.tokenize(st.session_state.text)
        st.write(f"File decoded successfully with encoding: {encoding}")
    except UnicodeDecodeError as e:
        st.error(f"Error decoding file: {e}. Please ensure it is a valid text file (e.g., UTF-8 or ANSI).")
        st.stop()

    analysis_type = st.selectbox("Khetha uhlobo lokuhlaziya:", [
        "Uhlumagama (Word List)", 
        "Imvumelwanomagama (Concordance)", 
        "Ubungqikithimagama (Keyness)", 
        "Onhlamvunye (N-grams)", 
        "Amafumagama (Wordcloud)", 
        "Isibalo sezinhlamvu zamagama (Letter Frequency)", 
        "Isibalo samagama (Word Count)"
    ])

    tokens = st.session_state.tokens
    text = st.session_state.text

    if analysis_type == "Uhlumagama (Word List)":
        freq_dist = FreqDist(tokens)
        freq_df = pd.DataFrame(sorted(freq_dist.items(), key=lambda x: x[1], reverse=True), columns=["Word", "Frequency"])
        st.write(freq_df)
        st.download_button("Download as CSV", freq_df.to_csv(index=False), "word_list.csv")

    elif analysis_type == "Imvumelwanomagama (Concordance)":
        search_word = st.text_input("Loba igama:")
        if search_word:
            nltk_text_obj = nltk_text(tokens)
            concordance_list = nltk_text_obj.concordance_list(search_word)
            if concordance_list:
                for conc in concordance_list:
                    st.write(conc.line)
            else:
                st.write(f"No matches found for the word: {search_word}")

    elif analysis_type == "Ubungqikithimagama (Keyness)":
        reference_file = st.file_uploader("Khetha ikhophasi eyisindlalelo", type="txt")
        if reference_file:
            raw_ref_data = reference_file.read()
            ref_result = chardet.detect(raw_ref_data)
            ref_encoding = ref_result['encoding']
            try:
                if ref_encoding is None:
                    ref_text = raw_ref_data.decode('latin-1')
                else:
                    ref_text = raw_ref_data.decode(ref_encoding)
                ref_tokens = [tokenizer.tokenize(t) for t in sent_tokenize(ref_text)]
                corpus_sents = [tokenizer.tokenize(t) for t in sent_tokenize(text)]
                keyness = log_likelihood(corpus_sents, ref_tokens)
                keyness_df = pd.DataFrame(keyness, columns=["Word", "Log Likelihood"])
                st.write(keyness_df)
                st.download_button("Download as CSV", keyness_df.to_csv(index=False), "keyness.csv")
            except UnicodeDecodeError as e:
                st.error(f"Error decoding reference file: {e}. Please ensure it is a valid text file.")

    elif analysis_type == "Onhlamvunye (N-grams)":
        n = st.slider("Select N-gram size", 1, 5, 2)
        n_grams = list(ngrams(tokens, n))
        n_gram_freq = FreqDist([" ".join(gram) for gram in n_grams])
        n_gram_df = pd.DataFrame(sorted(n_gram_freq.items(), key=lambda x: x[1], reverse=True), columns=["N-gram", "Frequency"])
        st.write(n_gram_df)
        st.download_button("Download as CSV", n_gram_df.to_csv(index=False), "ngrams.csv")

    elif analysis_type == "Amafumagama (Wordcloud)":
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(tokens))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
        plt.savefig("wordcloud.png")
        with open("wordcloud.png", "rb") as file:
            st.download_button("Download Wordcloud", file, "wordcloud.png")

    elif analysis_type == "Isibalo sezinhlamvu zamagama (Letter Frequency)":
        letters = [char.lower() for char in text if char.isalpha()]
        letter_freq = Counter(letters)
        letter_df = pd.DataFrame(sorted(letter_freq.items(), key=lambda x: x[1], reverse=True), columns=["Letter", "Frequency"])
        st.write(letter_df)
        st.download_button("Download as CSV", letter_df.to_csv(index=False), "letter_freq.csv")

    elif analysis_type == "Isibalo samagama (Word Count)":
        st.write(f"Total number of words: {len(tokens)}")

# Run the app
if __name__ == "__main__":
    pass