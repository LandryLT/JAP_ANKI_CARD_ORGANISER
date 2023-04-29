import hashlib
import hmac
import pickle
import secrets
import string
import random
import sys
from os import path

secret_key_file = path.join(path.dirname(path.realpath(__file__)) ,".secret_key")

# Raise if file has wrong signature
class InvalidSignature(Exception):
    def __init__(self, file) -> None:
        self.message = file + " has an invalid signature and could be potentially harmful to your machine."
        super().__init__(self.message)

# Raise if no .secret_key file is found
class UserKeyNotFound(Exception):
     def __init__(self) -> None:
        self.message = "To ensure that no harmful code can run through this code, please create a file .secret_key file with your secret key"
        super().__init__(self.message) 

# Check for key in folder, create one if missing
def check_key(working_dir):
    if not path.isfile(path.join(working_dir, ".secret_key")):
        print("No secret key found, creating a new one")
        chars = string.ascii_letters.join(string.punctuation).join(string.digits)
        new_key = ''
        for x in range(100):
            if random.randint(0, 100) < 80:
                new_key += chars[random.randint(0, 14805)]
            else:
                new_key += string.punctuation[random.randint(0, 31)]
        with open(path.join(working_dir, ".secret_key"), 'w') as key_file:
            key_file.write(new_key)

# Quick read file simplification
def read_file_data (filepath, flag= 'rb'):
    with open(filepath, flag) as f:
        return f.read()


# Save a pickled file with hmac signature
def save_secure_pickle (obj, filepath):
    # Max Lim 1000 WWWJDIC words
    sys.setrecursionlimit(700000)
    data = pickle.dumps(obj)
    #Get key from your own personnal .secret_key
    try:
        u_key = read_file_data(secret_key_file)
    except FileNotFoundError:
        raise UserKeyNotFound
    
    digest = hmac.new(u_key, data, hashlib.blake2b).hexdigest()
    with open(filepath, 'wb') as output:
        output.write(digest.encode('utf-8'))
        output.write('<keydataseparator>'.encode('utf-8'))
        output.write(data)
    sys.setrecursionlimit(1000)

# Load a pickled file with hmac signature
def load_secure_pickle (filepath):
    data = read_file_data(filepath)
    digest, pickle_data = data.split('<keydataseparator>'.encode('utf-8'))
    #Get key from your own personnal .secret_key
    try:
        u_key = read_file_data(secret_key_file)
    except FileNotFoundError:
        raise UserKeyNotFound
    
    expected_digest = hmac.new(u_key, pickle_data, hashlib.blake2b).hexdigest()
    try:
        if not secrets.compare_digest(digest, expected_digest.encode('utf-8')):
            raise InvalidSignature(filepath)
        else:
            return pickle.loads(pickle_data)
    except:
        raise
