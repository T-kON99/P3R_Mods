import sys
import os
from pathlib import Path


def modify_skill_data(file_path):
    # Read the original file
    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) < 694:
        print("Error: File is too small to process")
        return

    header = data[:694]
    data_rest = data[694:]

    chunk_size = 86
    data_length = len(data_rest)
    num_chunks = data_length // chunk_size
    leftover = data_length % chunk_size

    modified_chunks = bytearray()
    changes = []

    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = bytearray(data_rest[start:end])
        original_value = chunk[65]
        chunk[65] = 0x01
        modified_chunks.extend(chunk)
        changes.append((i, original_value))

    # Append any leftover bytes unmodified
    modified_data = modified_chunks + data_rest[num_chunks * chunk_size :]

    # Create output data
    output_data = header + modified_data

    # Write to new file
    original_path = Path(file_path)
    output_path = original_path.with_stem(original_path.stem + "_modified")
    with open(output_path, "wb") as f:
        f.write(output_data)

    # Print changes
    print(f"Processed {num_chunks} skill entries.")
    for idx, original in changes:
        print(f"Skill entry {idx}: Changed target level from {original} to 1")
    print(f"\nModified file saved as: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drag and drop the DatSkillDataAsset.uasset file onto this script.")
        input("Press enter to exit...")
    else:
        file_path = sys.argv[1].strip('"')
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
        else:
            modify_skill_data(file_path)
            input("Press any key to exit")
