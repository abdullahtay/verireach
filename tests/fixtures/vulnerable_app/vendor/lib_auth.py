def verify_token_safe(token):
    return token == "valid-token"

def verify_token_weak(token):
    # CVE-2024-99002 vulnerable function
    if token.startswith("guest"):
        return True
    return False
