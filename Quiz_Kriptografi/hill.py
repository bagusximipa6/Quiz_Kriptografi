import streamlit as st
import numpy as np
import io
from math import gcd

alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def mod_inverse(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))  # Determinan dari matriks
    det_inv = pow(det, -1, modulus)  # Invers modulo dari determinan
    matrix_modulus_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % modulus
    return matrix_modulus_inv

def hill_encrypt(plaintext, key_matrix):
    key_matrix = np.array(key_matrix)
    p_vector = [alphabets.index(c) for c in plaintext]
    if len(p_vector) % 2 != 0:  # Memastikan panjang genap
        p_vector.append(alphabets.index('X'))  # Padding dengan 'X'
    p_matrix = np.array(p_vector).reshape(-1, 2)  # Matriks 2x2
    result = np.dot(p_matrix, key_matrix) % 26
    cipher_text = ''.join([alphabets[i] for i in result.flatten()])
    
    return cipher_text

def hill_decrypt(cipher_text, key_matrix):
    key_matrix = np.array(key_matrix)
    key_matrix_inv = mod_inverse(key_matrix, 26)  # Menghitung invers dari kunci
    cipher_vector = [alphabets.index(c) for c in cipher_text]
    cipher_matrix = np.array(cipher_vector).reshape(-1, 2)
    decrypted_matrix = (cipher_matrix.dot(key_matrix_inv) % 26).astype(int)
    decrypted_text = ''.join([alphabets[i] for i in decrypted_matrix.flatten()])

    return decrypted_text

def hill_cipher():
    st.header("Hill Cipher")

    option = st.selectbox("Pilih opsi:", ("Enkripsi", "Dekripsi"), key="hill_option")
    uploaded_file = st.file_uploader("Pilih file", type="txt", key="hill_file")

    if uploaded_file is not None:
        text_input = io.StringIO(uploaded_file.getvalue().decode("utf-8")).read().replace(" ", "")
        st.write("File berhasil diupload!")
    else:
        text_input = st.text_area("Masukkan teks:", key="hill_text")

    key_text = st.text_input("Masukkan kunci (minimal 12 karakter):", key="hill_key")

    if st.button("Kirim", key="hill_submit"):
        if len(key_text) < 12 or not key_text.isalpha():
            st.error("Kunci harus terdiri dari minimal 12 karakter!")
        elif not text_input or not text_input.replace(" ", "").isalpha():
            st.error("Teks harus berisi huruf!")
        else:
            text_input = text_input.upper().replace(" ", "")  # Mengubah menjadi huruf kapital
            
            # Mengonversi kunci menjadi matriks 2x2
            key_matrix = [[alphabets.index(key_text[i]), alphabets.index(key_text[i + 1])]
            for i in range(0, 4, 2)]

            try:
                if option == "Enkripsi":
                    result = hill_encrypt(text_input, key_matrix)
                    st.success(f"Hasil cipherteks dari {text_input} adalah: {result}")
                elif option == "Dekripsi":
                    result = hill_decrypt(text_input, key_matrix)
                    st.success(f"Hasil plaintext dari {text_input} adalah: {result}")
            except ValueError as e:
                st.error(str(e))
