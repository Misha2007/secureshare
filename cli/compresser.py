import os, math
from collections import Counter
import struct

def shannon_entropy(data):
    freq = Counter(data)
    entropy = 0 
    for i in freq.values():
        p = i / len(data)
        if p > 0:
            result = p * math.log2(p)
            entropy -= result

    return entropy

def rle(data):
    pos = 0
    compressed = bytearray()
    while pos < len(data):
        run_byte = data[pos]
        count = 1
        while pos + count < len(data) and data[pos + count] == run_byte:
            count += 1
        compressed += struct.pack("!BH", run_byte, count)
        pos += count      
    return compressed

def compress_file(filepath: str, output_path: str = None, delete_original: bool = False) -> str:
    """
    Encrypts a file using a Fernet key (already base64 encoded).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")

    with open(filepath, "rb") as f:
        data = f.read()
    
    entropy = shannon_entropy(data) 
    if entropy > 7.9:
        print(entropy)
        print("Data is already very random. Skipping RLE.")
        return data  
    else:
        compressed_data = rle(data)

    output_path = "/home/mykhailo/secureshare/img-compressed.jpg"

    with open(output_path, "wb") as f:
        f.write(compressed_data)


filepath="/home/mykhailo/secureshare/img.jpg"
compress_file(filepath)