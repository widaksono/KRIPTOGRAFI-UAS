# 📚 DOKUMENTASI TEKNIS - Crypto Steganography System

## 🎯 Gambaran Umum

Sistem ini mengimplementasikan dua teknik keamanan informasi:
1. **Caesar Cipher** - Kriptografi klasik dengan pergeseran karakter
2. **LSB Steganography** - Menyembunyikan data dalam gambar digital

## 🏗️ Arsitektur Sistem

```
crypto_steganography_complete.py
├── Caesar Cipher Functions
├── LSB Steganography Functions  
├── Utility Functions
├── Menu Functions
└── Main Program
```

---

## 📖 BAGIAN 1: CAESAR CIPHER

### 🔐 Konsep Dasar

Caesar Cipher adalah teknik enkripsi substitusi sederhana yang menggeser setiap huruf dalam alfabet dengan jumlah posisi tetap.

**Rumus Matematika:**
- **Enkripsi:** `E(x) = (x + k) mod 26`
- **Dekripsi:** `D(x) = (x - k) mod 26`

Dimana:
- `x` = posisi huruf dalam alfabet (A=0, B=1, ..., Z=25)
- `k` = kunci pergeseran (dalam sistem ini k=7)

### 🔧 Implementasi Teknis

#### Fungsi Enkripsi
```python
def caesar_encrypt(plaintext, shift=7):
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

**Penjelasan Langkah demi Langkah:**

1. **Input Validation:** Cek apakah karakter adalah huruf (`char.isalpha()`)
2. **Case Handling:** Pisahkan huruf besar dan kecil
3. **ASCII Conversion:** 
   - Huruf besar: A=65, B=66, ..., Z=90
   - Huruf kecil: a=97, b=98, ..., z=122
4. **Shift Calculation:**
   - `ord(char) - 65`: Konversi ke posisi 0-25
   - `+ shift`: Tambah pergeseran
   - `% 26`: Modulo untuk wrapping (Z→A)
   - `+ 65`: Konversi kembali ke ASCII
5. **Non-alphabetic:** Karakter selain huruf tidak diubah

#### Contoh Proses:
```
Input: "Hello"
H (72) → (72-65+7)%26+65 = (7+7)%26+65 = 14+65 = 79 → O
e (101) → (101-97+7)%26+97 = (4+7)%26+97 = 11+97 = 108 → l
l (108) → (108-97+7)%26+97 = (11+7)%26+97 = 18+97 = 115 → s
l (108) → s
o (111) → (111-97+7)%26+97 = (14+7)%26+97 = 21+97 = 118 → v

Output: "Olssv"
```

---

## 📖 BAGIAN 2: LSB STEGANOGRAPHY

### 🖼️ Konsep Dasar

LSB (Least Significant Bit) Steganography menyembunyikan data dengan memodifikasi bit terakhir (paling tidak signifikan) dari setiap komponen warna pixel.

**Struktur Pixel RGB:**
```
Pixel = (Red, Green, Blue)
Red   = 8 bit = XXXXXXX? (? = LSB yang dimodifikasi)
Green = 8 bit = XXXXXXX?
Blue  = 8 bit = XXXXXXX?
```

### 🔧 Implementasi Teknis

#### 1. Konversi Teks ke Binary
```python
def text_to_binary(text):
    binary = ""
    for char in text:
        binary += format(ord(char), '08b')
    return binary
```

**Contoh:**
```
Input: "Hi"
H = ASCII 72 = 01001000 (8 bit)
i = ASCII 105 = 01101001 (8 bit)
Output: "0100100001101001" (16 bit)
```

#### 2. Embedding Process

```python
def embed_text_in_image(image_path, secret_text, output_path):
    # 1. Load dan validasi gambar
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 2. Konversi teks ke binary
    binary_data = text_to_binary(secret_text)
    data_length = len(binary_data)
    
    # 3. Tambah header 32-bit untuk panjang data
    length_header = format(data_length, '032b')
    full_data = length_header + binary_data
    
    # 4. Cek kapasitas
    max_capacity = width * height * 3  # 3 bit per pixel (R,G,B)
    
    # 5. Embed bit ke LSB setiap komponen warna
    for pixel in pixels:
        r, g, b = pixel
        
        # Embed di LSB Red
        if bit_index < len(full_data):
            r = (r & 0xFE) | int(full_data[bit_index])
            
        # Embed di LSB Green  
        if bit_index < len(full_data):
            g = (g & 0xFE) | int(full_data[bit_index])
            
        # Embed di LSB Blue
        if bit_index < len(full_data):
            b = (b & 0xFE) | int(full_data[bit_index])
```

**Penjelasan Operasi Bitwise:**
- `r & 0xFE`: Nol-kan LSB (0xFE = 11111110)
- `| int(bit)`: Set LSB dengan bit data
- Contoh: r=150 (10010110) → (10010110 & 11111110) | 1 = 10010111 = 151

#### 3. Extraction Process

```python
def extract_text_from_image(image_path):
    # 1. Load gambar
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    # 2. Ekstrak LSB dari semua pixel
    binary_data = ""
    for pixel in pixels:
        r, g, b = pixel
        binary_data += str(r & 1)  # Ambil LSB
        binary_data += str(g & 1)
        binary_data += str(b & 1)
    
    # 3. Baca header 32-bit untuk panjang data
    length_header = binary_data[:32]
    data_length = int(length_header, 2)
    
    # 4. Ekstrak data sebenarnya
    text_binary = binary_data[32:32 + data_length]
    extracted_text = binary_to_text(text_binary)
