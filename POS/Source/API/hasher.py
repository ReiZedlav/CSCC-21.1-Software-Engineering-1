import bcrypt

def hash_password(password):
    """Hash a password using bcrypt"""
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Convert bytes to string for storage

# Example usage:
password = "1"
hashed = hash_password(password)
print(f"Original: {password}")
print(f"Hashed: {hashed}")
# Store 'hashed' in your database