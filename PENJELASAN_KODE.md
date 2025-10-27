# 💻 PENJELASAN KODE - Detail Implementasi

## 🎯 Struktur Kode Keseluruhan

```python
crypto_steganography_complete.py
├── Import Libraries
├── Caesar Cipher Functions (Baris 12-35)
├── LSB Steganography Functions (Baris 37-150)
├── Utility Functions (Baris 152-175)
├── Menu Functions (Baris 177-350)
└── Main Program (Baris 352-380)
```

---

## 📖 BAGIAN 1: IMPORT DAN SETUP

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os
```

**Penjelasan:**
- `#!/usr/bin/env python3`: Shebang untuk eksekusi di Unix/Linux
- `# -*- coding: utf-8 -*-`: Encoding UTF-8 untuk karakter khusus
- `PIL (Pillow)`: Library untuk manipulasi gambar
- `os`: Library untuk operasi file system

---

## 📖 BAGIAN 2: CAESAR CIPHER - DETAIL KODE

### 🔐 Fungsi Enkripsi

```python
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
```

**Analisis Baris per Baris:**

1. **Baris 1:** Definisi fungsi dengan parameter default shift=7
2. **Baris 2:** Docstring untuk dokumentasi
3. **Baris 3:** Inisialisasi string hasil enkripsi
4. **Baris 4:** Loop untuk setiap karakter dalam teks
5. **Baris 5:** Cek apakah karakter adalah huruf
6. **Baris 6-7:** Proses huruf besar (A-Z)
   - `ord(char) - 65`: Konversi A=0, B=1, ..., Z=25
   - `+ shift`: Tambah pergeseran
   - `% 26`: Modulo untuk wrapping (Z kembali ke A)
   - `+ 65`: Konversi kembali ke ASCII
   - `chr()`: Konversi ASCII ke karakter
8. **Baris 8-9:** Proses huruf kecil (a-z) dengan logika sama
9. **Baris 10-11:** Karakter non-huruf tidak diubah
10. **Baris 12:** Return hasil enkripsi

**Contoh Trace Eksekusi:**
```python
Input: "Hello"
char='H': ord('H')=72 → (72-65+7)%26+65 = 14+65 = 79 → chr(79)='O'
char='e': ord('e')=101 → (101-97+7)%26+97 = 11+97 = 108 → chr(108)='l'
char='l': ord('l')=108 → (108-97+7)%26+97 = 18+97 = 115 → chr(115)='s'
char='l': → 's'
char='o': ord('o')=111 → (111-97+7)%26+97 = 21+97 = 118 → chr(118)='v'
Output: "Olssv"
```

### 🔓 Fungsi Dekripsi

```python
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
```

**Perbedaan dengan Enkripsi:**
- Menggunakan `- shift` instead of `+ shift`
- Logika sebaliknya untuk membalik proses enkripsi

---

## 📖 BAGIAN 3: STEGANOGRAFI - DETAIL KODE

### 🔄 Konversi Teks ke Binary

```python
def text_to_binary(text):
    """Convert text to binary string"""
    binary = ""
    for char in text:
        binary += format(ord(char), '08b')
    return binary
```

**Penjelasan Detail:**
- `ord(char)`: Konversi karakter ke nilai ASCII
- `format(value, '08b')`: Format ke binary 8-bit dengan leading zeros
- Contoh: 'A' → 65 → '01000001'

**Trace Eksekusi:**
```python
Input: "Hi"
char='H': ord('H')=72 → format(72, '08b') = '01001000'
char='i': ord('i')=105 → format(105, '08b') = '01101001'
Output: "0100100001101001"
```

### 🔄 Konversi Binary ke Teks

```python
def binary_to_text(binary):
    """Convert binary string to text"""
    text = ""
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):
            byte = binary[i:i+8]
            text += chr(int(byte, 2))
    return text
```

**Penjelasan Detail:**
- `range(0, len(binary), 8)`: Loop dengan step 8 (1 byte)
- `binary[i:i+8]`: Slice 8 bit
- `int(byte, 2)`: Konversi binary string ke integer
- `chr()`: Konversi integer ke karakter

### 🖼️ Embedding Function - Analisis Mendalam

```python
def embed_text_in_image(image_path, secret_text, output_path):
    try:
        # 1. LOAD DAN VALIDASI GAMBAR
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        
        # 2. VALIDASI UKURAN MINIMUM
        if width < 128 or height < 128:
            raise ValueError("Image must be at least 128x128 pixels")
        
        # 3. KONVERSI TEKS KE BINARY
        binary_data = text_to_binary(secret_text)
        data_length = len(binary_data)
        
        # 4. BUAT HEADER 32-BIT
        length_header = format(data_length, '032b')
        full_data = length_header + binary_data
        
        # 5. CEK KAPASITAS
        max_capacity = width * height * 3
        if len(full_data) > max_capacity:
            raise ValueError(f"Text too large! Max: {max_capacity} bits, Need: {len(full_data)} bits")
        
        # 6. PROSES EMBEDDING
        pixels = list(img.getdata())
        new_pixels = []
        bit_index = 0
        
        for pixel in pixels:
            r, g, b = pixel
            
            # Embed in LSB of Red
            if bit_index < len(full_data):
                r = (r & 0xFE) | int(full_data[bit_index])
                bit_index += 1
            
            # Embed in LSB of Green
            if bit_index < len(full_data):
                g = (g & 0xFE) | int(full_data[bit_index])
                bit_index += 1
            
            # Embed in LSB of Blue
            if bit_index < len(full_data):
                b = (b & 0xFE) | int(full_data[bit_index])
                bit_index += 1
            
            new_pixels.append((r, g, b))
        
        # 7. SIMPAN GAMBAR BARU
        new_img = Image.new('RGB', (width, height))
        new_img.putdata(new_pixels)
        new_img.save(output_path)
        
        return True
        
    except Exception as e:
        print(f"✗ Error embedding text: {e}")
        return False
```

