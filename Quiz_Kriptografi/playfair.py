import streamlit as st
import io

def generate_playfair_matrix(key):
    matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    # Membuat kunci tanpa duplikat dengan urutan yang dipertahankan
    key_unique = ""
    for char in key.upper():
        if char not in key_unique:
            key_unique += char
    
    # Tambahkan sisa alfabet yang belum ada di kunci
    key_unique += "".join([char for char in alphabet if char not in key_unique])

    # Membuat matriks 5x5
    for i in range(5):
        matrix.append([key_unique[5 * i + j] for j in range(5)])

    return matrix

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    
    if len(plaintext) % 2 != 0:
        plaintext += "X"
    
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        row_a, col_a = next((r, c) for r, row in enumerate(matrix) for c, char in enumerate(row) if char == a)
        row_b, col_b = next((r, c) for r, row in enumerate(matrix) for c, char in enumerate(row) if char == b)

        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b] + matrix[row_b][col_a]

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row_a, col_a = next((r, c) for r, row in enumerate(matrix) for c, char in enumerate(row) if char == a)
        row_b, col_b = next((r, c) for r, row in enumerate(matrix) for c, char in enumerate(row) if char == b)

        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b] + matrix[row_b][col_a]

    return plaintext

# Tampilan Playfair Cipher
def playfair_cipher():
    st.header("Playfair Cipher")
    opsi = st.selectbox("Pilih opsi:", ("Enkripsi", "Dekripsi"), key="opsi_playfaircipher")
    kunci = st.text_input("Masukkan kunci (minimal 12 karakter):", key="kunci_playfaircipher")

    # Opsi untuk unggah file
    unggah_file = st.file_uploader("Pilih file", type="txt", key="file_playfaircipher")

    # Menangani pengunggahan file atau input teks manual
    if unggah_file is not None:
        text_input = io.StringIO(unggah_file.getvalue().decode("utf-8")).read().replace(" ", "")
        st.write("File berhasil diunggah!")
    else:
        text_input = st.text_area("Masukkan teks:", key="text_palyfaircipher")

    if st.button("Kirim", key="kirim_playfaircipher"):
        if len(kunci) < 12 or not kunci.isalpha():
             st.error("Kunci harus terdiri dari minimal 12 karakter!")
        elif not text_input or not text_input.replace(" ", "").isalpha():
            st.error("Teks harus berisi huruf!")
        else:
            text_input = text_input.replace(" ", "")
            if opsi == "Enkripsi":
                hasil = playfair_encrypt(text_input, kunci)
                st.success(f"Hasil cipherteks dari {text_input} adalah: {hasil}")
            elif opsi == "Dekripsi":
                hasil = playfair_decrypt(text_input, kunci)
                st.success(f"Hasil plaintext dari {text_input} adalah: {hasil}")
