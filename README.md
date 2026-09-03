# 🛡️ PyFIM – File Integrity Monitoring Tool

A lightweight Python-based **File Integrity Monitoring (FIM)** tool that detects unauthorized file changes by generating and comparing **SHA-256** hash values.

This project was built to demonstrate practical cybersecurity concepts including hashing, file integrity verification, JSON data storage, and Python automation.

---

## 📌 Features

- Generate **SHA-256** hashes for files
- Store hashes in a local JSON database
- Detect **new**, **modified**, **deleted**, and **unchanged** files
- Generate a detailed scan report
- Update the hash database after user confirmation

---

## 🖥️ How It Works

1. User enters the directory path to scan.
2. PyFIM loads the existing `hashes.json` database.
3. Each file's SHA-256 hash is generated.
4. The current hashes are compared with the stored hashes.
5. A scan report is displayed.
6. The user chooses whether to update the database.

---

## 📂 Project Structure

```text
PyFIM/
│
├── main.py          # Main application
├── hashes.json      # Hash database (generated automatically)
└── README.md

```

---

## ▶️ Usage

Run the program:

```bash
python main.py
```

Example:

```text
================== PyFIM ==================

Enter directory path:
/home/kali/Documents

Hidden files/folders detected. Include them in the scan? (Y/N): N

Scanning...

================ Scan Report ================

Total files scanned : 5
Unchanged files     : 3
New files           : 1
Modified files      : 1
Deleted files       : 0

Update hash database? (Y/N):
```

---

# 🧠 Cybersecurity Concepts Used

## 1. File Integrity Monitoring (FIM)

**Definition:** A security technique used to detect unauthorized modifications to files by comparing their current state with a trusted baseline.

**Real-world use:** Enterprise servers, SOC environments, malware detection, compliance monitoring.

---

## 2. SHA-256 Hashing

**Purpose:** Generate a unique fingerprint for a file.

- Same file + same algorithm = Same hash
- Even a one-byte change produces a completely different hash
- Used for **integrity**, not encryption

Example:

```text
hello.txt
↓
SHA-256
↓
a591a6d40bf420404a011733...
```

---

## 3. Why Files Are Opened in Binary Mode (`rb`)

Binary mode reads the **raw bytes** of a file rather than text.

This allows the program to hash **any file type**:

- TXT
- PDF
- JPG
- ZIP
- EXE

---

## 4. Chunk-Based File Reading

Instead of loading an entire file into RAM, PyFIM reads **4096 bytes** at a time.

```python
for chunk in iter(lambda: f.read(4096), b""):
```

### Why 4096?

- 4096 bytes = **4 KB**
- Common memory page and buffer size
- Efficient for large files
- Keeps memory usage low

---

## 5. JSON as a Lightweight Database

PyFIM stores hashes inside `hashes.json`.

Example:

```json
{
    "notes.txt": {
        "hash": "3a7bd3e2360a...",
        "algorithm": "SHA-256"
    }
}
```

JSON is **not a database engine** like SQL; it's a structured text format used here for lightweight persistent storage.

---

## 6. Python Concepts Used

| Concept | Purpose |
|----------|---------|
| `hashlib` | Generate SHA-256 hashes |
| `os` | File & directory operations |
| `json` | Load and save the hash database |
| `with open()` | Safe file handling |
| Dictionary | Store filename → hash mappings |
| Set | Efficient deleted-file detection |
| Functions | Modular program architecture |

---

# 🔍 Detection Categories

| Status | Meaning |
|---------|----------|
| 🟢 Unchanged | File matches stored hash |
| 🟡 New | File not present in database |
| 🔴 Modified | Hash differs from stored value |
| ⚫ Deleted | Previously tracked file no longer exists |

---

# 🚀 Future Improvements

- Recursive directory scanning (`os.walk`)
- Multiple hashing algorithms (SHA-512, MD5)
- Timestamp & file size metadata
- Export reports to PDF/CSV
- Real-time monitoring using filesystem events
- Command-line arguments instead of interactive input

---

## 👨‍💻 Author

**Hussamuddin**

A beginner cybersecurity project focused on understanding how real-world File Integrity Monitoring tools verify the integrity of files using cryptographic hashing.