"""
Assignment 2 Q1
Group Name: [Group No. 11]
Group Members:
[Bidhan Chaudhary] - [S394807]
[Dipesh Sedhai] - [S395457]
[Nitesh Raj Chaudhary] - [S394811]
[Shova Bhujel] - [S396449]

"""
import os

# --- Helper functions for character shifting ---
def get_shifted_char(char, shift, direction='forward'):
    """
    Shifts a character within its alphabetical range.
    Handles both forward and backward shifts.
    """
    if 'a' <= char <= 'm':
        base = ord('a')
        alphabet_size = 13
    elif 'n' <= char <= 'z':
        base = ord('n')
        alphabet_size = 13
    elif 'A' <= char <= 'M':
        base = ord('A')
        alphabet_size = 13
    elif 'N' <= char <= 'Z':
        base = ord('N')
        alphabet_size = 13
    else:
        # Return non-alphabetic characters unchanged
        return char

    # Convert character to a 0-25 index
    char_index = ord(char) - base

    if direction == 'forward':
        new_index = (char_index + shift) % alphabet_size
    elif direction == 'backward':
        new_index = (char_index - shift + alphabet_size) % alphabet_size
    else:
        return char

    return chr(new_index + base)

# --- Core Encryption/Decryption Logic ---
def encrypt_char(char, shift1, shift2):
    """Encrypts a single character based on the defined rules."""
    char_ord = ord(char)

    # Lowercase letters
    if 'a' <= char <= 'z':
        if 'a' <= char <= 'm':  # First half
            shift = shift1 * shift2
            return get_shifted_char(char, shift, 'forward')
        else:  # Second half
            shift = shift1 + shift2
            return get_shifted_char(char, shift, 'backward')
    
    # Uppercase letters
    elif 'A' <= char <= 'Z':
        if 'A' <= char <= 'M':  # First half
            shift = shift1
            return get_shifted_char(char, shift, 'backward')
        else:  # Second half
            shift = shift2 ** 2
            return get_shifted_char(char, shift, 'forward')
    
    # Other characters remain unchanged
    else:
        return char

def decrypt_char(char, shift1, shift2):
    """Decrypts a single character by reversing the encryption logic."""
    char_ord = ord(char)

    # Lowercase letters
    if 'a' <= char <= 'z':
        if 'a' <= char <= 'm':  # First half
            shift = shift1 * shift2
            return get_shifted_char(char, shift, 'backward')
        else:  # Second half
            shift = shift1 + shift2
            return get_shifted_char(char, shift, 'forward')
    
    # Uppercase letters
    elif 'A' <= char <= 'Z':
        if 'A' <= char <= 'M':  # First half
            shift = shift1
            return get_shifted_char(char, shift, 'forward')
        else:  # Second half
            shift = shift2 ** 2
            return get_shifted_char(char, shift, 'backward')
    
    # Other characters remain unchanged
    else:
        return char

# --- Main Functions to Implement ---
def encrypt_file(input_file, output_file, shift1, shift2):
    """
    Reads from the input file, encrypts the content, and writes to the output file.
    """
    print(f"\nEncrypting '{input_file}'...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        encrypted_text = "".join([encrypt_char(char, shift1, shift2) for char in raw_text])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
            
        print(f"Encryption successful. Encrypted content saved to '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")

def decrypt_file(input_file, output_file, shift1, shift2):
    """
    Reads from the input file, decrypts the content, and writes to the output file.
    """
    print(f"\nDecrypting '{input_file}'...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_text = f.read()
            
        decrypted_text = "".join([decrypt_char(char, shift1, shift2) for char in encrypted_text])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
            
        print(f"Decryption successful. Decrypted content saved to '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")

def verify_files(file1, file2):
    """
    Compares the contents of two files and prints a verification result.
    """
    print(f"\nVerifying '{file1}' against '{file2}'...")
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            content1 = f1.read()
        
        with open(file2, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
            
        if content1 == content2:
            print("Verification Successful: The decrypted file matches the original.")
            return True
        else:
            print("Verification Failed: The decrypted file does not match the original.")
            return False
    except FileNotFoundError:
        print("Error: One or both verification files were not found.")
        return False

# --- Program Execution ---
if __name__ == "__main__":
    RAW_FILE = "raw_text.txt"
    ENCRYPTED_FILE = "encrypted_text.txt"
    DECRYPTED_FILE = "decrypted_text.txt"
    
    try:
            shift1 = int(input("Enter the first shift value (shift1): "))
            shift2 = int(input("Enter the second shift value (shift2): "))
    except ValueError:
            print("Invalid input. Please enter integer values.")
            exit()
            
        # 2. Encrypt the file
    encrypt_file(RAW_FILE, ENCRYPTED_FILE, shift1, shift2)
        
        # 3. Decrypt the file
    decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, shift1, shift2)
        
        # 4. Verify the decryption
    verify_files(RAW_FILE, DECRYPTED_FILE)
    # try:
    #     # 1. Prompt the user for shift values
    #     try:
    #         shift1 = int(input("Enter the first shift value (shift1): "))
    #         shift2 = int(input("Enter the second shift value (shift2): "))
    #     except ValueError:
    #         print("Invalid input. Please enter integer values.")
    #         exit()
            
    #     # 2. Encrypt the file
    #     encrypt_file(RAW_FILE, ENCRYPTED_FILE, shift1, shift2)
        
    #     # 3. Decrypt the file
    #     decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, shift1, shift2)
        
    #     # 4. Verify the decryption
    #     verify_files(RAW_FILE, DECRYPTED_FILE)
        
    # finally:
    #     # Clean up created files
    #     for filename in [ENCRYPTED_FILE, DECRYPTED_FILE]:
    #         if os.path.exists(filename):
    #             os.remove(filename)
    #             print(f"Cleaned up '{filename}'.")
