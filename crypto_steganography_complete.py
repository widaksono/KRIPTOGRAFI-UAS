#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Complete Cryptography and Steganography System
3 Main Options:
1. Caesar Cipher Only (Encrypt/Decrypt)
2. LSB Steganography Only (Embed/Extract)
3. Combined (Caesar + LSB Steganography)
"""

from PIL import Image
import os

# ==================== CAESAR CIPHER FUNCTIONS ====================

def caesar_encrypt(plaintext, shift=7):
    """Manual Caesar Cipher encryption"""
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                encrypted += chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                encrypted += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(ciphertext, shift=7):
    """Manual Caesar Cipher decryption"""
    decrypted = ""
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                decrypted += chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                decrypted += chr((ord(char) - 97 - shift) % 26 + 97)
        else:
            decrypted += char
    return decrypted

# ==================== LSB STEGANOGRAPHY FUNCTIONS ====================

def text_to_binary(text):
    """Convert text to binary string"""
    binary = ""
    for char in text:
        binary += format(ord(char), '08b')
    return binary

def binary_to_text(binary):
    """Convert binary string to text"""
    text = ""
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):
            byte = binary[i:i+8]
            text += chr(int(byte, 2))
    return text

def embed_text_in_image(image_path, secret_text, output_path):
    """Embed text into image using LSB steganography"""
    try:
        # Open image
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        
        # Check minimum size
        if width < 128 or height < 128:
            raise ValueError("Image must be at least 128x128 pixels")
        
        # Convert text to binary
        binary_data = text_to_binary(secret_text)
        data_length = len(binary_data)
        
        # Add 32-bit header for data length
        length_header = format(data_length, '032b')
        full_data = length_header + binary_data
        
        # Check capacity
        max_capacity = width * height * 3
        if len(full_data) > max_capacity:
            raise ValueError(f"Text too large! Max: {max_capacity} bits, Need: {len(full_data)} bits")
        
        # Get pixels
        pixels = list(img.getdata())
        new_pixels = []
        
        bit_index = 0
        
        for pixel in pixels:
            r, g, b = pixel
            
            # Embed in LSB of R
            if bit_index < len(full_data):
                r = (r & 0xFE) | int(full_data[bit_index])
                bit_index += 1
            
            # Embed in LSB of G
            if bit_index < len(full_data):
                g = (g & 0xFE) | int(full_data[bit_index])
                bit_index += 1
            
            # Embed in LSB of B
            if bit_index < len(full_data):
                b = (b & 0xFE) | int(full_data[bit_index])
                bit_index += 1
            
            new_pixels.append((r, g, b))
        
        # Save new image
        new_img = Image.new('RGB', (width, height))
        new_img.putdata(new_pixels)
        new_img.save(output_path)
        
        print(f"✓ Text embedded successfully in {output_path}")
        print(f"✓ Used {len(full_data)} bits out of {max_capacity} available")
        return True
        
    except Exception as e:
        print(f"✗ Error embedding text: {e}")
        return False

def extract_text_from_image(image_path):
    """Extract text from steganographic image"""
    try:
        # Open image
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        
        # Extract LSB from all pixels
        binary_data = ""
        for pixel in pixels:
            r, g, b = pixel
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
        
        # Get data length from first 32 bits
        if len(binary_data) < 32:
            raise ValueError("Invalid steganographic image")
        
        length_header = binary_data[:32]
        data_length = int(length_header, 2)
        
        # Extract actual data
        if len(binary_data) < 32 + data_length:
            raise ValueError("Incomplete data in image")
        
        text_binary = binary_data[32:32 + data_length]
        extracted_text = binary_to_text(text_binary)
        
        return extracted_text
        
    except Exception as e:
        print(f"✗ Error extracting text: {e}")
        return None

# ==================== MENU FUNCTIONS ====================

def caesar_cipher_menu():
    """Menu for Caesar Cipher operations only"""
    print("\n" + "="*50)
    print("CAESAR CIPHER (SHIFT 7)")
    print("="*50)
    
    while True:
        print("\nCaesar Cipher Options:")
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Back to main menu")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            print("\n--- ENCRYPT TEXT ---")
            plaintext = input("Enter text to encrypt: ")
            if plaintext:
                encrypted = caesar_encrypt(plaintext, 7)
                print(f"Original text: {plaintext}")
                print(f"Encrypted text: {encrypted}")
            else:
                print("✗ Text cannot be empty!")
        
        elif choice == '2':
            print("\n--- DECRYPT TEXT ---")
            ciphertext = input("Enter text to decrypt: ")
            if ciphertext:
                decrypted = caesar_decrypt(ciphertext, 7)
                print(f"Encrypted text: {ciphertext}")
                print(f"Decrypted text: {decrypted}")
            else:
                print("✗ Text cannot be empty!")
        
        elif choice == '3':
            break
        
        else:
            print("✗ Invalid choice!")

def steganography_menu():
    """Menu for LSB Steganography operations only"""
    print("\n" + "="*50)
    print("LSB STEGANOGRAPHY")
    print("="*50)
    
    while True:
        print("\nSteganography Options:")
        print("1. Embed text in image")
        print("2. Extract text from image")      
        print("3. Back to main menu")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            print("\n--- EMBED TEXT IN IMAGE ---")
            text = input("Enter text to embed: ")
            if not text:
                print("✗ Text cannot be empty!")
                continue
            
            image_path = input("Enter image path (.bmp/.jpg): ").strip()
            if not os.path.exists(image_path):
                print("✗ Image file not found!")
                continue
            
            output_path = input("Enter output path (default: stego.bmp): ").strip()
            if not output_path:
                output_path = "stego.bmp"
            
            embed_text_in_image(image_path, text, output_path)
        
        elif choice == '2':
            print("\n--- EXTRACT TEXT FROM IMAGE ---")
            image_path = input("Enter steganographic image path: ").strip()
            if not os.path.exists(image_path):
                print("✗ Image file not found!")
                continue
            
            extracted = extract_text_from_image(image_path)
            if extracted:
                print(f"✓ Extracted text: {extracted}")
                      
        elif choice == '3':
            break
        
        else:
            print("✗ Invalid choice!")

def combined_menu():
    """Menu for combined Caesar Cipher + LSB Steganography"""
    print("\n" + "="*50)
    print("COMBINED: CAESAR CIPHER + LSB STEGANOGRAPHY")
    print("="*50)
    
    while True:
        print("\nCombined Options:")
        print("1. Encrypt text + Embed in image")
        print("2. Extract from image + Decrypt text")     
        print("3. Back to main menu")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            print("\n--- ENCRYPT + EMBED ---")
            
            # Get plaintext
            plaintext = input("Enter secret message: ")
            if not plaintext:
                print("✗ Message cannot be empty!")
                continue
            
            # Get image path
            image_path = input("Enter carrier image path (.bmp/.jpg): ").strip()
            if not os.path.exists(image_path):
                print("✗ Image file not found!")
                continue
            
            # Get output path
            output_path = input("Enter output path (default: combined_stego.bmp): ").strip()
            if not output_path:
                output_path = "combined_stego.bmp"
            
            # Step 1: Encrypt with Caesar Cipher
            print(f"\nStep 1: Encrypting with Caesar Cipher (shift 7)...")
            encrypted_text = caesar_encrypt(plaintext, 7)
            print(f"✓ Original: {plaintext}")
            print(f"✓ Encrypted: {encrypted_text}")
            
            # Step 2: Embed encrypted text in image
            print(f"\nStep 2: Embedding encrypted text in image...")
            if embed_text_in_image(image_path, encrypted_text, output_path):
                print("✓ Combined process completed successfully!")
        
        elif choice == '2':
            print("\n--- EXTRACT + DECRYPT ---")
            
            # Get steganographic image path
            image_path = input("Enter steganographic image path: ").strip()
            if not os.path.exists(image_path):
                print("✗ Image file not found!")
                continue
            
            # Step 1: Extract encrypted text from image
            print(f"\nStep 1: Extracting text from image...")
            extracted_encrypted = extract_text_from_image(image_path)
            
            if extracted_encrypted:
                print(f"✓ Extracted (encrypted): {extracted_encrypted}")
                
                # Step 2: Decrypt with Caesar Cipher
                print(f"\nStep 2: Decrypting with Caesar Cipher (shift 7)...")
                decrypted_text = caesar_decrypt(extracted_encrypted, 7)
                print(f"✓ Final decrypted message: {decrypted_text}")
            else:
                print("✗ Failed to extract text from image!")
        
               
        elif choice == '3':
            break
        
        else:
            print("✗ Invalid choice!")

def main_menu():
    """Main program menu"""
    print("="*60)
    print("CRYPTOGRAPHY & STEGANOGRAPHY SYSTEM")
    print("="*60)
    print("Manual implementation without encryption/decryption libraries")
    print("Supports .bmp and .jpg images (minimum 128x128 RGB)")
    print("="*60)
    
    while True:
        print("\nMain Menu:")
        print("1. Caesar Cipher Only (Encrypt/Decrypt)")
        print("2. LSB Steganography Only (Embed/Extract)")
        print("3. Combined (Caesar + Steganography)")
        print("4. Exit")
        print("-" * 40)
        
        try:
            choice = input("Choose main option (1-4): ").strip()
            
            if choice == '1':
                caesar_cipher_menu()
            
            elif choice == '2':
                steganography_menu()
            
            elif choice == '3':
                combined_menu()
            
            elif choice == '4':
                print("\nThank you for using the program!")
                break
            
            else:
                print("✗ Invalid choice! Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    main_menu()