import argparse
import io
import glob
import os
import json

from docx import Document
from tqdm import tqdm


def format_para(para, pos):
    left_para = para[:pos]
    right_para = para[pos:]
    return '*'.join([left_para, right_para])

def dump_into_doc(fn):
    with io.open(fn, 'r', encoding='utf-8-sig') as f:
        objects = sorted(json.load(f), key=lambda o: o['type'])
    
    doc = Document()
    for o in tqdm(objects):
        para = o['ex']
        type = o['type']
        key = o['key']
        pos = o['pos']

        para = format_para(para, pos)

        values = [para, type, key]
        keys = ['Example', 'Type', 'Key']

        
        table = doc.add_table(rows=3, cols=2)
        for i, row in enumerate(table.rows):
            row.cells[0].width = 10
            row.cells[0].text = keys[i]
            row.cells[1].text = values[i]
        
        doc.add_page_break()

    out_fn, _ = os.path.basename(fn).split('.')
    out_path = os.path.join('data/export', '{}.docx'.format(out_fn))
    doc.save(out_path)



if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)                                              
    ap.add_argument("--path", type=str, help="path to corpus")                                
    args = ap.parse_args()

    fns = sorted(glob.glob(os.path.join(args.path, "*.json")))
    for fn in tqdm(fns):
        dump_into_doc(fn)                      
