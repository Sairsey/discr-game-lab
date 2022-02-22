import os
from os import listdir
from os.path import isfile, join
import json
from math import sqrt as s
import subprocess
params = {
    "email_user": "example@gmail.com",
    "service": "gmail",  # or outlook or yahoo
    "save_dir_name": "mail_saved",
    "password": "123"
}

def test_for(fname1 : str, fname2 : str):
    wrapper_code = ""
    with open("wrapper.py", "r") as f:
        wrapper_code = f.read()

    with open("tmp_wrapper.py", "w") as f:
        f.write("from " + params["save_dir_name"] + "." + fname1[:-3] + " import func as F1\n")
        f.write("from " + params["save_dir_name"] + "." + fname2[:-3] + " import func as F2\n")
        f.write(wrapper_code)
    res = None
    f = open("tmp.tmp", "w")
    try:
        res = subprocess.run(['python', 'tmp_wrapper.py'], timeout=20, stdout=f)
    except subprocess.TimeoutExpired:
        print(fname1 + " " + fname2 + "takes too long to finish.")
        return (fname1, fname2, 0)
    except subprocess.CalledProcessError:
        print(fname1 + " " + fname2 + "cannot compile")
        return (fname1, fname2, 0)
    f.close()
    f = open("tmp.tmp", "r")
    try:
        q = int(f.read())
    except:
        print(fname1 + " " + fname2 + "someone printing data.")
        return (fname1, fname2, 0)
    return (fname1, fname2, q)

def main(fname = "bot.json"):
    global params
    # at first I just load data from json
    with open(fname, "r") as f:
        params.update(json.loads(f.read()))

    if not os.path.exists(params["save_dir_name"]):
        os.mkdir(params["save_dir_name"])
    files_to_check = [f for f in listdir(params["save_dir_name"]) if isfile(join(params["save_dir_name"], f)) and f.endswith(".py")]
    all_res = []
    for i in range(len(files_to_check)):
        for j in range(len(files_to_check)):
            if i == j:
                continue
            res = test_for(files_to_check[i], files_to_check[j])
            all_res.append(res)
    print(all_res)


if __name__ == "__main__":
    s(5)
    main()