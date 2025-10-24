# 📊 DIAGRAM ALUR - Crypto Steganography System

## 🎯 Alur Utama Program

```
┌─────────────────────────────────────────┐
│           MAIN PROGRAM START            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│              MAIN MENU                  │
│  1. Caesar Cipher Only                  │
│  2. LSB Steganography Only              │
│  3. Combined (Caesar + LSB)             │
│  4. Exit                                │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │Caesar   │ │LSB      │ │Combined │
   │Menu     │ │Menu     │ │Menu     │
   └─────────┘ └─────────┘ └─────────┘
```

---

## 📖 BAGIAN 1: CAESAR CIPHER FLOW

### 🔐 Enkripsi Process

```
┌─────────────────┐
│   INPUT TEXT    │
│   "Hello"       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  FOR EACH CHAR  │
│     H, e, l,    │
│     l, o        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   IS ALPHA?     │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │YES        │NO
    ▼           ▼
┌─────────┐ ┌─────────┐
│IS UPPER?│ │KEEP     │
└────┬────┘ │ORIGINAL │
     │      └─────────┘
┌────┴────┐
│YES   NO │
▼         ▼
┌─────────────────┐ ┌─────────────────┐
│(ord(c)-65+7)%26 │ │(ord(c)-97+7)%26 │
│     +65         │ │     +97         │
└─────────┬───────┘ └─────────┬───────┘
          │                   │
          └─────────┬─────────┘
                    ▼
          ┌─────────────────┐
          │   chr(result)   │
          └─────────┬───────┘
                    │
                    ▼
          ┌─────────────────┐
          │ APPEND TO       │
          │ ENCRYPTED       │
          └─────────┬───────┘
                    │
                    ▼
          ┌─────────────────┐
          │ OUTPUT: "Olssv" │
          └─────────────────┘
```

### 🔓 Dekripsi Process

```
┌─────────────────┐
│ ENCRYPTED TEXT  │
│    "Olssv"      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ SAME PROCESS    │
│ BUT USE -shift  │
│ INSTEAD +shift  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ OUTPUT: "Hello" │
└─────────────────┘
```

---

## 📖 BAGIAN 2: LSB STEGANOGRAPHY FLOW

### 🖼️ Embedding Process

```
┌─────────────────┐
│  SECRET TEXT    │
│     "Hi"        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ TEXT_TO_BINARY  │
│ H=72=01001000   │
│ i=105=01101001  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ BINARY STRING   │
│"0100100001101001"│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ CREATE HEADER   │
│ Length=16 bits  │
│ 32-bit header   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   FULL DATA     │
│[Header][Data]   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  LOAD IMAGE     │
│ Convert to RGB  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ CHECK CAPACITY  │
│ Max = W×H×3     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ FOR EACH PIXEL  │
│   (R, G, B)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ EMBED LSB       │
│ R = (R&0xFE)|bit│
│ G = (G&0xFE)|bit│
│ B = (B&0xFE)|bit│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  SAVE IMAGE     │
│ stego_image.bmp │
└─────────────────┘
```

### 🔍 Extraction Process

```
┌─────────────────┐
│ STEGO IMAGE     │
│ stego_image.bmp │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  LOAD IMAGE     │
│ Convert to RGB  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ FOR EACH PIXEL  │
│   (R, G, B)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ EXTRACT LSB     │
│ R&1, G&1, B&1   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ BINARY STRING   │
│"001...101001..."│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ READ HEADER     │
│ First 32 bits   │
│ Get data length │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ EXTRACT DATA    │
│ Next N bits     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ BINARY_TO_TEXT  │
│ Convert to chars│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ OUTPUT: "Hi"    │
└─────────────────┘
```

---

## 📖 BAGIAN 3: COMBINED MODE FLOW

### 🔄 Encoding (Encrypt + Embed)

```
┌─────────────────┐
│  PLAINTEXT      │
│ "Secret msg"    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ CAESAR ENCRYPT  │
│   Shift = 7     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  CIPHERTEXT     │
│ "Zljyla tzn"    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ LSB EMBEDDING   │
│ Hide in image   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ STEGO IMAGE     │
│ combined.bmp    │
└─────────────────┘
```

### 🔄 Decoding (Extract + Decrypt)

