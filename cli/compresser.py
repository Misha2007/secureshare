import os, math
from collections import Counter
import struct
import heapq
import struct

# ---------- RLE ----------
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

# ---------- Huffman ----------
class Node:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(freqs):
    heap = [Node(f, b) for b, f in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, Node(a.freq + b.freq, left=a, right=b))
    return heap[0]

def generate_codes(node, prefix="", table=None):
    if table is None: table = {}
    if node.byte is not None:
        table[node.byte] = prefix or "0"
    else:
        generate_codes(node.left, prefix + "0", table)
        generate_codes(node.right, prefix + "1", table)
    return table

def encode_data(data, codes):
    bits = "".join(codes[b] for b in data)
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding
    packed = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return packed, padding

def write_header(freqs):
    header = struct.pack(">H", len(freqs))
    for b, f in freqs.items():
        header += struct.pack(">BI", b, f)
    return header

def read_header(blob):
    n = struct.unpack_from(">H", blob, 0)[0]
    pos = 2
    freqs = {}
    for _ in range(n):
        b, f = struct.unpack_from(">BI", blob, pos)
        freqs[b] = f
        pos += 5
    return freqs, pos

def compress(data):
    freqs = dict(Counter(data))
    root = build_tree(freqs)
    codes = generate_codes(root)
    packed, padding = encode_data(data, codes)
    header = write_header(freqs)
    return header + struct.pack(">B", padding) + packed

def decompress(blob):
    freqs, pos = read_header(blob)
    padding = struct.unpack_from(">B", blob, pos)[0]
    pos += 1
    bitstring = "".join(f"{b:08b}" for b in blob[pos:])
    bitstring = bitstring[:-padding] if padding else bitstring
    root = build_tree(freqs)
    out, node = bytearray(), root
    for bit in bitstring:
        node = node.right if bit == "1" else node.left
        if node.byte is not None:
            out.append(node.byte)
            node = root
    return bytes(out)

def compress_file(filepath, output_path=None):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")
    with open(filepath, "rb") as f:
        data = f.read()
    compressed_data = compress(data)
    output_path = output_path or filepath + ".huf"
    with open(output_path, "wb") as f:
        f.write(compressed_data)
    print(f"Compressed {len(data)} -> {len(compressed_data)} bytes")
    return output_path

def decompress_file(filepath, output_path=None):
    with open(filepath, "rb") as f:
        blob = f.read()
    data = decompress(blob)
    output_path = output_path or filepath + ".orig"
    with open(output_path, "wb") as f:
        f.write(data)
    print(f"Decompressed to {output_path}")
    return output_path

if __name__ == "__main__":
    inp = "/path/to/file.txt"
    cmp = compress_file(inp)      
    dec = decompress_file(cmp) 
