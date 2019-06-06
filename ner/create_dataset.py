import sys
sys.path.append('../')

import argparse
import os
import glob
from pathlib import Path

import yaml as yml
import jsonpickle as jp
from pybo import BoPipeline
from tqdm import tqdm

from lighttag.prepare_datasets import paragraphify, sentencify

jp.set_encoder_options('simplejson', sort_keys=True, indent=4, ensure_ascii=False)


def parse_keys(path):
    text = path.read_text()
    keys_dict = yml.load(text)
    return keys_dict


def unique_objects(objects, key):
    seen = set()
    return [seen.add(obj[key]) or obj for obj in objects if obj[key] not in seen]


def filter_and_format_para(paras):
    output = []
    keys_path = Path('keys.yml').resolve()
    keys_dict = parse_keys(keys_path)
    for i, para in enumerate(paras):
        para_str = ''.join([token.content for token in para[1]])
        for key_type, keys in keys_dict.items():
            for key in keys:
                idx = para_str.find(key)
                if idx >= 0:
                    output.append({'ex': para_str, 'order': i, 'type': key_type, 'key': key, 'pos': idx})
                    break

    output = unique_objects(output, 'ex')
    return jp.dumps(output)


if __name__ == "__main__":
    pipeline = BoPipeline('dummy',                            # preprocessor
                          'pybo',                             # tokenizer
                          ('pybo_paragraphs', paragraphify),  # processor
                          filter_and_format_para,             # formatter
                          pybo_profile='GMD')                 # pybo_profile
   
    ap = argparse.ArgumentParser(add_help=False)                  
    ap.add_argument("--path", type=str, help="path to corpus")    
    args = ap.parse_args()                               
                                                              
    fns = sorted(glob.glob(os.path.join(args.path, "*")))         
    for fn in tqdm(fns):
        pipeline.pipe_file(fn, 'data/toupload')

    # convert all the ext file to json
    out_dir = 'data/toupload'
    out_fns = sorted(glob.glob(os.path.join(out_dir, "*")))
    for fn in out_fns:
        if fn.endswith('.txt'):
            name, ext = fn.split('.')
            new_file = '{}.json'.format(name)
            os.rename(fn, new_file)
