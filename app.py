import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_card import card
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import spacy 
import io
from itertools import permutations
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('onw-1.4')

st.set_page_config(page_title="CipherSolver", page_icon="🔐",layout="wide")
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    return [token.text for token in doc if token.is_alpha and not token.is_stop]

def caesar_cipher(text, shift):
    encrypted = []
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def vigenere_cipher(text, key):
    key = preprocess_text(key)
    key_repeated = ''.join(key) * (len(text) // len(key) + 1)
    encrypted = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            shift = ord(key_repeated[i % len(key)]) - shift_base
            encrypted.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def rail_fence_cipher(text, num_rails):
    fence = [[] for _ in range(num_rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    return ''.join(''.join(row) for row in fence)

def simple_columnar_transposition(text, columns):
    grid = [text[i:i + columns] for i in range(0, len(text), columns)]
    cipher_text = ''
    for col in range(columns):
        for row in grid:
            if col < len(row):
                cipher_text += row[col]
    return cipher_text

def caesar_cipher_decrypt(text, shift):
    decrypted = []
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            decrypted.append(chr((ord(char) - shift_base - shift) % 26 + shift_base))
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def vigenere_cipher_decrypt(text, key):
    key = preprocess_text(key)
    key_repeated = ''.join(key) * (len(text) // len(key) + 1)
    decrypted = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            shift = ord(key_repeated[i % len(key)]) - shift_base
            decrypted.append(chr((ord(char) - shift_base - shift) % 26 + shift_base))
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def rail_fence_cipher_decrypt(text, num_rails):
    pattern = [0] * len(text)
    rail = 0
    direction = 1
    for i in range(len(text)):
        pattern[i] = rail
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    sorted_indices = sorted(range(len(pattern)), key=lambda x: pattern[x])
    decrypted = [''] * len(text)
    for i, index in enumerate(sorted_indices):
        decrypted[index] = text[i]
    return ''.join(decrypted)

def simple_columnar_transposition_decrypt(text, columns):
    rows = len(text) // columns
    extra = len(text) % columns
    grid = [''] * columns
    idx = 0
    for col in range(columns):
        end = rows + (1 if col < extra else 0)
        grid[col] = text[idx:idx + end]
        idx += end

    decrypted = []
    for row in range(rows + (1 if extra else 0)):
        for col in range(columns):
            if row < len(grid[col]):
                decrypted.append(grid[col][row])
    return ''.join(decrypted)

def cryptogram_solver():
     st.title("Cryptogram Solver")
     st.subheader("Cryptography techniques Settings")
     mode = option_menu("Select Mode", ["Encrypt", "Decrypt"],orientation="horizontal")
     method = st.selectbox("Select Method", 
                                   ["Caesar Cipher", "Vigenere Cipher", "Rail Fence Cipher", "Simple Columnar Transposition"])
     placeholder = "Enter plain text to encrypt:" if mode == "Encrypt" else "Enter cipher text to decrypt:"
     text = st.text_area(placeholder)

     shift = st.slider("Shift Value (for Caesar Cipher)", 1, 25, 3) if method == "Caesar Cipher" else None
     key = st.text_input("Key (for Vigenere Cipher):") if method == "Vigenere Cipher" else None
     rails = st.slider("Number of Rails (for Rail Fence Cipher)", 2, 10, 3) if method == "Rail Fence Cipher" else None
     columns = st.slider("Number of Columns (for Columnar Transposition)", 2, 10, 4) if method == "Simple Columnar Transposition" else None

     if st.button(f"{mode} Text"):
        if text.strip():
            if method == "Caesar Cipher":
                result = caesar_cipher(text, shift) if mode == "Encrypt" else caesar_cipher_decrypt(text, shift)
            elif method == "Vigenere Cipher":
                if key:
                    result = vigenere_cipher(text, key) if mode == "Encrypt" else vigenere_cipher_decrypt(text, key)
                else:
                    st.error("Please provide a key for Vigenere Cipher.")
                    result = None
            elif method == "Rail Fence Cipher":
                result = rail_fence_cipher(text, rails) if mode == "Encrypt" else rail_fence_cipher_decrypt(text, rails)
            elif method == "Simple Columnar Transposition":
                result = simple_columnar_transposition(text, columns) if mode == "Encrypt" else simple_columnar_transposition_decrypt(text, columns)
            else:
                result = None

            if result:
                st.subheader(f"{mode}ed Text:")
                st.code(result)
        else:
            st.error("Please enter valid text.")

def analyze_frequencies(text, n=1):
    text = ''.join(filter(str.isalpha, text.lower()))  
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)] 
    return Counter(ngrams)

def frequency_analysis():
        st.title("📊 Frequency Analysis")
        st.subheader("Analyze the frequency of letters, digraphs, and trigraphs in a given text.")
    
        st.markdown("### ✏️ Enter text or upload a file:")
        user_input = st.text_area("Input Text", placeholder="Type or paste text to analyze...", height=150)

        uploaded_file = st.file_uploader("Or upload a text file", type=["txt"])
   
        if uploaded_file is not None:
            user_input = uploaded_file.read().decode("utf-8")
   
        st.markdown("### ⚙️ Choose Analysis Type")
        analysis_type = st.radio("Select the type of frequency analysis:", ["Letters", "Digraphs", "Trigraphs"])

        if st.button("Analyze"):
            if user_input.strip():
                n = 1 if analysis_type == "Letters" else 2 if analysis_type == "Digraphs" else 3
                frequencies = analyze_frequencies(user_input, n=n)
                sorted_frequencies = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))
            
                df = pd.DataFrame(sorted_frequencies, columns=["N-gram", "Frequency"])
            
                st.markdown("### 📈 Frequency Distribution")
                fig = px.bar(
                df,
                x="N-gram",
                y="Frequency",
                title=f"{analysis_type} Frequency Analysis",
                labels={"N-gram": f"{analysis_type}", "Frequency": "Count"},
                text="Frequency",
                )
                fig.update_traces(textposition="outside", marker_color="skyblue")
                fig.update_layout(
                xaxis_title=f"{analysis_type}",
                yaxis_title="Frequency",
                title_font_size=18,
                title_x=0.5,
                template="plotly_white",
            )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### ☁️ Word Cloud (Letter Frequency)")
                wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
                fig_wordcloud = plt.figure(figsize=(8, 4))
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                st.pyplot(fig_wordcloud)
            
                st.markdown("### 🍰 Pie Chart (Letter Frequency Distribution)")
                fig_pie = px.pie(
                    df,
                    names="N-gram",
                values="Frequency",
                title=f"{analysis_type} Frequency Distribution",
                template="plotly_white"
            )
                st.plotly_chart(fig_pie, use_container_width=True)
           
                st.markdown("### 📋 Frequency Table")
                st.dataframe(df)
            
                st.markdown("### 💾 Download Results")
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="frequency_analysis.csv",
                mime="text/csv",
            )
            else:
                st.warning("⚠️ Please enter text or upload a file to analyze.")

