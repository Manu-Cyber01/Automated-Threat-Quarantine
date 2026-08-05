import hashlib
import json
import os
import shutil
from pathlib import Path

def load_signatures(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["hash"]: item for item in data.get("signatures", [])}

def hash_file(file_path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def scan_folder(target_dir, signatures):
    results = []
    target_dir = Path(target_dir)

    for root, _, files in os.walk(target_dir):
        for name in files:
            file_path = Path(root) / name

            if file_path.name in {"signatures.json", "report.json"}:
                continue

            try:
                file_hash = hash_file(file_path)
                matched = signatures.get(file_hash)

                results.append({
                    "file": str(file_path),
                    "hash": file_hash,
                    "status": "infected" if matched else "clean",
                    "signature": matched
                })
            except Exception as e:
                results.append({
                    "file": str(file_path),
                    "hash": None,
                    "status": "error",
                    "error": str(e)
                })

    return results

def quarantine_file(file_path, quarantine_dir="quarantine"):
    quarantine_dir = Path(quarantine_dir)
    quarantine_dir.mkdir(exist_ok=True)

    src = Path(file_path)
    dst = quarantine_dir / src.name
    shutil.move(str(src), str(dst))
    return str(dst)