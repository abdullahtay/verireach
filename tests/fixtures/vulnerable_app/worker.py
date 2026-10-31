from vendor.lib_crypto import aes_gcm_encrypt

def background_task(payload):
    # Only calls safe encryption
    return aes_gcm_encrypt("secret", payload)
