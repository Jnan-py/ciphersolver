# CipherSolver

**CipherSolver** is a cybersecurity-oriented Streamlit application that combines classical cryptography techniques with modern NLP tools. It provides functionalities to encrypt and decrypt text using various ciphers, perform frequency analysis of text, and solve anagrams with enhanced NLP features.

## Features

- **Cryptogram Solver:**  
  Encrypt and decrypt text using:

  - Caesar Cipher
  - Vigenere Cipher
  - Rail Fence Cipher
  - Simple Columnar Transposition

- **Frequency Analysis:**  
  Analyze text for letter, digraph, or trigraph frequencies with interactive visualizations (bar charts, pie charts, and word clouds).

- **Enhanced Anagram Solver:**  
  Generate anagrams from a given word or phrase and check if two words/phrases are anagrams. It also suggests synonyms and antonyms for input words using NLP and NLTK's WordNet.

- **NLP Integration:**  
  Uses SpaCy for text preprocessing and NLTK for lexical analysis to enhance anagram solving and other text operations.

- **User-Friendly UI:**  
  Built with Streamlit, featuring a modern sidebar navigation and card-based layouts for an engaging user experience.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Jnan-py/ciphersolver.git
   cd ciphersolver
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Required NLP Resources:**
   - **SpaCy:**  
     Download the English model by running:
     ```bash
     python -m spacy download en_core_web_sm
     ```
   - **NLTK:**  
     In your Python interpreter or script, run:
     ```python
     import nltk
     nltk.download('wordnet')
     nltk.download('omw-1.4')
     ```

## Usage

1. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

2. **Navigate Through Features:**
   - Use the sidebar to switch between:
     - **Home:** Overview and introduction to CipherSolver.
     - **Frequency Analysis:** Upload or input text to analyze n-gram frequencies.
     - **Cryptogram Solver:** Encrypt or decrypt text using your chosen cipher.
     - **Anagram Solver:** Generate or verify anagrams and get synonym/antonym suggestions.

## Project Structure

```
ciphersolver/
│
├── app.py                  # Main Streamlit application
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
```

## Technologies Used

- **Streamlit:** For building the interactive web interface.
- **SpaCy:** For natural language processing.
- **NLTK:** For lexical database access (WordNet).
- **Matplotlib & Plotly:** For generating visualizations.
- **Pandas:** For data manipulation.
- **WordCloud:** For generating word clouds.
- **Custom Cryptography Functions:** Implementing classical ciphers.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with any improvements or bug fixes.
