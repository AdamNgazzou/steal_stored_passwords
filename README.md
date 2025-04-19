🔐 Chrome Password Extractor
A powerful Python tool (compiled into .exe) that extracts saved login credentials—including URLs, usernames, passwords, and timestamps—from all Chrome profiles on a Windows machine. The data is saved in both CSV and JSON formats for easy usage and analysis.

⚠️ Disclaimer
This tool is for educational and personal recovery purposes only. Unauthorized access or extraction of credentials is illegal and unethical. Use responsibly.

📦 Features
✅ Extracts credentials from all Chrome profiles (Default, Profile 1, 2, etc.)

✅ Decrypts Chrome's AES-encrypted passwords

✅ Recovers:

Website URL

Username

Password

Time created (if available)

✅ Exports results to:

chrome_passwords.csv

chrome_passwords.json

✅ Includes robust error handling and fallback to DPAPI if AES decryption fails

✅ Stores error logs on Desktop if any issues occur

🖥️ Requirements
If you're running the .exe file, no setup is required.

If you're running from source, install the following:

bash
Copy
Edit
pip install pycryptodome pypiwin32
📂 Output
After running, you’ll find:

chrome_passwords.csv – Tabular format for Excel/sheets

chrome_passwords.json – Structured data for devs or backups

If any error occurs, it's logged in:

Desktop/error_log.txt

🚀 Usage
Double-click the compiled .exe file.

Wait for extraction to complete.

The output files will be saved in the same directory as the executable.

If you're running the Python file directly:

bash
Copy
Edit
python extract_chrome_passwords.py
⚙️ How It Works
Reads Chrome's Login Data SQLite database for each profile.

Uses the AES key from Chrome's Local State, decrypted with Windows DPAPI.

Decrypts each password entry using AES-GCM.

Converts Chrome's timestamp format (microseconds since 1601) to a readable date.

Outputs the cleaned data.

🛠️ Tech Stack
Python 3.x

sqlite3, json, os, win32crypt, Crypto.Cipher.AES

Optional: PyInstaller to compile into .exe

🔒 Ethical Use Cases
Recover your own saved credentials

Audit your own Chrome profiles

Learn about browser encryption mechanisms

❌ Prohibited Use
Extracting credentials from others’ computers without explicit permission

Using this tool for phishing, identity theft, or malicious hacking

👨‍💻 Author
Created by a privacy-conscious developer for educational and recovery purposes.

Let me know if you'd like to personalize this with your name or GitHub link!







