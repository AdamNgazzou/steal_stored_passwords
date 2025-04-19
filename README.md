# 🔐 Chrome Password Extractor

A powerful Python tool (compiled into `.exe`) that extracts saved login credentials—including URLs, usernames, passwords, and timestamps—from all Chrome profiles on a Windows machine. The data is saved in both CSV and JSON formats for easy usage and analysis.

---

## ⚠️ Disclaimer

This tool is for **educational and personal recovery purposes only**. Unauthorized access or extraction of credentials is **illegal and unethical**. Use responsibly.

---

## 📦 Features

✅ Extracts credentials from all Chrome profiles (`Default`, `Profile 1`, `Profile 2`, etc.)  
✅ Decrypts Chrome's AES-encrypted passwords  
✅ Recovers:
- Website URL  
- Username  
- Password  
- Time created (if available)  

✅ Exports results to:
- `chrome_passwords.csv`  
- `chrome_passwords.json`  

✅ Includes robust error handling and fallback to DPAPI if AES decryption fails  
✅ Stores error logs on Desktop if any issues occur  

---

## 🖥️ Requirements

**For .exe Users:**  
No setup required.

**For Source Code Users:**  
Install dependencies:

```bash
pip install pycryptodome pypiwin32