```
┌─────────────────┐
│ STEGO IMAGE     │
│ combined.bmp    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ LSB EXTRACTION  │
│ Get hidden data │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  CIPHERTEXT     │
│ "Zljyla tzn"    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ CAESAR DECRYPT  │
│   Shift = 7     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  PLAINTEXT      │
│ "Secret msg"    │
└─────────────────┘
```

---

## 📖 BAGIAN 4: LSB EMBEDDING DETAIL

### 🔍 Bit-Level Operations

```
Original Pixel: (150, 200, 75)
Binary:         (10010110, 11001000, 01001011)
                      ↑        ↑        ↑
                     LSB      LSB      LSB

Data to embed: "101"

Step 1: Embed '1' in Red LSB
10010110 & 11111110 = 10010110  (Clear LSB)
10010110 | 00000001 = 10010111  (Set LSB to 1)
Result: 151

Step 2: Embed '0' in Green LSB  
11001000 & 11111110 = 11001000  (Clear LSB)
11001000 | 00000000 = 11001000  (Set LSB to 0)
Result: 200

Step 3: Embed '1' in Blue LSB
01001011 & 11111110 = 01001010  (Clear LSB)
01001010 | 00000001 = 01001011  (Set LSB to 1)
Result: 75

Final Pixel: (151, 200, 75)
Visual Change: Minimal (1-2 intensity levels)
```

---

## 📖 BAGIAN 5: DATA STRUCTURE LAYOUT

### 🗂️ Image Data Format

```
┌─────────────────────────────────────────┐
│              STEGO IMAGE                │
├─────────────────────────────────────────┤
│ Pixel 1: (R₁, G₁, B₁)                  │
│          ↓   ↓   ↓                      │
│         b₁  b₂  b₃  ← First 3 bits     │
├─────────────────────────────────────────┤
│ Pixel 2: (R₂, G₂, B₂)                  │
│          ↓   ↓   ↓                      │
│         b₄  b₅  b₆  ← Next 3 bits      │
├─────────────────────────────────────────┤
│ ...                                     │
├─────────────────────────────────────────┤
│ Pixel 11: (R₁₁, G₁₁, B₁₁)              │
│           ↓    ↓    ↓                   │
│          b₃₁  b₃₂  b₃₃ ← Bits 31-33    │
└─────────────────────────────────────────┘

Bit Layout:
b₁b₂b₃...b₃₂ = 32-bit Header (Data Length)
b₃₃b₃₄...bₙ  = Actual Data Bits
```

### 📊 Header Structure

```
32-bit Header Format:
┌─────────────────────────────────────────┐
│ 00000000 00000000 00000000 00010000     │
└─────────────────────────────────────────┘
│                                    │
│                                    └─ Data Length = 16 bits
└─ Leading zeros for fixed 32-bit format

Example for "Hi" (16 bits):
Header: "00000000000000000000000000010000"
Data:   "0100100001101001"
Total:  48 bits needed
```

---

## 📖 BAGIAN 6: ERROR HANDLING FLOW

### ⚠️ Validation Chain

```
┌─────────────────┐
│   USER INPUT    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  FILE EXISTS?   │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │YES        │NO
    ▼           ▼
┌─────────┐ ┌─────────┐
│CONTINUE │ │ ERROR   │
└────┬────┘ │MESSAGE  │
     │      └─────────┘
     ▼
┌─────────────────┐
│ VALID FORMAT?   │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │YES        │NO
    ▼           ▼
┌─────────┐ ┌─────────┐
│CONTINUE │ │ ERROR   │
└────┬────┘ │MESSAGE  │
     │      └─────────┘
     ▼
┌─────────────────┐
│ SIZE OK?        │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │YES        │NO
    ▼           ▼
┌─────────┐ ┌─────────┐
│PROCESS  │ │ ERROR   │
│DATA     │ │MESSAGE  │
└─────────┘ └─────────┘
```

---

## 🎯 Kesimpulan Diagram

Diagram-diagram ini menunjukkan:

1. **Program Flow:** Struktur menu dan navigasi
2. **Algorithm Flow:** Langkah-langkah detail setiap proses
3. **Data Flow:** Transformasi data dari input ke output
4. **Bit-Level Operations:** Manipulasi data pada level bit
5. **Error Handling:** Validasi dan penanganan kesalahan

Setiap bagian saling terhubung membentuk sistem yang komprehensif untuk kriptografi dan steganografi.