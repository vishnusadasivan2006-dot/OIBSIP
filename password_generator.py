# ================================================================
#   Password Generator - Command Line Tool
#   Created by  : VISHNU S
#   Project     : Python Internship Project
#   Description : Generates strong, random passwords based on
#                 user-defined length and character preferences.
# ================================================================

import random
import string
import secrets   # more secure than random for password generation
import sys
import os

# Try importing pyperclip — needed for clipboard copy feature
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


# ---------------------------------------------------------------
# Character sets we'll work with
# ---------------------------------------------------------------
LOWERCASE  = string.ascii_lowercase          # a-z
UPPERCASE  = string.ascii_uppercase          # A-Z
DIGITS     = string.digits                   # 0-9
SYMBOLS    = "!@#$%^&*()-_=+[]{}|;:,.<>?"   # safe common symbols


# ---------------------------------------------------------------
# Helper: Banner
# ---------------------------------------------------------------
def show_banner():
    """Prints a nice header when the program launches."""
    print("\n" + "=" * 56)
    print("           PASSWORD GENERATOR  v1.0")
    print("            Created by : VISHNU S")
    print("=" * 56)
    print("  Generate strong passwords right from your terminal!")
    print("=" * 56 + "\n")


# ---------------------------------------------------------------
# Helper: Yes / No input
# ---------------------------------------------------------------
def ask_yes_no(prompt):
    """
    Keeps asking until the user gives a valid y/n answer.
    Returns True for yes, False for no.
    """
    while True:
        reply = input(f"  {prompt} (y/n): ").strip().lower()
        if reply in ("y", "yes"):
            return True
        elif reply in ("n", "no"):
            return False
        else:
            print("    [!] Please type 'y' for yes or 'n' for no.")


