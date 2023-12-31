import secrets

def generate_token():
    return secrets.token_urlsafe(16)

token = generate_token()
print(f"توکن شما: {token}")

#fixed_token = "xEvHRRA-27abEXrHsG2Tfg"