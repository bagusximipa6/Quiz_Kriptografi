import streamlit as st
import io

def vigenere_encrypt(plaintext, key):
    key = key.upper()
    ciphertext = ""
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - offset + ord(key[key_index]) - 65) % 26 + offset)
            ciphertext += encrypted_char
            key_index = (key_index + 1) % len(key)
        else:
            ciphertext += char
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted_char = chr((ord(char) - offset - (ord(key[key_index]) - 65)) % 26 + offset)
            plaintext += decrypted_char
            key_index = (key_index + 1) % len(key)
        else:
            plaintext += char
    return plaintext

def vigenere_cipher():
    st.header("Vigenere Cipher")

    opsi = st.selectbox("Pilih opsi:", ("Enkripsi", "Dekripsi"), key="opsi_vigenerecipher")
    kunci = st.text_input("Masukkan kunci (minimal 12 karakter):", key="kunci_vigenerecipher")

    # Opsi untuk unggah file
    unggah_file = st.file_uploader("Pilih file", type="txt", key="file_vigenerecipher")

    # Menangani pengunggahan file atau input teks manual
    if unggah_file is not None:
        text_input = io.StringIO(unggah_file.getvalue().decode("utf-8")).read().replace(" ", "")
        st.write("File berhasil diunggah!")
    else:
        text_input = st.text_area("Masukkan teks:", key="text_vigenerecipher")

    if st.button("Kirim", key="kirim_vigenerecipher"):
        if len(kunci) < 12 or not kunci.isalpha():
            st.error("Kunci harus terdiri dari minimal 12 karakter!")
        elif not text_input or not text_input.replace(" ", "").isalpha():
            st.error("Teks harus berisi huruf!")
        else:
            text_input = text_input.replace(" ", "")
            if opsi == "Enkripsi":
                hasil = vigenere_encrypt(text_input, kunci)
                st.success(f"Hasil cipherteks dari {text_input} adalah: {hasil}")
            elif opsi == "Dekripsi":
                hasil = vigenere_decrypt(text_input, kunci)
                st.success(f"Hasil plaintext dari {text_input} adalah: {hasil}")
