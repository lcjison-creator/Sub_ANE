"""Load and verify the frozen dataset.

Usage (from a notebook in the folder that contains AE_freeze_v1.4/):
    import sys; sys.dont_write_bytecode = True     # keeps the frozen folder free of __pycache__
    sys.path.insert(0, 'AE_freeze_v1.4/code')
    from load_frozen import load, tables, verify
    verify()                                      # every file against manifest.json
    adm = load('admission_summary')               # typed: datetimes, nullable booleans, numbers
The first load of a table writes a typed copy to ./cache_frozen_tables/ (outside the frozen folder); later loads take about a second.
"""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
_DICT = None
_MANIFEST = None

def _dictionary():
    global _DICT
    if _DICT is None:
        _DICT = pd.read_csv(ROOT / 'docs' / 'data_dictionary.csv', dtype=str, keep_default_na=False, encoding='utf-8-sig')
    return _DICT

def _manifest():
    global _MANIFEST
    if _MANIFEST is None:
        _MANIFEST = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    return _MANIFEST

def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def tables():
    return sorted(_dictionary().table.unique())

def verify(verbose=True):
    """Check every file listed in manifest.json against its MD5 checksum and list files the manifest does not know.
    Returns the list of problems (empty when the folder is intact)."""
    man = _manifest()
    files = {v['file']: v['md5'] for v in man['tables'].values()}
    files.update({k: v['md5'] for k, v in man['documents'].items()})
    problems = []
    for rel, md5 in sorted(files.items()):
        p = ROOT / rel
        if not p.exists():
            problems.append(f'missing: {rel}')
        elif _md5(p) != md5:
            problems.append(f'changed: {rel}')
    known = set(files) | {'manifest.json'}
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT).as_posix()
        if p.is_file() and '__pycache__' not in p.parts and rel not in known:
            problems.append(f'not in manifest: {rel}')
    if verbose:
        print('Frozen dataset intact: every file matches manifest.json.' if not problems else 'Problems:\n  ' + '\n  '.join(problems))
    return problems

def load(name, cache=True, cache_dir=None):
    spec = _dictionary()[_dictionary().table == name]
    if spec.empty:
        raise KeyError(f'Unknown table {name!r}; available: {tables()}')
    path = ROOT / 'tables' / f'{name}.csv'
    digest = _manifest()['tables'][name]['md5'][:12]
    cdir = Path(cache_dir) if cache_dir else Path.cwd() / 'cache_frozen_tables'
    cfile = cdir / f'{ROOT.name}_{name}_{digest}_pd{pd.__version__}.pkl'
    if cache and cfile.exists():
        try:
            return pd.read_pickle(cfile)
        except Exception:
            pass
    df = pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[''], encoding='utf-8-sig')
    for col, typ in zip(spec['column'], spec['type']):
        if typ == 'datetime':
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        elif typ == 'float':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif typ == 'int':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        elif typ == 'bool':
            df[col] = df[col].map({'True': True, 'False': False}).astype('boolean')
    if cache:
        cdir.mkdir(parents=True, exist_ok=True)
        pd.to_pickle(df, cfile)
    return df
