import os
import glob
import yaml as yml
import json

out_dir = '../data/toupload'
out_fns = sorted(glob.glob(os.path.join(out_dir, "*")))
keys_path = '../data/keys/test_keys.yml'

def test_key_in_para():
    with open(keys_path) as f:
        keys = yml.load(f.read())
        
    for fn in out_fns:
        with open(fn) as f:
             paras = json.load(f.read())
             print(len(paras))


if __name__ == "__main__":
    test_key_in_para()
