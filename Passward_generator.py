import random
import string

def generate_password(length=12):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    all_chars = letters + digits + symbols
    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

print("Generated Password:", generate_password(12))
