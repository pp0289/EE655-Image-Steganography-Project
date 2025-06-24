# 🖼️ Crypto-Based Image Steganography Tool

> A secure Python tool for hiding images inside other images using encryption and randomized Least Significant Bit (LSB) encoding.

---

## 🧭 Overview

This project implements a **robust and secure steganography system** that embeds a **message image** into a **cover image** with:

* 💬 **Symmetric encryption (Fernet)** for confidentiality
* 🎲 **Key-based pseudo-random embedding** for security
* ⚙️ **Adjustable bit-depth** to control image quality vs. capacity

Ideal for scenarios where both **stealth** and **security** are essential.

---

## ✨ Features

* 🔐 **Encrypted Embedding**

  * Encrypts the message using **Fernet** before hiding it.
  * Embeds encrypted data using pseudo-random pixel selection seeded by the user’s key.

* ⚙️ **Bit-Depth Control**

  * Allows selection of 1 to 8 bits per pixel channel for more or less subtlety.

* 🖼️ **Broad Format Support**

  * Supports `.png`, `.jpg`, `.bmp`, and other common formats via **OpenCV**.

* 🧱 **Secure Architecture**

  * Without the encryption key:

    * Pixel locations are unpredictable.
    * Extracted data remains undecipherable.

* 🧑‍💻 **Interactive Command-Line Tool**

  * Simple CLI interface with step-by-step prompts for ease of use.

---

## 🔧 How It Works

### 📥 Encoding Process

1. Load the **cover image** and **message image**.
2. Encrypt the message using **Fernet** with a user-provided key.
3. Convert the encrypted data into binary format.
4. Use the key to seed NumPy’s random number generator.
5. Embed bits in pseudo-randomly selected pixel locations using **LSB**.
6. Save the final **stego image**.

### 📤 Decoding Process

1. Load the **stego image**.
2. Recreate the random pixel order using the same key.
3. Extract the embedded binary data.
4. Decrypt using the same Fernet key.
5. Reconstruct and save the **original message image**.

---

## 🔐 Security Model

| 🔒 Layer                     | Description                                                         |
| ---------------------------- | ------------------------------------------------------------------- |
| **Message Encryption**       | Fernet encryption ensures confidentiality and integrity.            |
| **Key-Driven Embedding**     | Embedding and extraction rely on the exact same key.                |
| **Randomized Bit Placement** | Obscures the embedding pattern against visual/statistical analysis. |

---

## 💻 Usage Instructions

### 🧬 To Encode

```bash
$ python steg_tool.py
Enter the path to the cover image: cover.jpg
Enter the path to the message image: secret.png
Do you want to start encoding? (y/n): y
```

### 🔎 To Decode

```bash
Do you want to decode the message? (y/n): y
```

📁 **Output:**

* `stego.png` — Stego image containing the encrypted hidden message.
* `decoded_message.png` — Recovered message image after decoding.

---

## 🧪 Experimental Results

| ✅ Evaluation Metric     | Result                                 |
| ----------------------- | -------------------------------------- |
| **Visual Distortion**   | Minimal up to 4-bit embedding          |
| **Message Recovery**    | 100% accurate with correct key         |
| **Unauthorized Access** | Fails without correct key and RNG seed |

---

## 🧾 Sample Output

| Cover Image  | Stego Image    |
| ------------ | -------------- |
| ![](rcb.jpg) | ![](stego.png) |

| Hidden Message  | Recovered Message        |
| --------------- | ------------------------ |
| ![](trophy.jpg) | ![](decoded_message.png) |

---

## 🧰 Tech Stack

* 🐍 Python 3.x
* 🖼️ OpenCV (`cv2`) for image processing
* 📊 NumPy for data manipulation and randomization
* 🔐 Cryptography (`Fernet`) for secure message encryption

---

## 👨‍🎓 Project Team

> Developed as part of **EE655: Steganography and Watermarking**
> *Indian Institute of Technology Kanpur*

* **Satwik Raj Wadhwa** (230937)
* **Gaurav Kumar** (230792)
* **Vinay Chavan** (231155)
* **Pritam Priyadarshi** (230793)
* **Course Instructor:** Prof. *Koteswar Rao Jerripothula*

---
