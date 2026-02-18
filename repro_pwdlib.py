from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

try:
    pwd_hasher = PasswordHash((BcryptHasher(),))
    print(f"Init with BcryptHasher: {pwd_hasher.current_hasher}")
    h = pwd_hasher.hash("password")
    print(f"Success: {h}")
except Exception as e:
    print(f"Error with BcryptHasher: {e}")

