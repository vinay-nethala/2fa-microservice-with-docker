#!/usr/bin/env python3
from pathlib import Path
from app.totp_utils import generate_totp_code
from datetime import datetime, timezone

SEED_FILE = Path("/data/seed.txt")
OUT_FILE = Path("/cron/last_code.txt")

def main():
    try:
        if not SEED_FILE.exists():
            print("ERROR: seed not found", flush=True)
            return
        seed = SEED_FILE.read_text().strip()
        code = generate_totp_code(seed)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with OUT_FILE.open("a") as f:
            f.write(f"{ts} - 2FA Code: {code}\n")
    except Exception as e:
        print("CRON ERROR:", e, flush=True)

if __name__ == "__main__":
    main()
