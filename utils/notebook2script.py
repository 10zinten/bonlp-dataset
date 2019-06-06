#!/usr/bin/env python

import json,fire,re
from pathlib import Path

def is_export(cell):
    if cell['cell_type'] != 'code': return False
    src = cell['source']
    if len(src) == 0 or len(src[0]) < 7: return False
    #import pdb; pdb.set_trace()
    return re.match(r'^\s*#\s*export\s*$', src[0], re.IGNORECASE) is not None

def notebook2script(fname):
    fname = Path(fname)
    fname_out = f'{fname.stem}.py'
    main_dic = json.load(open(fname,'r'))
    code_cells = [c for c in main_dic['cells'] if is_export(c)]
    module = f''

    for cell in code_cells: module += ''.join(cell['source'][1:]) + '\n\n'
    # remove trailing spaces
    module = re.sub(r' +$', '', module, flags=re.MULTILINE)
    open(fname.parent/fname_out,'w').write(module[:-2])
    print(f"Converted {fname} to {fname_out}")

if __name__ == '__main__': fire.Fire(notebook2script)
