import streamlit as st
from vigenere import vigenere_cipher
from playfair import playfair_cipher
from hill import hill_cipher

# Tampilan Website dengan tab
st.title("Program Web Kriptografi")

tab1, tab2, tab3 = st.tabs(["Vigenere Cipher", "Playfair Cipher", "Hill Cipher"])

# Tab 1: Vigenère Cipher
with tab1:
    vigenere_cipher()

# Tab 2: Playfair Cipher
with tab2:
    playfair_cipher()

# Tab 3: Hill Cipher
with tab3:
    hill_cipher()