def is_valid_phrase(phrase):
    words = phrase.split()
    return all(wordnet.synsets(word) for word in words)

def get_synonyms_antonyms(word):
    synonyms = set()
    antonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                antonyms.update([ant.name() for ant in lemma.antonyms()])
    return synonyms, antonyms

def anagram_solver():
    st.title("Enhanced Anagram Solver")
    st.subheader("Solve Anagrams with NLP Features")

    mode = st.radio("Select Mode", ["Generate Anagrams", "Check Anagram Pair"])

    if mode == "Generate Anagrams":
        text = st.text_area("Enter a word or phrase to find anagrams:")
    else:
        word1 = st.text_input("Enter the first word or phrase:")
        word2 = st.text_input("Enter the second word or phrase:")

    n = st.slider("Choose the number of Anagrams to display", 1, 500, 10)

    if st.button("Solve"):
        if mode == "Generate Anagrams":
            if text.strip():
                cleaned_text = text.replace(" ", "").lower()
                anagrams = sorted(set(
                    " ".join(p).strip()
                    for p in permutations(cleaned_text)
                    if is_valid_phrase(" ".join(p).strip())
                ))

                st.subheader(f"Anagrams for '{text}':")
                
                if anagrams:
                    st.write(", ".join(anagrams[:n]))
                    if len(anagrams) > n:
                        st.write("...and more")
                else:
                    st.warning("No valid anagrams found!")

                st.subheader("Synonym and Antonym Suggestions")
                for word in text.split():
                    synonyms, antonyms = get_synonyms_antonyms(word.lower())
                    st.write(f"**Word:** {word}")
                    st.write(f"**Synonyms:** {', '.join(synonyms)}")
                    st.write(f"**Antonyms:** {', '.join(antonyms)}")

            else:
                st.error("Please enter a valid word or phrase.")

        elif mode == "Check Anagram Pair":
            if word1.strip() and word2.strip():
                normalized1 = "".join(sorted(word1.replace(" ", "").lower()))
                normalized2 = "".join(sorted(word2.replace(" ", "").lower()))

                if normalized1 == normalized2:
                    st.success(f"'{word1}' and '{word2}' are anagrams!")
                else:
                    st.error(f"'{word1}' and '{word2}' are not anagrams.")
            else:
                st.error("Please enter valid inputs for both words or phrases.")
  
def home_page():
    st.title("🔐 CipherSolver")
    st.title("🧠 NLP Meets Cryptography")  
    st.title("Welcome to **CipherSolver**, your one-stop solution for solving")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        res = card(
    title="Cryptogram Solver📝",
    text="Decode substitution ciphers with ease.",
    image="https://tse4.mm.bing.net/th?id=OIP.HkyK0YzSJ3V6742FwbuNgQHaE8&pid=Api&P=0&h=180",
    styles={
        "card": {
            "width": "300px",
            "height": "300px",
            "border-radius": "60px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
       
        },
        "text": {
            "font-family": "serif",

        }
    }
)

    with col2:
        res = card(
    title="Anagram Solver🔄",
    text="Rearrange letters into meaningful words.",
    image="https://plus.unsplash.com/premium_photo-1687509673996-0b9e35d58168?w=1000&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YW5hZ3JhbXN8ZW58MHx8MHx8fDA%3D",
    styles={
        "card": {
            "width": "300px",
            "height": "300px",
            "border-radius": "60px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
       
        },
        "text": {
            "font-family": "serif",

        }
    }
)

    with col3:
        res = card(
    title="Frequency Analysis📊",
    text="Analyze text patterns and distributions.",
    image="https://tse3.mm.bing.net/th?id=OIP.pNrAbVpZZk8C9rngPfapMAHaEN&pid=Api&P=0&h=180",
    styles={
        "card": {
            "width": "300px",
            "height": "300px",
            "border-radius": "60px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
       
        },
        "text": {
            "font-family": "serif",

        }
    }
)

def main():

    with st.sidebar:
        menu = option_menu("CipherSolver",["Home","Frequency Analysis","Cryptogram Solver","Anagram Solver"],icons=["house","bar-chart", "puzzle", "sort-alpha-down"],menu_icon="menu-app",default_index=0)
    
    if menu == "Home":
        home_page()

    if menu == "Frequency Analysis":
        frequency_analysis()
    
    if menu == "Cryptogram Solver":
        cryptogram_solver()
    
    if menu == "Anagram Solver":
        anagram_solver()
              
if __name__ == "__main__":
    main()