import json
from pathlib import Path
from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import datetime
import pyotp

# Paths
SEED_FILE = Path("seed.json")
PRIVATE_KEY_FILE = Path(__file__).parent.parent / "student_private.pem"  # Update if your private key path is different

def decrypt_encrypted_seed(encrypted_seed_b64, private_key_path):
    with open(private_key_path, "rb") as f:
        private_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_bytes = b64decode(encrypted_seed_b64)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    return decrypted_bytes.hex()

def generate_2fa_code_from_hex_seed(hex_seed):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_utc} - Your 2FA Code: {code}")
    return code

def main():
    # 1. Read encrypted_seed from seed.json
    if not SEED_FILE.exists():
        print("ERROR: seed.json file not found! Run request_seed.py first.")
        return

    data = json.loads(SEED_FILE.read_text())
    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        print("ERROR: 'encrypted_seed' not found in seed.json!")
        return

    # 2. Decrypt seed using private key
    try:
        hex_seed = decrypt_encrypted_seed(encrypted_seed, PRIVATE_KEY_FILE)
    except Exception as e:
        print(f"ERROR decrypting seed: {e}")
        return

    # 3. Generate and print 2FA code
    try:
        generate_2fa_code_from_hex_seed(hex_seed)
    except Exception as e:
        print(f"ERROR generating 2FA code: {e}")

if __name__ == "__main__":
    main()