**Analisis Bagian Kritis:**

#### A. Operasi Bitwise untuk LSB
```python
r = (r & 0xFE) | int(full_data[bit_index])
```

**Penjelasan:**
- `0xFE = 11111110` (binary)
- `r & 0xFE`: Nol-kan LSB, pertahankan 7 bit lainnya
- `| int(bit)`: Set LSB dengan bit data (OR operation)

**Contoh:**
```
Original r = 150 = 10010110
r & 0xFE     = 10010110 & 11111110 = 10010110 (LSB=0)
bit = '1'
Result = 10010110 | 00000001 = 10010111 = 151
```

#### B. Header 32-bit
```python
length_header = format(data_length, '032b')
```

**Tujuan:** Menyimpan panjang data untuk ekstraksi yang akurat
**Format:** 32-bit binary dengan leading zeros
**Contoh:** 
- Data length = 16 bits
- Header = "00000000000000000000000000010000"

### 🔍 Extraction Function - Analisis Mendalam

```python
def extract_text_from_image(image_path):
    try:
        # 1. LOAD GAMBAR
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        
        # 2. EKSTRAK LSB DARI SEMUA PIXEL
        binary_data = ""
        for pixel in pixels:
            r, g, b = pixel
            binary_data += str(r & 1)  # LSB dari Red
            binary_data += str(g & 1)  # LSB dari Green
            binary_data += str(b & 1)  # LSB dari Blue
        
        # 3. BACA HEADER 32-BIT
        if len(binary_data) < 32:
            raise ValueError("Invalid steganographic image")
        
        length_header = binary_data[:32]
        data_length = int(length_header, 2)
        
        # 4. EKSTRAK DATA SEBENARNYA
        if len(binary_data) < 32 + data_length:
            raise ValueError("Incomplete data in image")
        
        text_binary = binary_data[32:32 + data_length]
        extracted_text = binary_to_text(text_binary)
        
        return extracted_text
        
    except Exception as e:
        print(f"✗ Error extracting text: {e}")
        return None
```

**Analisis Bagian Kritis:**

#### A. Ekstraksi LSB
```python
binary_data += str(r & 1)
```

**Penjelasan:**
- `r & 1`: Ambil hanya LSB (AND dengan 00000001)
- `str()`: Konversi ke string '0' atau '1'

**Contoh:**
```
r = 151 = 10010111
r & 1 = 10010111 & 00000001 = 00000001 = 1
Result: '1'
```

#### B. Parsing Header
```python
length_header = binary_data[:32]
data_length = int(length_header, 2)
```

**Proses:**
1. Ambil 32 bit pertama sebagai header
2. Konversi binary string ke integer
3. Gunakan sebagai panjang data yang akan diekstrak

---
**Algoritma Gradient:**
- **Red:** Gradient horizontal (0→255)
- **Green:** Gradient vertikal (0→255)
- **Blue:** Gradient diagonal (kombinasi x+y)

**Formula:**
```
R = (x / width) * 255
G = (y / height) * 255  
B = ((x + y) / (width + height)) * 255
```

---

## 📖 BAGIAN 4: MENU SYSTEM

### 🖥️ Struktur Menu

```python
def main_menu():
    while True:
        # Display menu options
        choice = input("Choose main option (1-4): ").strip()
        
        if choice == '1':
            caesar_cipher_menu()
        elif choice == '2':
            steganography_menu()
        elif choice == '3':
            combined_menu()
        elif choice == '4':
            break
        else:
            print("✗ Invalid choice!")
```

**Design Pattern:** State Machine
- Setiap menu adalah state
- User input menentukan transisi state
- Loop hingga user memilih exit

### 🔄 Combined Menu Logic

```python
def combined_menu():
    # Mode 1: Encrypt + Embed
    if choice == '1':
        # Step 1: Caesar Cipher
        encrypted_text = caesar_encrypt(plaintext, 7)
        
        # Step 2: LSB Steganography
        embed_text_in_image(image_path, encrypted_text, output_path)
    
    # Mode 2: Extract + Decrypt
    elif choice == '2':
        # Step 1: LSB Extraction
        extracted_encrypted = extract_text_from_image(image_path)
        
        # Step 2: Caesar Decryption
        decrypted_text = caesar_decrypt(extracted_encrypted, 7)
```

**Pipeline Processing:**
1. **Encoding:** Plaintext → Caesar → LSB → Stego Image
2. **Decoding:** Stego Image → LSB → Caesar → Plaintext

---

## 📖 BAGIAN 5: ERROR HANDLING STRATEGY

### ⚠️ Exception Hierarchy

```python
try:
    # Main operation
except ValueError as e:
    # Input validation errors
except IOError as e:
    # File I/O errors
except Exception as e:
    # Catch-all for unexpected errors
```

**Error Types:**
1. **ValueError:** Invalid input (ukuran gambar, teks kosong)
2. **IOError:** File tidak ditemukan, permission denied
3. **Exception:** Unexpected errors (memory, corruption)

### 🔍 Validation Checks

```python
# Size validation
if width < 128 or height < 128:
    raise ValueError("Image must be at least 128x128 pixels")

# Capacity validation
if len(full_data) > max_capacity:
    raise ValueError(f"Text too large! Max: {max_capacity} bits")

# File existence
if not os.path.exists(image_path):
    print("✗ Image file not found!")
```

---