# 🔑 Secure Password Generator

A secure, interactive Python utility designed to generate strong, customizable random passwords based on user-defined constraints.

Created by **[Vishnu S](https://github.com/vishnusadasivan2006)** as part of the **Oasis Infobyte Internship Project (OIBSIP)**.

---

## 🌟 Key Features

- 🔒 **Cryptographically Secure**: Built using Python's `secrets` module, which generates cryptographically strong random numbers suitable for managing secrets (passwords, tokens).
- ⚙️ **Interactive Step-by-Step Configuration**:
  - Set custom password lengths between 4 and 128 characters.
  - Individually toggle character types: lowercase (`a-z`), uppercase (`A-Z`), digits (`0-9`), and symbols (`!@#$%^&*...`).
- 🚫 **Exclusion of Visual Confusables**: Option to filter out custom characters (e.g. `0`, `O`, `o`, `1`, `l`, `I`) to avoid visual ambiguity.
- 🎯 **Guaranteed Character Types**: Guarantees that at least one character from each selected set is placed in the final password, ensuring compliance with strict password policies.
- 📊 **Strength Estimation**: Rates your configured password's strength (Weak, Medium, Strong, Very Strong) dynamically.
- 📋 **Clipboard Integration**: Automatically copies generated passwords to the clipboard (via `pyperclip`).
- 💾 **Batch Exporting**: Optionally appends generated passwords to a local `my_passwords.txt` file for future reference.

---

## 📋 Prerequisites & Installation

To use the optional clipboard-copying feature, install the `pyperclip` module:
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Generator

Run the script using:

```bash
python "VISHNU S_3.py"
```

---

## 💬 Sample Execution

```text
========================================================
           PASSWORD GENERATOR  v1.0
            Created by : VISHNU S
========================================================
  Generate strong passwords securely and instantly!
========================================================

[ STEP 1 ]  Set Password Length
  Tip: 12+ characters is recommended for security.

  Enter password length (4 to 128): 16

[ STEP 2 ]  Choose Character Types

  Include lowercase letters?  (a-z) (y/n): y
  Include uppercase letters?  (A-Z) (y/n): y
  Include numbers?            (0-9) (y/n): y
  Include symbols?            (!@#$...) (y/n): y

[ STEP 3 ]  Exclude Specific Characters  (optional)

  Example: type  0Oo1lI  to avoid visually confusing characters.
  Characters to exclude (or press Enter to skip): 0O1l

  Excluding: 0 O 1 l

[ STEP 4 ]  How Many Passwords?

  How many passwords to generate? (1 to 20): 3

  Strength  : [**]  VERY STRONG [excellent!]
  Pool size : 68 unique characters available

========================================================
  GENERATED PASSWORDS
========================================================
  [ 1]  g@H$vK7*mP9qZ_X2
  [ 2]  aB#3fD^9yJ*7cR-8
  [ 3]  xW+2kL!6nQ#5tP_9
========================================================

[ OPTIONS ]

  Copy the first password to clipboard? (y/n): y
  [OK] Password copied to clipboard!

  Save all passwords to a text file? (y/n): y
  [OK] Passwords saved to 'my_passwords.txt'

  Generate another set of passwords? (y/n): n

  Thanks for using the Password Generator!
  — Created by VISHNU S
```

---

## 📂 Folder Structure

```text
├── VISHNU S_Task3/
│   ├── VISHNU S_3.py       # Main Secure Password Generator script
│   ├── requirements.txt    # Clipboard copy dependencies (pyperclip)
│   └── README.md           # Project documentation (this file)
```
