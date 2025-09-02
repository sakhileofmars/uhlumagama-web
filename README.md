# 🔬 Uhlelo Lokuhlaziya Ikhophasi YesiZulu
## IsiZulu Corpus Analysis Toolkit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NLTK](https://img.shields.io/badge/NLTK-3.8+-green.svg)](https://www.nltk.org/)

A comprehensive web-based corpus analysis toolkit specifically designed for IsiZulu linguistic research. This application provides advanced computational linguistics tools for analyzing IsiZulu text corpora, featuring both traditional corpus analysis methods and modern visualization techniques.

## 🎓 Academic Context

This project was developed as part of PhD Linguistics research focusing on IsiZulu language analysis. It serves as a practical tool for computational linguistics research, corpus studies, and linguistic data analysis within the context of African language processing.

**Authors:**
- **Mr. Mthuli Percival Buthelezi** 🎓 - PhD Linguistics [IsiZulu] Candidate
- **Mr. Sakhile Marcus Zungu** 🎓 - MSc Applied Mathematics [Astronomy] Candidate
- **Research Collaboration:** Uluntu Algorithms

## ✨ Features

### Core Analysis Tools

| Feature | IsiZulu Name | Description |
|---------|--------------|-------------|
| 📊 **Word Frequency** | *Uhlumagama* | Statistical analysis of word occurrence with frequency distribution |
| 🔍 **Concordance** | *Imvumelwanomagama* | Contextual word search showing surrounding text |
| 🎯 **Keyness Analysis** | *Ubungqikithimagama* | Comparative analysis against reference corpus using log-likelihood |
| 🔗 **N-grams Analysis** | *Onhlamvunye* | Extract uni-grams, bi-grams, tri-grams, and higher-order sequences |
| ☁️ **Word Cloud** | *Amafumagama* | Visual representation of word frequency distribution |
| 🔤 **Letter Frequency** | *Isibalo sezinhlamvu zamagama* | Character-level statistical analysis |
| 📈 **Word Count** | *Isibalo samagama* | Basic corpus statistics and metrics |

### Technical Capabilities

- **Multi-encoding Support**: Automatic encoding detection (UTF-8, Latin-1, ANSI)
- **Interactive Web Interface**: Built with Streamlit for easy deployment
- **Data Export**: Download results as CSV files
- **Visualization**: Matplotlib-based word clouds and charts
- **Robust Text Processing**: NLTK-powered tokenization and analysis
- **Research-Grade Output**: Suitable for academic publication and presentation

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8 or higher
pip package manager
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/isizulu-corpus-analyzer.git
   cd isizulu-corpus-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run uhlumagama_web.py
   ```

4. **Access the app:**
   Open your browser and navigate to `http://localhost:8501`

### Docker Deployment (Optional)

```bash
# Build the Docker image
docker build -t isizulu-analyzer .

# Run the container
docker run -p 8501:8501 isizulu-analyzer
```

## 📖 Usage Guide

### Basic Workflow

1. **Upload Corpus**: Click "Khetha ikhophasi" to upload your IsiZulu text file (.txt)
2. **Select Analysis**: Choose from the dropdown menu "Khetha uhlobo lokuhlaziya"
3. **Configure Parameters**: Adjust settings specific to your chosen analysis
4. **View Results**: Analyze the output in the main interface
5. **Export Data**: Download results as CSV files for further analysis

### Analysis Types

#### 📊 Word Frequency Analysis (Uhlumagama)
- Generates frequency distribution of all words in corpus
- Sortable by frequency or alphabetical order
- Export functionality for spreadsheet analysis

#### 🔍 Concordance Analysis (Imvumelwanomagama)
- Search for specific words in context
- Shows surrounding words for linguistic analysis
- Useful for studying word usage patterns

#### 🎯 Keyness Analysis (Ubungqikithimagama)
- Requires a reference corpus for comparison
- Uses log-likelihood ratio for statistical significance
- Identifies words that are unusually frequent in your corpus

#### 🔗 N-grams Analysis (Onhlamvunye)
- Configurable n-gram size (1-5)
- Identifies common word sequences
- Essential for phraseological studies

