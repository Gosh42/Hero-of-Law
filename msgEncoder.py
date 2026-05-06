import json
import string
import sys

def load_mapping(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    table = {}
    for entry in data["Entries"]:
        token = entry["Token"]
        bytes_list = [int(x, 16) for x in entry["Value"].split(";")]
        table[token] = bytes_list
    return table


def encode_string(s, table):
    out = []

    for ch in s:
        if ch in table:
            # Use the bytes defined in the JSON mapping
            for b in table[ch]:
                out.append(f"\\x{b:02X}")

        elif ord(ch) < 128:
            # ASCII — output as literal ASCII
            out.append(ch)

        else:
            # Non-ASCII but not in the table = error
            raise KeyError(f"Character {ch!r} not found in table.")

    return "".join(out)


# -------------------------------
# Example usage
# -------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Give me the json bro")
        sys.exit(1)

try:
    text = input('what do you need encoding my guy?: ')
    mapping = load_mapping(sys.argv[1])
    c_string = encode_string(text, mapping)
    print(c_string)
except KeyError as e:
    print("ERROR:", e)
    
