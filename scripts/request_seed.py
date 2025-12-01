# scripts/request_seed.py
import requests
from pathlib import Path

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
STUDENT_ID = "24a95a0513@aec.edu.in"   # <-- YOUR STUDENT ID
GITHUB_REPO_URL = "https://github.com/vinay-nethala/2fa-microservice-with-docker.git"

pub = Path("student_public.pem").read_text()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": pub.replace("\n", "\\n")
}

resp = requests.post(API_URL, json=payload, timeout=30)
resp.raise_for_status()

data = resp.json()
if data.get("status") == "success":
    Path("encrypted_seed.txt").write_text(data["encrypted_seed"])
    print("Saved encrypted_seed.txt")
else:
    print("Error:", data)