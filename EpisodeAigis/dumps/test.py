import json


def dump_dict_to_file(d: dict, path: str):
    toWrite = json.dumps(d, indent=4, ensure_ascii=False, sort_keys=False)
    with open(path, "w") as out:
        out.write(toWrite)


# Read the skill list
with open("test.txt", "r") as f:
    skillList = f.readlines()
    res = {
        x[0]: {"Name": x[1], "Description": x[2].strip()}
        for x in [i.split("\t") for i in skillList]
    }

    dump_dict_to_file(res, "skill_list.json")
