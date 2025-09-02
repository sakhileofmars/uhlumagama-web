import streamlit as st
import pandas as pd
from collections import Counter
import chardet
import os
import sys

# Try importing NLTK with error handling
try:
    import nltk
    from nltk import FreqDist, Text as nltk_text, ngrams
    from nltk.tokenize import RegexpTokenizer, sent_tokenize
    NLTK_AVAILABLE = True
except ImportError as e:
    st.error(f"NLTK import failed: {e}")
    st.error("Please ensure NLTK is installed properly.")
    NLTK_AVAILABLE = False

# Try importing other libraries
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError as e:
    st.warning(f"WordCloud not available: {e}")
    WORDCLOUD_AVAILABLE = False

# Try importing keyness with fallback
try:
    from keyness import log_likelihood
    KEYNESS_AVAILABLE = True
except ImportError as e:
    st.warning(f"Keyness library not available: {e}. Keyness analysis will be disabled.")
    KEYNESS_AVAILABLE = False

# Download required NLTK data with better error handling
@st.cache_data
def ensure_punkt_download():
    if not NLTK_AVAILABLE:
        return False
    
    try:
        # Try to find punkt tokenizer
        nltk.data.find('tokenizers/punkt')
        return True
    except LookupError:
        try:
            # Download punkt tokenizer
            nltk.download('punkt', quiet=True)
            # Verify download
            nltk.data.find('tokenizers/punkt')
            return True
        except Exception as e:
            st.error(f"Failed to download NLTK punkt tokenizer: {e}")
            return False

# Initialize the app only if NLTK is available
if NLTK_AVAILABLE:
    punkt_available = ensure_punkt_download()
    if not punkt_available:
        st.error("NLTK punkt tokenizer is required but couldn't be downloaded.")
        st.stop()
    
    # Initialize tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
else:
    st.error("NLTK is required for this application to work properly.")
    st.stop()

# Streamlit app
st.title("🔬 Uhlelo Lokuhlaziya Ikhophasi YesiZulu")
st.markdown("### IsiZulu Corpus Analysis Toolkit")

# Author information in sidebar
with st.sidebar:
    st.markdown("### 👥 Authors")
    st.info("""
    **Co-developed by:**
    
    🎓 **Mr Mthuli Percival Buthelezi**  
    PhD Linguistics [IsiZulu] Candidate
    
    🎓 **Mr Sakhile Marcus Zungu**  
    MSc Applied Mathematics [Astronomy] Candidate
    
    *For Mthuli's PhD research*
    """)

st.markdown("---")
st.write("📂 Upload a .txt file to analyze an IsiZulu corpus.")

# File upload
uploaded_file = st.file_uploader("📁 Khetha ikhophasi (Choose Corpus)", type="txt")

# Session state to store tokenized text
if 'tokens' not in st.session_state:
    st.session_state.tokens = None
    st.session_state.text = None
    st.session_state.filename = None

