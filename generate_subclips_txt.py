import os

SUBCLIPS = "subclips"
for file in os.listdir(SUBCLIPS):
    if file.endswith(".mp4"):
        if len(file.split(".")[0]) <= 4:
            padded_zeros = "".join(["0"] * (4 -  len(file.split(".")[0])))
            new_name = "".join([padded_zeros, file])
            os.rename(os.path.join(SUBCLIPS, file), os.path.join(SUBCLIPS, new_name))

with open("subclips.txt", "w") as f:
    for file in os.listdir(SUBCLIPS):
        if file.startswith("."):
            continue
        f.write("file '{}'\n".format(os.path.join(SUBCLIPS, file)))