#### ☁️ Word Cloud Visualization (Amafumagama)
- Visual representation of word frequencies
- Customizable appearance
- Download as PNG image

#### 🔤 Letter Frequency Analysis (Isibalo sezinhlamvu zamagama)
- Character-level frequency analysis
- Useful for phonological studies
- Statistical breakdown of character usage

### File Format Requirements

- **Input Format**: Plain text files (.txt)
- **Encoding**: UTF-8, Latin-1, or ANSI (auto-detected)
- **Size Limit**: Dependent on system memory
- **Content**: Raw text, minimal preprocessing required

## 🛠 Technical Architecture

### Dependencies

```python
streamlit>=1.32.0    # Web application framework
nltk>=3.8.1          # Natural language processing
wordcloud>=1.9.2     # Word cloud generation
matplotlib>=3.8.2    # Plotting and visualization
pandas>=2.2.0        # Data manipulation
chardet>=5.2.0       # Character encoding detection
keyness>=1.0.1       # Keyness analysis (log-likelihood)
```

### Project Structure

```
isizulu-corpus-analyzer/
├── uhlumagama_web.py          # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── tests/
│   └── test_corpus_analysis.py
└── examples/
    ├── sample_corpus.txt
    └── sample_reference.txt
```

### Key Functions

- `ensure_punkt_download()`: Manages NLTK data dependencies
- `RegexpTokenizer()`: Handles text tokenization
- `FreqDist()`: Calculates frequency distributions
- `concordance_list()`: Generates concordance lines
- `log_likelihood()`: Performs keyness analysis

## 📚 Academic Applications

### Research Use Cases

- **Corpus Linguistics**: Large-scale text analysis and pattern identification
- **Lexicography**: Frequency-based dictionary compilation
- **Sociolinguistics**: Comparative analysis across text varieties
- **Computational Linguistics**: Algorithm development and testing
- **Language Documentation**: Systematic analysis of language resources

### Citation

If you use this tool in academic research, please cite:

```bibtex
@software{buthelezi_zungu_2024_isizulu_analyzer,
  author       = {Buthelezi, Mthuli Percival and Zungu, Sakhile Marcus},
  title        = {Uhlelo Lokuhlaziya Ikhophasi YesiZulu: IsiZulu Corpus Analysis Toolkit},
  year         = {2024},
  publisher    = {GitHub},
  url          = {https://github.com/yourusername/isizulu-corpus-analyzer}
}
```

## 🤝 Contributing

We welcome contributions from the computational linguistics and African languages research community!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Include docstrings for all functions
- Add unit tests for new features
- Update documentation as needed
- Consider multilingual accessibility (English/IsiZulu)

## 🐛 Known Issues & Limitations

- **Memory Usage**: Large corpora may require significant RAM
- **Encoding**: Some legacy text files may need manual encoding conversion
- **NLTK Data**: First run requires internet connection for NLTK downloads
- **Keyness Analysis**: Requires reference corpus for meaningful results

## 📞 Support & Contact

- **Issues**: Please use GitHub Issues for bug reports and feature requests
- **Academic Inquiries**: Contact the authors through institutional channels
- **Collaboration**: Open to research partnerships and academic collaborations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NLTK Community**: For comprehensive natural language processing tools
- **Streamlit Team**: For the excellent web application framework
- **IsiZulu Language Community**: For inspiration and linguistic expertise
- **Academic Institutions**: Supporting computational linguistics research
- **Open Source Contributors**: Making tools accessible for African language research

## 🔮 Future Development

- **Enhanced Visualizations**: Interactive plots with Plotly
- **Statistical Analysis**: Advanced corpus comparison metrics
- **Multi-language Support**: Extension to other Bantu languages
- **API Development**: RESTful API for programmatic access
- **Cloud Deployment**: Scalable hosting solutions
- **Mobile Interface**: Responsive design for mobile devices

---

**Ngiyabonga! Thank you for using the IsiZulu Corpus Analysis Toolkit!** 🙏

*This tool represents a contribution to the digital preservation and analysis of African languages, supporting both academic research and language technology development.*
