import secrets
import string
import hashlib

def generate_api_key():
    characters = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(characters) for _ in range(48))
    api_key = f"myapi-{random_part}"
    return api_key

def hash_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()
