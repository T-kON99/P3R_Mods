import sys
import os
from skill_list import skills
from skill_uninheritable import skills_uninheritable
from skill_story import skill_story
from pathlib import Path

skillDict = {
    0: "Slash",
    1: "Strike",
    2: "Pierce",
    3: "Fire",
    4: "Ice",
    5: "Electric",
    6: "Wind",
    7: "Almighty",
    8: "Light",
    9: "Dark",
    10: "Charm",
    11: "Poison",
    12: "Distress",
    13: "Confuse",
    14: "Fear",
    15: "Rage",
    16: "Healing",
    17: "Support",
    255: "Passive",
}


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
    modified_chunks = bytearray()
    changes = []
    for skillID in range(num_chunks):
        start = skillID * chunk_size
        end = start + chunk_size
        chunk = bytearray(data_rest[start:end])
        affinity = chunk[13]
        sType = chunk[39]
        targetLv = chunk[65]
        originalLv = chunk[65]
        isMagicMastery = skillID == 866
        # Controls whether the given skillID is indeed a valid skill?
        isSkill = skillID in skills
        isStory = skillID in skill_story
        isUninheritable = skillID in skills_uninheritable
        # Change targetLv
        if isSkill:
            if isStory:
                targetLv = targetLv
            elif isUninheritable and targetLv == 0 and not isMagicMastery:
                # Change to rank 8 skills, make it easier to get magic mastery?
                # Debatable but....
                # For now, set it to rank 9 (can not mutate anymore), to make it fair game for difficulty wise
                targetLv = 0x09
            else:
                targetLv = targetLv
        else:
            if targetLv == 0:
                targetLv = 0x01
        chunk[65] = targetLv
        changes.append((skillID, originalLv, targetLv))
        modified_chunks.extend(chunk)

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
    modified = 0
    for idx, original, target in changes:
        if original != target:
            modified += 1
            print(
                f"Skill {skills.get(idx, {"Name": "Unused###" + str(idx)})["Name"]}: Changed target level from {original} to {target}"
            )
    print(f"modified {modified} num of skills out of {len(skills)} skills")
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
            try:
                modify_skill_data(file_path)
            except Exception as e:
                print(f"Exception happened, exception {e}")
            input("Press any key to exit")