if uploaded_file:
    # Show file info
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Detect encoding
    with st.spinner("🔍 Detecting file encoding..."):
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] or 'utf-8'
    
    try:
        # Decode with detected encoding
        st.session_state.text = raw_data.decode(encoding)
        st.session_state.tokens = tokenizer.tokenize(st.session_state.text)
        st.session_state.filename = uploaded_file.name
        
        # Show file stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Encoding", encoding)
        with col2:
            st.metric("📊 Total Words", len(st.session_state.tokens))
        with col3:
            st.metric("📄 Characters", len(st.session_state.text))
            
    except UnicodeDecodeError as e:
        st.error(f"❌ Error decoding file: {e}")
        st.error("Please ensure it is a valid text file (UTF-8, Latin-1, or ANSI).")
        st.stop()

    # Analysis type selection
    st.markdown("---")
    analysis_options = [
        "📊 Uhlumagama (Word List)", 
        "🔍 Imvumelwanomagama (Concordance)", 
        "🔗 Onhlamvunye (N-grams)", 
        "📈 Isibalo samagama (Word Count & Statistics)"
    ]
    
    # Add keyness option only if available
    if KEYNESS_AVAILABLE:
        analysis_options.insert(2, "🎯 Ubungqikithimagama (Keyness)")
    
    # Add wordcloud option only if available
    if WORDCLOUD_AVAILABLE:
        analysis_options.append("☁️ Amafumagama (Wordcloud)")
    
    # Always add letter frequency (doesn't need special libraries)
    analysis_options.append("🔤 Isibalo sezinhlamvu zamagama (Letter Frequency)")

    analysis_type = st.selectbox("🔬 Khetha uhlobo lokuhlaziya (Choose analysis type):", analysis_options)

    tokens = st.session_state.tokens
    text = st.session_state.text

    # Analysis sections
    st.markdown("---")
    
    if analysis_type == "📊 Uhlumagama (Word List)":
        st.header("📊 Word Frequency Analysis")
        
        with st.spinner("🔄 Calculating word frequencies..."):
            freq_dist = FreqDist(tokens)
            freq_df = pd.DataFrame(
                sorted(freq_dist.items(), key=lambda x: x[1], reverse=True), 
                columns=["Word", "Frequency"]
            )
            
            # Add percentage column
            total_words = len(tokens)
            freq_df["Percentage"] = (freq_df["Frequency"] / total_words * 100).round(2)
        
        # Display controls
        col1, col2 = st.columns(2)
        with col1:
            top_n = st.slider("Show top N words", 10, min(500, len(freq_df)), 50)
        with col2:
            min_freq = st.slider("Minimum frequency", 1, 20, 1)
        
        # Filter data
        filtered_df = freq_df[freq_df["Frequency"] >= min_freq].head(top_n)
        
        # Display results
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "📥 Download as CSV", 
            csv, 
            f"word_frequency_{st.session_state.filename}.csv",
            mime="text/csv"
        )

    elif analysis_type == "🔍 Imvumelwanomagama (Concordance)":
        st.header("🔍 Concordance Analysis")
        
        search_word = st.text_input("🔎 Loba igama (Enter word to search):", placeholder="Type a word...")
        
        if search_word:
            with st.spinner(f"🔄 Searching for '{search_word}'..."):
                nltk_text_obj = nltk_text(tokens)
                concordance_list = nltk_text_obj.concordance_list(search_word.lower())
                
                if concordance_list:
                    st.success(f"✅ Found {len(concordance_list)} occurrences of '{search_word}'")
                    
                    # Create DataFrame for better display
                    concordance_data = []
                    for i, conc in enumerate(concordance_list):
                        concordance_data.append({
                            "Line #": i + 1,
                            "Context": conc.line
                        })
                    
                    concordance_df = pd.DataFrame(concordance_data)
                    st.dataframe(concordance_df, use_container_width=True)
                    
                    # Download button
                    csv = concordance_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Concordance", 
                        csv, 
                        f"concordance_{search_word}_{st.session_state.filename}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning(f"⚠️ No matches found for the word: '{search_word}'")

    elif analysis_type == "🎯 Ubungqikithimagama (Keyness)" and KEYNESS_AVAILABLE:
        st.header("🎯 Keyness Analysis")
        st.info("📋 Upload a reference corpus to compare against your main corpus.")
        
        reference_file = st.file_uploader("📁 Khetha ikhophasi eyisindlalelo (Choose reference corpus)", type="txt")
        
        if reference_file:
            with st.spinner("🔄 Processing reference corpus..."):
                raw_ref_data = reference_file.read()
                ref_result = chardet.detect(raw_ref_data)
                ref_encoding = ref_result['encoding'] or 'utf-8'
                
                try:
                    ref_text = raw_ref_data.decode(ref_encoding)
                    st.success(f"✅ Reference corpus loaded: {reference_file.name}")
                    
                    # Prepare data for keyness analysis
                    ref_tokens = [tokenizer.tokenize(t) for t in sent_tokenize(ref_text)]
                    corpus_sents = [tokenizer.tokenize(t) for t in sent_tokenize(text)]
                    
                    # Calculate keyness
                    with st.spinner("🔄 Calculating keyness values..."):
                        keyness_results = log_likelihood(corpus_sents, ref_tokens)
                        keyness_df = pd.DataFrame(keyness_results, columns=["Word", "Log Likelihood"])
                        keyness_df["Significance"] = keyness_df["Log Likelihood"].apply(
                            lambda x: "Very High" if x > 15.13 else 
                                     "High" if x > 10.83 else 
                                     "Medium" if x > 6.63 else "Low"
                        )
                    
                    st.dataframe(keyness_df.head(100), use_container_width=True)
                    
                    # Download button
                    csv = keyness_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Keyness Results", 
                        csv, 
                        f"keyness_{st.session_state.filename}.csv",
                        mime="text/csv"
                    )
                    
                except UnicodeDecodeError as e:
                    st.error(f"❌ Error decoding reference file: {e}")

    elif analysis_type == "🔗 Onhlamvunye (N-grams)":
        st.header("🔗 N-grams Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            n = st.slider("📏 Select N-gram size", 1, 5, 2)
        with col2:
            top_n = st.slider("📊 Show top N n-grams", 10, 200, 50)
        
        with st.spinner(f"🔄 Calculating {n}-grams..."):
            if n == 1:
                # For unigrams, use the existing tokens
                n_gram_freq = FreqDist(tokens)
            else:
                n_grams = list(ngrams(tokens, n))
                n_gram_freq = FreqDist([" ".join(gram) for gram in n_grams])
            
            n_gram_df = pd.DataFrame(
                sorted(n_gram_freq.items(), key=lambda x: x[1], reverse=True)[:top_n], 
                columns=[f"{n}-gram", "Frequency"]
            )
        
        st.dataframe(n_gram_df, use_container_width=True)
        
        # Download button
        csv = n_gram_df.to_csv(index=False)
        st.download_button(
            "📥 Download N-grams", 
            csv, 
            f"{n}grams_{st.session_state.filename}.csv",
            mime="text/csv"
        )

    elif analysis_type == "☁️ Amafumagama (Wordcloud)" and WORDCLOUD_AVAILABLE:
        st.header("☁️ Word Cloud Visualization")
        
        col1, col2 = st.columns(2)
        with col1:
            max_words = st.slider("Max words in cloud", 50, 200, 100)
        with col2:
            min_freq = st.slider("Minimum word frequency", 1, 10, 2)
        
        with st.spinner("🎨 Generating word cloud..."):
            # Filter tokens by frequency
            freq_dist = FreqDist(tokens)
            filtered_words = {word: freq for word, freq in freq_dist.items() if freq >= min_freq}
            
            if filtered_words:
                wordcloud = WordCloud(
                    width=800, 
                    height=400, 
                    background_color="white",
                    max_words=max_words,
                    colormap='autumn'
                ).generate_from_frequencies(filtered_words)
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
                
                # Save and download option
                plt.savefig("wordcloud.png", bbox_inches='tight', dpi=300)
                with open("wordcloud.png", "rb") as file:
                    st.download_button(
                        "📥 Download Wordcloud", 
                        file, 
                        f"wordcloud_{st.session_state.filename}.png",
                        mime="image/png"
                    )
            else:
                st.warning("⚠️ No words meet the minimum frequency requirement.")

    elif analysis_type == "🔤 Isibalo sezinhlamvu zamagama (Letter Frequency)":
        st.header("🔤 Letter Frequency Analysis")
        
        with st.spinner("🔄 Analyzing letter frequencies..."):
            # Get only alphabetic characters
            letters = [char.lower() for char in text if char.isalpha()]
            letter_freq = Counter(letters)
            
            total_letters = sum(letter_freq.values())
            letter_data = []
            
            for letter, freq in sorted(letter_freq.items(), key=lambda x: x[1], reverse=True):
                letter_data.append({
                    "Letter": letter.upper(),
                    "Frequency": freq,
                    "Percentage": round((freq / total_letters * 100), 2)
                })
            
            letter_df = pd.DataFrame(letter_data)
        
        # Display results
        st.dataframe(letter_df, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔤 Total Letters", total_letters)
        with col2:
            st.metric("🎯 Unique Letters", len(letter_freq))
        with col3:
            most_common = letter_df.iloc[0]
            st.metric("📊 Most Common", f"{most_common['Letter']} ({most_common['Percentage']}%)")
        
        # Download button
        csv = letter_df.to_csv(index=False)
        st.download_button(
            "📥 Download Letter Frequency", 
            csv, 
            f"letter_frequency_{st.session_state.filename}.csv",
            mime="text/csv"
        )

    elif analysis_type == "📈 Isibalo samagama (Word Count & Statistics)":
        st.header("📈 Corpus Statistics")
        
        # Calculate comprehensive statistics
        total_words = len(tokens)
        unique_words = len(set(tokens))
        total_chars = len(text)
        sentences = sent_tokenize(text)
        total_sentences = len(sentences)
        
        # Display main statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📝 Total Words", f"{total_words:,}")
            st.metric("🔤 Total Characters", f"{total_chars:,}")
            st.metric("📄 Total Sentences", f"{total_sentences:,}")
        
        with col2:
            st.metric("🎯 Unique Words", f"{unique_words:,}")
            st.metric("📊 Lexical Diversity", f"{(unique_words/total_words):.3f}")
            if total_sentences > 0:
                st.metric("📏 Avg Words/Sentence", f"{(total_words/total_sentences):.1f}")
        
        # Additional statistics
        st.subheader("📋 Detailed Statistics")
        
        word_lengths = [len(word) for word in tokens]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        stats_data = {
            "Statistic": [
                "Average Word Length",
                "Shortest Word Length", 
                "Longest Word Length",
                "Characters (excluding spaces)",
                "Vocabulary Richness (%)"
            ],
            "Value": [
                f"{avg_word_length:.2f} characters",
                f"{min(word_lengths)} characters" if word_lengths else "N/A",
                f"{max(word_lengths)} characters" if word_lengths else "N/A", 
                f"{len([c for c in text if not c.isspace()]):,}",
                f"{(unique_words/total_words)*100:.2f}%"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>🔬 Uhlelo Lokuhlaziya Ikhophasi YesiZulu</strong></p>
    <p><em>IsiZulu Corpus Analysis Toolkit for Academic Research</em></p>
</div>
""", unsafe_allow_html=True)