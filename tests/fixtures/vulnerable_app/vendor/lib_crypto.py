def aes_gcm_encrypt(key, plaintext):
    return b"encrypted-data"

def insecure_des_decrypt(key, ciphertext):
    # CVE-2024-99001 vulnerable function - Unreachable in main.py
    return b"plaintext"