# ---------------------------------------------------------------
# Helper: Integer input with range validation
# ---------------------------------------------------------------
def ask_int(prompt, min_val, max_val):
    """
    Asks for an integer input and validates it within [min_val, max_val].
    Keeps looping until the user enters something valid.
    """
    while True:
        try:
            value = int(input(f"  {prompt}").strip())
            if min_val <= value <= max_val:
                return value
            else:
                print(f"    [!] Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("    [!] That doesn't look like a number. Try again.")


# ---------------------------------------------------------------
# Core: Build character pool
# ---------------------------------------------------------------
def build_pool(use_lower, use_upper, use_digits, use_symbols, excluded):
    """
    Combines selected character sets into one big pool string.
    Then removes any characters the user wants to exclude.
    """
    pool = ""

    if use_lower:
        pool += LOWERCASE
    if use_upper:
        pool += UPPERCASE
    if use_digits:
        pool += DIGITS
    if use_symbols:
        pool += SYMBOLS

    # Exclude user-specified characters
    for ch in excluded:
        pool = pool.replace(ch, "")

    # Remove duplicates (just in case) while keeping order
    seen = set()
    clean_pool = ""
    for ch in pool:
        if ch not in seen:
            seen.add(ch)
            clean_pool += ch

    return clean_pool


# ---------------------------------------------------------------
# Core: Password strength checker
# ---------------------------------------------------------------
def check_strength(length, use_lower, use_upper, use_digits, use_symbols):
    """
    Gives a rough strength rating based on:
    - password length
    - how many character types are used

    Not a perfect algorithm but covers the basics well.
    """
    score = 0

    # Points for length
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if length >= 20:
        score += 1

    # Points for character variety
    variety = sum([use_lower, use_upper, use_digits, use_symbols])
    score += variety

    # Classify
    if score <= 2:
        label = "WEAK       [low length or low variety]"
        icon  = "[!!]"
    elif score <= 4:
        label = "MEDIUM     [decent but can be stronger]"
        icon  = "[~]"
    elif score <= 6:
        label = "STRONG     [good length and variety]"
        icon  = "[OK]"
    else:
        label = "VERY STRONG [excellent!]"
        icon  = "[**]"

    return f"{icon}  {label}"


# ---------------------------------------------------------------
# Core: Generate one password
# ---------------------------------------------------------------
def generate_password(length, pool, use_lower, use_upper, use_digits, use_symbols, excluded):
    """
    Generates a single password using secrets.choice for secure randomness.

    Security Rule: Guarantees at least one character from each selected
    type appears in the final password. This ensures the password actually
    meets the selected criteria — not just "maybe" includes them.
    """

    guaranteed_chars = []

    # Pick one guaranteed character from each selected set
    # (after filtering out excluded chars from that set too)
    if use_lower:
        sub = [c for c in LOWERCASE if c not in excluded]
        if sub:
            guaranteed_chars.append(secrets.choice(sub))

    if use_upper:
        sub = [c for c in UPPERCASE if c not in excluded]
        if sub:
            guaranteed_chars.append(secrets.choice(sub))

    if use_digits:
        sub = [c for c in DIGITS if c not in excluded]
        if sub:
            guaranteed_chars.append(secrets.choice(sub))

    if use_symbols:
        sub = [c for c in SYMBOLS if c not in excluded]
        if sub:
            guaranteed_chars.append(secrets.choice(sub))

    # Fill the remaining length with random chars from the full pool
    remaining = length - len(guaranteed_chars)
    if remaining < 0:
        remaining = 0

    filler = [secrets.choice(pool) for _ in range(remaining)]

    # Combine and shuffle — so guaranteed chars don't always appear first
    all_chars = guaranteed_chars + filler
    random.shuffle(all_chars)

    return "".join(all_chars)


# ---------------------------------------------------------------
# Feature: Copy to clipboard
# ---------------------------------------------------------------
def copy_to_clipboard(password):
    """Copies the given password to the system clipboard."""
    if not CLIPBOARD_AVAILABLE:
        print("\n  [!] pyperclip is not installed.")
        print("      Run this to enable clipboard support:")
        print("      pip install pyperclip\n")
        return

    try:
        pyperclip.copy(password)
        print("  [OK] Password copied to clipboard!")
    except Exception as e:
        print(f"  [!] Clipboard copy failed: {e}")


# ---------------------------------------------------------------
# Feature: Save passwords to file
# ---------------------------------------------------------------
def save_passwords(passwords):
    """
    Appends the generated passwords to a local text file
    so users can keep a record (useful for reference later).
    """
    filename = "my_passwords.txt"
    try:
        with open(filename, "a") as f:
            f.write("\n--- New Batch ---\n")
            for i, pwd in enumerate(passwords, start=1):
                f.write(f"  Password {i}: {pwd}\n")
        print(f"  [OK] Passwords saved to '{filename}'")
    except Exception as e:
        print(f"  [!] Could not save to file: {e}")


# ---------------------------------------------------------------
# Main program flow
# ---------------------------------------------------------------
def main():
    # Clear screen for a clean look (works on both Windows and Linux/Mac)
    os.system("cls" if os.name == "nt" else "clear")

    show_banner()

    # ---- STEP 1: Password Length ----
    print("[ STEP 1 ]  Set Password Length")
    print("  Tip: 12+ characters is recommended for security.\n")
    length = ask_int("Enter password length (4 to 128): ", 4, 128)

    # ---- STEP 2: Character Set Selection ----
    print("\n[ STEP 2 ]  Choose Character Types\n")
    use_lower   = ask_yes_no("Include lowercase letters?  (a-z)")
    use_upper   = ask_yes_no("Include uppercase letters?  (A-Z)")
    use_digits  = ask_yes_no("Include numbers?            (0-9)")
    use_symbols = ask_yes_no("Include symbols?            (!@#$...)")

    # Must select at least one type — fallback to all if none chosen
    if not any([use_lower, use_upper, use_digits, use_symbols]):
        print("\n  [!] No character type selected — enabling all by default.\n")
        use_lower = use_upper = use_digits = use_symbols = True

    # ---- STEP 3: Exclude Characters (Customization) ----
    print("\n[ STEP 3 ]  Exclude Specific Characters  (optional)\n")
    print("  Example: type  0Oo1lI  to avoid visually confusing characters.")
    exclude_input = input("  Characters to exclude (or press Enter to skip): ").strip()
    excluded = set(exclude_input)  # set for O(1) lookup

    if excluded:
        print(f"  Excluding: {' '.join(sorted(excluded))}")

    # ---- STEP 4: Number of Passwords ----
    print("\n[ STEP 4 ]  How Many Passwords?\n")
    count = ask_int("How many passwords to generate? (1 to 20): ", 1, 20)

    # ---- Build character pool ----
    pool = build_pool(use_lower, use_upper, use_digits, use_symbols, excluded)

    if len(pool) == 0:
        print("\n  [!!] No characters left after exclusions!")
        print("       Please try again with fewer exclusions.\n")
        sys.exit(1)

    if len(pool) < 5:
        print(f"\n  [!] Warning: Only {len(pool)} characters in pool. Passwords may be weak.\n")

    # ---- Show strength info ----
    strength = check_strength(length, use_lower, use_upper, use_digits, use_symbols)
    print(f"\n  Strength  : {strength}")
    print(f"  Pool size : {len(pool)} unique characters available\n")

    # ---- Generate passwords ----
    print("=" * 56)
    print("  GENERATED PASSWORDS")
    print("=" * 56)

    passwords = []
    for i in range(count):
        pwd = generate_password(
            length, pool,
            use_lower, use_upper, use_digits, use_symbols,
            excluded
        )
        passwords.append(pwd)
        print(f"  [{i + 1:>2}]  {pwd}")

    print("=" * 56)

    # ---- Clipboard option ----
    print("\n[ OPTIONS ]\n")
    if passwords:
        if ask_yes_no("Copy the first password to clipboard?"):
            copy_to_clipboard(passwords[0])

    # ---- Save to file option ----
    if passwords:
        if ask_yes_no("Save all passwords to a text file?"):
            save_passwords(passwords)

    # ---- Generate again? ----
    print()
    if ask_yes_no("Generate another set of passwords?"):
        main()
    else:
        print("\n  Thanks for using the Password Generator!")
        print("  — Created by VISHNU S\n")


# ---------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()