```

### 📊 Kapasitas Steganografi

**Rumus Kapasitas:**
```
Kapasitas (bit) = Width × Height × 3
Kapasitas (karakter) = (Width × Height × 3) ÷ 8
```

**Contoh:**
- Gambar 128×128: 49,152 bit = 6,144 karakter
- Gambar 256×256: 196,608 bit = 24,576 karakter

---

## 📖 BAGIAN 3: COMBINED MODE

### 🔄 Alur Proses

#### Encoding (Encrypt + Embed):
```
Plaintext → Caesar Cipher → Ciphertext → LSB Embed → Stego Image
```

#### Decoding (Extract + Decrypt):
```
Stego Image → LSB Extract → Ciphertext → Caesar Cipher → Plaintext
```

### 🛡️ Keamanan Berlapis

1. **Layer 1 - Caesar Cipher:** Mengacak teks asli
2. **Layer 2 - LSB Steganography:** Menyembunyikan teks teracak
3. **Layer 3 - Visual Camouflage:** Gambar terlihat normal

---

## 📖 BAGIAN 4: STRUKTUR DATA

### 🗂️ Format Data dalam Gambar

```
Bit Layout dalam Gambar:
[32-bit Header][Data Binary]
│              │
│              └─ Teks rahasia dalam format binary
└─ Panjang data dalam 32-bit binary
```

**Contoh Header:**
```
Teks "Hi" = 16 bit
Header = format(16, '032b') = "00000000000000000000000000010000"
```

### 🎨 Pixel Modification

**Sebelum Embedding:**
```
Pixel (150, 200, 75) = (10010110, 11001000, 01001011)
```

**Setelah Embedding bit "101":**
```
R: 10010110 → 10010111 (LSB: 0→1)
G: 11001000 → 11001000 (LSB: 0→0) 
B: 01001011 → 01001010 (LSB: 1→0)
Result: (151, 200, 74)
```

**Perubahan Visual:** Minimal, tidak terdeteksi mata manusia

---

## 📖 BAGIAN 5: ERROR HANDLING

### ⚠️ Validasi Input

1. **Gambar:**
   - Format: .bmp, .jpg
   - Ukuran minimum: 128×128 pixel
   - Mode warna: RGB

2. **Teks:**
   - Tidak boleh kosong
   - Panjang sesuai kapasitas gambar

3. **File:**
   - Path harus valid
   - File harus dapat dibaca/ditulis

### 🔍 Error Detection

```python
try:
    # Operasi steganografi
except ValueError as e:
    # Kesalahan validasi
except IOError as e:
    # Kesalahan file I/O
except Exception as e:
    # Kesalahan umum lainnya
```

---

## 📖 BAGIAN 6: OPTIMASI PERFORMA

### ⚡ Efisiensi Algoritma

1. **Time Complexity:**
   - Caesar Cipher: O(n) dimana n = panjang teks
   - LSB Steganography: O(w×h) dimana w×h = jumlah pixel

2. **Space Complexity:**
   - Memory usage: O(w×h×3) untuk menyimpan pixel data

### 💾 Memory Management

- Gambar dimuat sepenuhnya ke memory
- Pixel data disimpan sebagai list tuple
- Binary string dibuat secara incremental

---

## 📖 BAGIAN 7: KEAMANAN SISTEM

### 🔒 Kekuatan Keamanan

1. **Caesar Cipher:**
   - Kekuatan: Sederhana, cepat
   - Kelemahan: Mudah dipecahkan dengan frequency analysis
   - Cocok untuk: Pembelajaran, obfuskasi ringan

2. **LSB Steganography:**
   - Kekuatan: Tidak terdeteksi visual, kapasitas besar
   - Kelemahan: Rentan terhadap statistical analysis
   - Cocok untuk: Menyembunyikan keberadaan data

### 🛡️ Rekomendasi Keamanan

1. Gunakan gambar dengan noise tinggi
2. Kombinasikan dengan enkripsi yang lebih kuat
3. Distribusikan data secara acak (tidak berurutan)
4. Gunakan multiple carrier images

---

## 📖 BAGIAN 8: PENGGUNAAN PRAKTIS

### 🎯 Use Cases

1. **Pendidikan:** Pembelajaran konsep kriptografi dan steganografi
2. **Research:** Eksperimen dengan teknik information hiding
3. **Digital Watermarking:** Menyembunyikan copyright information
4. **Covert Communication:** Komunikasi tersembunyi (dengan enkripsi yang lebih kuat)

### 📋 Best Practices

1. **Pilih Gambar Carrier:**
   - Resolusi tinggi untuk kapasitas besar
   - Banyak detail/noise untuk kamuflase
   - Format lossless (.bmp) untuk akurasi

2. **Manajemen Kunci:**
   - Gunakan shift yang tidak mudah ditebak
   - Pertimbangkan dynamic key generation
   - Implementasikan key distribution yang aman

3. **Testing:**
   - Selalu test dengan berbagai ukuran data
   - Verifikasi integritas data setelah ekstraksi
   - Uji dengan berbagai format gambar

---

## 🎉 Kesimpulan

Sistem Crypto Steganography ini mendemonstrasikan implementasi dasar dari:
- **Classical Cryptography** (Caesar Cipher)
- **Modern Steganography** (LSB technique)
- **Combined Security** (Layered protection)

Meskipun sederhana, sistem ini memberikan fondasi yang solid untuk memahami konsep-konsep keamanan informasi dan dapat dikembangkan lebih lanjut dengan algoritma yang lebih kompleks.