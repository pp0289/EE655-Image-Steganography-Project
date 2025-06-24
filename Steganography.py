import cv2
import numpy as np
from cryptography.fernet import Fernet

# --- Edge-Based LSB Steganography Functions ---

def text_to_binary(text):
    binary = ''.join(format(ord(i), '08b') for i in text)
    return binary

def binary_to_text(binary):
    bytes_list = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''.join(chr(int(byte, 2)) for byte in bytes_list if byte != '')
    return text

def detect_edges(image, low_threshold=50, high_threshold=150):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    return edges

def get_edge_positions(edges):
    y, x = np.where(edges != 0)
    return list(zip(y, x))

def embed_edge_message(cover_path, message, output_path, low_threshold=50, high_threshold=150):
    cover_image = cv2.imread(cover_path)
    if cover_image is None:
        raise ValueError("Failed to load cover image")
    
    binary_message = text_to_binary(message)
    total_bits = len(binary_message)
    
    edges = detect_edges(cover_image, low_threshold, high_threshold)
    edge_positions = get_edge_positions(edges)
    
    capacity = len(edge_positions) * 3
    if total_bits > capacity:
        raise ValueError("Message too long for the cover image")
    
    stego_image = cover_image.copy()
    msg_idx = 0
    for y, x in edge_positions:
        if msg_idx >= total_bits:
            break
        for channel in range(3):
            if msg_idx >= total_bits:
                break
            pixel = stego_image[y, x, channel]
            bit = int(binary_message[msg_idx])
            stego_image[y, x, channel] = (pixel & 0xFE) | bit
            msg_idx += 1
    
    cv2.imwrite(output_path, stego_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print(f"Edge-based stego image saved as {output_path}")
    return total_bits

def extract_edge_message(stego_path, total_bits, low_threshold=50, high_threshold=150):
    stego_image = cv2.imread(stego_path)
    if stego_image is None:
        raise ValueError("Failed to load stego image")
    
    edges = detect_edges(stego_image, low_threshold, high_threshold)
    edge_positions = get_edge_positions(edges)
    
    extracted_bits = ''
    bit_count = 0
    for y, x in edge_positions:
        for channel in range(3):
            if bit_count >= total_bits:
                break
            pixel = stego_image[y, x, channel]
            lsb = pixel & 1
            extracted_bits += str(lsb)
            bit_count += 1
        if bit_count >= total_bits:
            break
    
    message = binary_to_text(extracted_bits[:total_bits])
    return message

# --- Multi-Level Steganography (MLS) Functions ---

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def randomize_pixels(image):
    height, width, _ = image.shape
    pixels = np.arange(height * width).reshape(height, width)
    np.random.shuffle(pixels.ravel())
    return pixels

def mls_embed(cover_path, message, output_path, key):
    cover_image = cv2.imread(cover_path)
    if cover_image is None:
        raise ValueError("Failed to load cover image")
    
    encrypted_message = encrypt_message(message, key)
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
    
    randomized_pixels = randomize_pixels(cover_image)
    flat_image = cover_image.reshape(-1, 3)
    
    msg_idx = 0
    for i in range(len(flat_image)):
        for c in range(3):
            if msg_idx < len(binary_message):
                bit = int(binary_message[msg_idx])
                flat_image[i][c] = (flat_image[i][c] & 0xFE) | bit
                msg_idx += 1
            else:
                break
        if msg_idx >= len(binary_message):
            break
    
    stego_image = flat_image.reshape(cover_image.shape)
    cv2.imwrite(output_path, stego_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print(f"MLS stego image saved as {output_path}")
    return len(binary_message)

def mls_extract(stego_path, total_bits, key):
    stego_image = cv2.imread(stego_path)
    if stego_image is None:
        raise ValueError("Failed to load stego image")
    
    flat_image = stego_image.reshape(-1, 3)
    extracted_bits = ''
    bit_count = 0
    for i in range(len(flat_image)):
        for c in range(3):
            if bit_count >= total_bits:
                break
            lsb = flat_image[i][c] & 1
            extracted_bits += str(lsb)
            bit_count += 1
        if bit_count >= total_bits:
            break
    
    byte_length = total_bits // 8
    binary_str = extracted_bits[:byte_length * 8]
    bytes_list = [int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8)]
    encrypted_message = bytes(bytes_list)
    message = decrypt_message(encrypted_message, key)
    return message

# Example usage
if __name__ == "__main__":
    cover_path = r"C:\Users\vinay\OneDrive\Pictures\prince.jpg"  # Replace with your cover image path
    message = "Hello, My password is Password @12345"
    edge_output = "edge_stego.png"
    mls_output = "mls_stego.png"
    
    # Edge-Based Steganography
    try:
        total_bits = embed_edge_message(cover_path, message, edge_output)
        extracted = extract_edge_message(edge_output, total_bits)
        print("Edge-Based Extracted message:", extracted)
    except Exception as e:
        print(f"Edge-Based Error: {e}")
    
    # MLS Steganography
    try:
        key = generate_key()
        total_bits = mls_embed(cover_path, message, mls_output, key)
        extracted = mls_extract(mls_output, total_bits, key)
        print("MLS Extracted message:", extracted)
    except Exception as e:
        print(f"MLS Error: {e}")


# import cv2
# import numpy as np
# from cryptography.fernet import Fernet
# import os

# # Generate encryption key
# def generate_key():
#     return Fernet.generate_key()

# # Encrypt data
# def encrypt_data(data, key):
#     fernet = Fernet(key)
#     return fernet.encrypt(data)

# # Decrypt data
# def decrypt_data(encrypted_data, key):
#     fernet = Fernet(key)
#     return fernet.decrypt(encrypted_data)

# # Encode secret image into cover image
# def encode_image(secret_path, cover_path, stego_path, key_path):
#     # Load secret image and save as PNG (compression)
#     secret = cv2.imread(secret_path)
#     if secret is None:
#         raise ValueError("Failed to load secret image")
#     cv2.imwrite("compressed_secret.png", secret, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    
#     # Read compressed secret image as binary
#     with open("compressed_secret.png", "rb") as f:
#         secret_data = f.read()
    
#     # Encrypt the secret data
#     key = generate_key()
#     encrypted = encrypt_data(secret_data, key)
    
#     # Convert encrypted data to bit stream
#     bit_stream = ''.join(f'{byte:08b}' for byte in encrypted)
    
#     # Add 32-bit length prefix
#     total_bits = len(bit_stream)
#     length_bin = f'{total_bits:032b}'
#     full_bit_stream = length_bin + bit_stream
    
#     # Load cover image
#     cover = cv2.imread(cover_path)
#     if cover is None:
#         raise ValueError("Failed to load cover image")
    
#     # Flatten cover image
#     cover_flat = cover.reshape(-1, 3)
    
#     # Check if cover image has enough capacity
#     required_bits = len(full_bit_stream)
#     required_pixels = (required_bits + 2) // 3  # 3 bits per pixel
#     if len(cover_flat) < required_pixels:
#         raise ValueError(f"Cover image too small: needs {required_pixels} pixels, has {len(cover_flat)}")
    
#     # Embed bit stream into LSB of cover image
#     msg_idx = 0
#     for pixel in cover_flat:
#         for c in range(3):
#             if msg_idx < len(full_bit_stream):
#                 bit = int(full_bit_stream[msg_idx])
#                 pixel[c] = (pixel[c] & 0xFE) | bit  # Set LSB
#                 msg_idx += 1
#             else:
#                 break
#         if msg_idx >= len(full_bit_stream):
#             break
    
#     # Reshape back to image
#     stego = cover_flat.reshape(cover.shape)
    
#     # Save stego image
#     cv2.imwrite(stego_path, stego, [cv2.IMWRITE_PNG_COMPRESSION, 0])
#     print(f"Stego-image saved as {stego_path}")
    
#     # Save encryption key
#     with open(key_path, "wb") as f:
#         f.write(key)
#     print(f"Encryption key saved as {key_path}")

# # Decode secret image from stego-image
# def decode_image(stego_path, decoded_path, key_path):
#     # Load stego-image
#     stego = cv2.imread(stego_path)
#     if stego is None:
#         raise ValueError("Failed to load stego image")
    
#     # Flatten stego-image
#     stego_flat = stego.reshape(-1, 3)
    
#     # Extract bits from LSB
#     extracted_bits = ''
#     idx = 0
#     while len(extracted_bits) < 32:  # First, extract 32 bits for length
#         pixel = stego_flat[idx]
#         for c in range(3):
#             lsb = pixel[c] & 1
#             extracted_bits += str(lsb)
#             if len(extracted_bits) == 32:
#                 break
#         idx += 1
    
#     # Convert length bits to integer
#     total_bits = int(extracted_bits, 2)
    
#     # Continue extracting total_bits more bits
#     while len(extracted_bits) < 32 + total_bits:
#         pixel = stego_flat[idx]
#         for c in range(3):
#             lsb = pixel[c] & 1
#             extracted_bits += str(lsb)
#             if len(extracted_bits) == 32 + total_bits:
#                 break
#         idx += 1
    
#     # Extract message bits (excluding length)
#     message_bits = extracted_bits[32:32 + total_bits]
    
#     # Convert message bits to bytes
#     byte_list = [message_bits[i:i+8] for i in range(0, len(message_bits), 8)]
#     encrypted_data = bytes(int(b, 2) for b in byte_list if b)
    
#     # Load encryption key
#     with open(key_path, "rb") as f:
#         key = f.read()
    
#     # Decrypt the data
#     decrypted = decrypt_data(encrypted_data, key)
    
#     # Save decrypted data as image
#     with open(decoded_path, "wb") as f:
#         f.write(decrypted)
#     print(f"Decoded secret image saved as {decoded_path}")

# # Example usage
# if __name__ == "__main__":
#     # Paths
#     secret_path = r"C:\Users\vinay\OneDrive\Pictures\logout.png"  # Replace with your secret image path
#     cover_path = r"C:\Users\vinay\OneDrive\Pictures\prince.jpg"    # Replace with your cover image path
#     stego_path = "stego.png"
#     decoded_path = "decoded_secret.png"
#     key_path = "key.key"
    
#     try:
#         # Encode
#         encode_image(secret_path, cover_path, stego_path, key_path)
        
#         # Decode
#         decode_image(stego_path, decoded_path, key_path)
#     except Exception as e:
#         print(f"Error: {e}")