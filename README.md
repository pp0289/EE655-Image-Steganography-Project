# 🕵️‍♂️ Image Steganography using Edge-Based LSB and Multi-Level Techniques

This Python project implements **two steganographic methods** for hiding messages inside images:

1. **Edge-Based LSB Steganography**: Hides the message in pixels located at edges detected via Canny edge detection.
2. **Multi-Level Steganography (MLS)**: Encrypts the message and embeds it randomly into pixel data using LSB substitution.

---

## 📂 Project Structure

```
├── steganography.py      # Main implementation with all functions
├── README.md             # Project documentation
├── edge_stego.png        # Output from edge-based embedding (generated)
├── mls_stego.png         # Output from MLS embedding (generated)
```

---

## 🛠️ Requirements

Install dependencies using:

```bash
pip install opencv-python numpy cryptography
```

---

## ▶️ How to Use

### 1. **Edge-Based LSB Steganography**

**Embed a message:**

```python
total_bits = embed_edge_message("cover.jpg", "Secret message", "edge_stego.png")
```

**Extract the message:**

```python
extracted = extract_edge_message("edge_stego.png", total_bits)
```

---

### 2. **Multi-Level Steganography (MLS)**

**Encrypt and embed the message:**

```python
key = generate_key()
total_bits = mls_embed("cover.jpg", "Secret message", "mls_stego.png", key)
```

**Extract and decrypt the message:**

```python
extracted = mls_extract("mls_stego.png", total_bits, key)
```

---

## 🔐 Features

* **Canny Edge Detection** ensures message embedding occurs only on informative image areas.
* **Fernet Encryption** secures the hidden message in the MLS method.
* **Randomized Pixel Embedding** makes detection harder in MLS.
* **PNG format** preserves LSB integrity better than JPEG.

---

## 📸 Sample Output

If successful, the script will produce:

* `edge_stego.png` — Image with message hidden in edge pixels.
* `mls_stego.png` — Image with encrypted message embedded randomly.

Both can be decoded using the respective extract functions.

---

## ⚠️ Notes

* Ensure the **cover image has enough edges** (for edge-based method).
* Use **lossless image formats (e.g., PNG)** to preserve embedded data.
* The key used for encryption in MLS must be kept safe to recover the message.

---

## 📃 License

This project is for educational and research purposes. Use responsibly.

---

Let me know if you want this in `.md` format or included inside a zip with the code files.
