#!/usr/bin/env python3
"""FINISHER-05x IEEG054 (Tong et al. 2021 eLife; Dryad doi:10.5061/dryad.5qfttdz6t) -> derivative BIDS tree.

- sourcedata/dryad-5qfttdz6t/: original release files byte-for-byte (Dryad digest re-checked), EXCEPT
  fig2_contspk_LFP_iEEG_data.mat, which is withheld because its `subjsessions` strings are recording date+time
  stamps (YYMMDD_HHMM) of the participants' sessions. Its sha-256 and Dryad file id are listed in SHA256SUMS/WITHHELD.md.
- sub-XX/ieeg/: per-participant copies of the original MAT files (bytes unchanged, renamed) and, for fig2, one MAT
  file per participant x session holding that cell of every fig2 variable (values unchanged; dates dropped).
- Round-trip: every fig2 array re-read and compared exactly (dtype + values) to the original cell.
Usage: f05x_build054.py <textdir>
"""
import json, os, shutil, sys
import numpy as np, scipy.io as sio
sys.path.insert(0, os.path.dirname(__file__))
from f05x_lib import *  # noqa

ID = 'IEEG054'; SLUG = 'dryad-5qfttdz6t'
SRC = f'{ROOT}/work/{ID}/sourcedata/{SLUG}'
TREE = f'{ROOT}/work/{ID}/bids'
REP = f'{ROOT}/work/{ID}/reports/f05x'
TEXT = sys.argv[1]
assert not os.path.exists(TREE + '/.nemar'), 'tree already uploaded; refusing to rebuild'
if os.path.exists(TREE):
    shutil.rmtree(TREE)
os.makedirs(TREE)
man = manifest(ID)
WITHHELD = 'fig2_contspk_LFP_iEEG_data.mat'

# participant mapping (source code -> sub label), order: fig1 participant, then fig2 subjnames order
SUBJ = {'NIH025': '01', 'NIH029': '02', 'NIH030': '03', 'NIH034': '04', 'NIH037': '05', 'NIH039': '06', 'NIH042': '07'}

report = {'id': ID, 'files': {}, 'roundtrip': {}, 'withheld': {}}
# 1. sourcedata
sd = f'{TREE}/sourcedata/{SLUG}'
sums = []
for n, exp in sorted(man.items()):
    if n == WITHHELD:
        dg = sha256(f'{SRC}/{n}')
        assert dg == exp[1]
        report['withheld'][n] = {'sha256': dg, 'bytes': exp[2], 'reason': 'subjsessions strings = recording date/time stamps'}
        continue
    report['files'][f'sourcedata/{SLUG}/{n}'] = copy_verified(f'{SRC}/{n}', f'{sd}/{n}', exp)
    sums.append((n, report['files'][f'sourcedata/{SLUG}/{n}']))
write_sha256sums(sd, sums, [f'# withheld from this deposit (see WITHHELD.md): {report["withheld"][WITHHELD]["sha256"]}  {WITHHELD}'])
log('sourcedata done')

# 2. per-participant copies of the original MAT files (bytes unchanged)
COPIES = {
    'fig1_NIH025_s1_chanTT1_data.mat': ('01', 'sub-01_desc-fig1s1chanTT1_tfpower.mat'),
    'fig1_NIH025_s1_chanTT1_rippleband_trials.mat': ('01', 'sub-01_desc-fig1s1chanTT1_rippleband.mat'),
    'fig1_NIH025_s1_chanTT1_rippleraster.mat': ('01', 'sub-01_desc-fig1s1chanTT1_rippleraster.mat'),
    'fig1_NIH025_s1_chanTT1_ripplerate.mat': ('01', 'sub-01_desc-fig1s1chanTT1_ripplerate.mat'),
    'fig3_LFP_iEEG_ripple_NIH037_data.mat': ('05', 'sub-05_desc-fig3_lfpieegripple.mat'),
    'fig3_LFP_iEEG_ripple_NIH037_PPC_computed.mat': ('05', 'sub-05_desc-fig3_ppc.mat'),
    'fig4_spike_LFP_NIH037_s1_data.mat': ('05', 'sub-05_desc-fig4s1_spikelfp.mat'),
}
for n, (s, newn) in COPIES.items():
    d = f'{TREE}/sub-{s}/ieeg/{newn}'
    dg = copy_verified(f'{SRC}/{n}', d, man[n])
    assert dg == report['files'][f'sourcedata/{SLUG}/{n}']
    report['files'][os.path.relpath(d, TREE)] = dg
log('copies done')

# 3. fig2 split per participant x session
m = sio.loadmat(f'{SRC}/{WITHHELD}')
VARS = ['iEEGripple_sig_cont', 'iEEGripple_win', 'lfpripple_sig_cont', 'lfpripple_win', 'spkrt_Z_win']
names = [str(np.asarray(e).ravel()[0]) for e in m['subjnames'].ravel()]
assert names == ['NIH029', 'NIH030', 'NIH034', 'NIH037', 'NIH039', 'NIH042'], names
fig2 = []
for i, code in enumerate(names):
    s = SUBJ[code]
    for j in range(m[VARS[0]].shape[1]):
        cells = {v: m[v][i, j] for v in VARS}
        if all(c.size == 0 for c in cells.values()):
            continue
        assert all(c.size > 0 for c in cells.values()), (code, j)
        out = f'{TREE}/sub-{s}/ieeg/sub-{s}_desc-fig2session{j + 1}_ripplewindows.mat'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sio.savemat(out, cells, format='5', do_compression=False, oned_as='row')
        back = sio.loadmat(out)
        ok = True
        for v in VARS:
            a, b = cells[v], back[v]
            ok &= (a.dtype == b.dtype and a.shape == b.shape and np.array_equal(a, b, equal_nan=True))
        report['roundtrip'][os.path.relpath(out, TREE)] = {'exact': bool(ok), 'shapes': {v: list(cells[v].shape) for v in VARS},
                                                           'dtypes': {v: str(cells[v].dtype) for v in VARS}}
        assert ok, out
        report['files'][os.path.relpath(out, TREE)] = sha256(out)
        fig2.append((s, code, j + 1, {v: list(cells[v].shape) for v in VARS}))
del m
# completeness: every non-empty cell went somewhere
report['fig2_cells'] = fig2
log('fig2 split done', len(fig2))

# 4. texts
report['texts'] = install_texts(TEXT, TREE)
os.makedirs(f'{TREE}/code', exist_ok=True)
for f in ('f05x_build054.py', 'f05x_lib.py'):
    shutil.copyfile(f'{ROOT}/harness/{f}', f'{TREE}/code/{f}')

# 5. checks
report['validator'] = validate(TREE, REP)
log('validator', report['validator'])
report['privacy'] = {k: v for k, v in privacy_scan(TREE, REP, allow=('Created on',)).items() if k != 'findings'}
report['privacy']['findings_head'] = json.load(open(REP + '/privacy.json'))['findings'][:30]
log('privacy', report['privacy']['n_findings'])
report['listing'] = tree_listing(TREE)
json.dump(report, open(REP + '/build.json', 'w'), indent=1)
print('RESULT', json.dumps({'validator': report['validator'], 'privacy_n': report['privacy']['n_findings'],
                            'roundtrip_all_exact': all(v['exact'] for v in report['roundtrip'].values()), 'n_files': len(report['listing'])}))
