from PIL import Image

# Convert message to binary
def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

# Convert binary to message
def binary_to_message(binary_data):
    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return ''.join(chars)

# Hide message
def hide_message(image_path, message, output_path):
    image = Image.open(image_path)
    binary_message = message_to_binary(message) + '1111111111111110'  # EOF
    data_index = 0
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_message):
            r = (r & ~1) | int(binary_message[data_index])
            data_index += 1
        if data_index < len(binary_message):
            g = (g & ~1) | int(binary_message[data_index])
            data_index += 1
        if data_index < len(binary_message):
            b = (b & ~1) | int(binary_message[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_path)
    print("✅ Message hidden in", output_path)

# Reveal message
def reveal_message(image_path):
    image = Image.open(image_path)
    binary_data = ''
    for pixel in image.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)

    eof_marker = '1111111111111110'
    end_index = binary_data.find(eof_marker)
    if end_index != -1:
        message_binary = binary_data[:end_index]
        message = binary_to_message(message_binary)
        print("🔓 Hidden message:", message)
    else:
        print("❌ No hidden message found.")

# ---- Example run ----

# Hide the message
hide_message('input.png', 'Hello from Steganography!', 'output_stego.png')

# Reveal the message
reveal_message('output_stego.png')
