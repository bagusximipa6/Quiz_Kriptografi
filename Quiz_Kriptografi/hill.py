import streamlit as st
import numpy as np
import io

alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def mod_inverse(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))  # Determinan dari matriks
    det_inv = pow(det, -1, modulus)  # Invers modulo dari determinan
    matrix_modulus_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % modulus
    return matrix_modulus_inv

def hill_encrypt(p, key_matrix):
    key_matrix = np.array(key_matrix)
    p_vector = [alphabets.index(c) for c in p]
    if len(p_vector) % 2 != 0:  # Memastikan panjang genap
        p_vector.append(alphabets.index('X'))  # Padding dengan 'X'
    p_matrix = np.array(p_vector).reshape(-1, 2)  # Matriks 2x2
    result = np.dot(p_matrix, key_matrix) % 26
    cipher_text = ''.join([alphabets[i] for i in result.flatten()])
    
    return cipher_text

def hill_decrypt(cipher_text, key_matrix):
    key_matrix_inv = mod_inverse(np.array(key_matrix), 26)
    cipher_vector = [alphabets.index(c) for c in cipher_text]  # Menggunakan huruf kapital
    cipher_matrix = np.array(cipher_vector).reshape(-1, 2)
    decrypted_matrix = (cipher_matrix.dot(key_matrix_inv)) % 26
    decrypted_text = ''.join([alphabets[i] for i in decrypted_matrix.flatten()])

    return decrypted_text

def hill_cipher():
    st.header("Hill Cipher")

    opsi = st.selectbox("Pilih opsi:", ("Enkripsi", "Dekripsi"), key="hill_option")
    unggah_file = st.file_uploader("Pilih file", type="txt", key="hill_file")

    if unggah_file is not None:
        text_input = io.StringIO(unggah_file.getvalue().decode("utf-8")).read().replace(" ", "")
        st.write("File berhasil diupload!")
    else:
        text_input = st.text_area("Masukkan teks:", key="hill_text")
        
    st.write("Masukkan nilai matriks kunci 2x2:")
    kunci_matriks = [
        [st.number_input("Key Matrix[1][1]:", value=0, key="hill_key_1_1"), 
         st.number_input("Key Matrix[1][2]:", value=0, key="hill_key_1_2")],
        [st.number_input("Key Matrix[2][1]:", value=0, key="hill_key_2_1"), 
         st.number_input("Key Matrix[2][2]:", value=0, key="hill_key_2_2")]
    ]
    
    if st.button("Kirim", key="hill_submit"):
        if not text_input or not text_input.replace(" ", "").isalpha():
            st.error("Teks harus berisi huruf!")
        else:
            text_input = text_input.upper().replace(" ", "")  # Mengubah menjadi huruf kapital
            if opsi == "Enkripsi":
                hasil = hill_encrypt(text_input, kunci_matriks)
                st.success(f"Hasil cipherteks dari {text_input} adalah: {hasil}")
            elif opsi == "Dekripsi":
                hasil = hill_decrypt(text_input, kunci_matriks)
                st.success(f"Hasil plaintext dari {text_input} adalah: {hasil}")
