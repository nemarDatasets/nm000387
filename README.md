# Ripples reflect a spectrum of synchronous spiking activity in human anterior temporal lobe (Tong et al., 2021): figure-level arrays (derivative)

**This is a processed-data (derivative) dataset.** It repackages the authors' public Dryad release
(doi:[10.5061/dryad.5qfttdz6t](https://doi.org/10.5061/dryad.5qfttdz6t), version 2, CC0-1.0), which holds the data
needed to reproduce panels of Figures 1-4 of the article. **Raw continuous recordings are not part of the release and
are not included here.** The arrays are epochs, band-filtered signals, time-frequency power, ripple rasters and spike
indices that the authors derived from the recordings.

Article: Tong AP, Vaz AP, Wittig JH Jr, Inati SK, Zaghloul KA (2021). Ripples reflect a spectrum of synchronous spiking
activity in human anterior temporal lobe. *eLife* 10:e68401. doi:[10.7554/eLife.68401](https://doi.org/10.7554/eLife.68401)

## Overview

- 21 participants with drug-resistant epilepsy were implanted with subdural and depth contacts at the NIH Clinical
  Center (Bethesda, MD) and performed a paired-associates verbal episodic memory task. Six of them (4 female;
  34.8 ± 4.7 years) also had one or two 96-channel microelectrode arrays (MEA; Cereplex I, Blackrock) in the anterior
  temporal lobe (ATL) (article, Materials and methods, Participants).
- The release covers **7 participants**: one example iEEG participant for Figure 1 and the six MEA participants for
  Figure 2; Figures 3 and 4 use one of them.
- Processing described by the authors (Materials and methods): iEEG sampled at 1000 Hz, referenced to the hardware
  reference; local detrending (≤ 2 Hz, Chronux) and regression removal of 60 and 120 Hz line noise; Morlet wavelet
  power; retrieval epochs from 4 s before to 1 s after vocalization. Micro-LFP: 500 Hz low-pass of the MEA signals,
  downsampled to 1000 Hz, same line-noise removal. Single units: threshold crossing and manual spike sorting.
  Ripples: 80-120 Hz second-order Butterworth band-pass, Hilbert envelope > 2 SD for ≥ 25 ms with peak > 3 SD.
- The authors' MATLAB scripts (`generate_fig1..4_*.m`, referenced in their README) are published with the article as
  *Source code 1* (eLife); they are not part of the Dryad record.

## Participants

| participant_id | release code | data |
|---|---|---|
| sub-01 | NIH025 | Figure 1 (one medial temporal lobe iEEG electrode, "TT1", session "s1") |
| sub-02 | NIH029 | Figure 2 (MEA participant) |
| sub-03 | NIH030 | Figure 2 (MEA participant) |
| sub-04 | NIH034 | Figure 2 (MEA participant) |
| sub-05 | NIH037 | Figures 2, 3, 4 (MEA participant) |
| sub-06 | NIH039 | Figure 2 (MEA participant) |
| sub-07 | NIH042 | Figure 2 (MEA participant) |

The `NIHxxx` codes are the research pseudonyms used in the Dryad file names and in the Figure 2 `subjnames` variable;
the article itself does not list per-participant codes, ages or sexes, so `age` and `sex` are `n/a` in
`participants.tsv`.

## Files

All derivative data files are MATLAB v5 MAT files (load with `scipy.io.loadmat` in Python or `load` in MATLAB). They are
not BIDS raw data types and are listed in `.bidsignore`. Time axes are in seconds; signals are in the units of the
authors' export (not stated in the release).

### sub-01/ieeg/ (Figure 1; original files, bytes unchanged, renamed)

| file | original Dryad file | content |
|---|---|---|
| `sub-01_desc-fig1s1chanTT1_tfpower.mat` | `fig1_NIH025_s1_chanTT1_data.mat` | `TF` [44 trials x 150 frequencies x 5000 samples] wavelet power, `freqvec` (1-150 Hz), `timevec` (-3.999 .. 1.0 s, 1 kHz, relative to vocalization) |
| `sub-01_desc-fig1s1chanTT1_rippleband.mat` | `fig1_NIH025_s1_chanTT1_rippleband_trials.mat` | `ripple_band_TT1` [44 x 5000] 80-120 Hz band signal, `ripple_band_trials_time` |
| `sub-01_desc-fig1s1chanTT1_rippleraster.mat` | `fig1_NIH025_s1_chanTT1_rippleraster.mat` | `ripple_raster_TT1` [44 x 5000] detected-ripple indicator, `ripple_raster_time` |
| `sub-01_desc-fig1s1chanTT1_ripplerate.mat` | `fig1_NIH025_s1_chanTT1_ripplerate.mat` | smoothed ripple rate and SE for correct / incorrect trials (`ripplerate_sm_corr`, `_corr_se`, `_incorr`, `_incorr_se`) on `timevec_sm` (73 points) |

### sub-02 .. sub-07/ieeg/ (Figure 2; split per participant and session)

`sub-XX_desc-fig2session<N>_ripplewindows.mat`: one file per participant and recording session, holding that
participant/session cell of each Figure 2 variable of the original `fig2_contspk_LFP_iEEG_data.mat` (values and dtypes
unchanged, verified by exact round-trip):

- `iEEGripple_sig_cont` [1 x 4001 x n]: iEEG ripple-band signal segments (4001 samples at 1 kHz)
- `lfpripple_sig_cont` [n_MEA_electrodes x 4001 x n]: micro-LFP ripple-band signal segments
- `iEEGripple_win`, `lfpripple_win`, `spkrt_Z_win` [39 x n]: windowed iEEG ripple-band amplitude, LFP ripple-band
  amplitude and z-scored spike rate, used for the Figure 2 correlations (the authors' README: "computes the
  correlation between continuous spiking, LFP, and iEEG"). The exact meaning of each dimension follows the authors'
  Figure 2 script (eLife Source code 1); n is 102-144 per session.

`<N>` is the column of the session in the original cell arrays (1-3). The original `subjsessions` variable (session
names) is not carried over because the names are recording date/time stamps (see Privacy).

### sub-05/ieeg/ (Figures 3 and 4; original files, bytes unchanged, renamed)

| file | original Dryad file | content |
|---|---|---|
| `sub-05_desc-fig3_lfpieegripple.mat` | `fig3_LFP_iEEG_ripple_NIH037_data.mat` | `LFP_signal`, `LFPripple_sig` [148 epochs x 96 MEA channels x 4001 samples]; `iEEGripple_envZ`, `iEEGripple_logic` [148 x 4001 x 4 nearby iEEG channels] |
| `sub-05_desc-fig3_ppc.mat` | `fig3_LFP_iEEG_ripple_NIH037_PPC_computed.mat` | `LFPripple_ppc_max`, `iEEGripple_max` (cells, one per iEEG channel): maximum LFP pairwise phase consistency and iEEG ripple amplitude per ripple |
| `sub-05_desc-fig4s1_spikelfp.mat` | `fig4_spike_LFP_NIH037_s1_data.mat` | `LFP_timeseries` [18 electrodes x 118 trials x 4001], `spike_raster` [33 units x 4001 x 118], `spike_id`, `spike_ph` (spike indices and phases at 60 `freqs`, 2-400 Hz), `*_lfprip` (same within LFP ripples), `lfpripple_logic`, `lfp_channels`, `lfp_channels_u`, `el_cnt`, `response`, `trials` |

Every per-subject derivative file has a JSON sidecar of the same name (description, `Sources` pointing to the original release file, variables, how it was repackaged).

### sourcedata/dryad-5qfttdz6t/

The original release files, byte-for-byte, with `SHA256SUMS` (all digests match the Dryad API sha-256 values), the
authors' `README.rtf`, and `WITHHELD.md`.

### code/

`f05x_build054.py` and `f05x_lib.py`: the repackaging, round-trip, privacy-scan and validation code used here.

## Privacy

The original `fig2_contspk_LFP_iEEG_data.mat` contains a `subjsessions` variable whose strings are the participants'
recording session date and time stamps (`YYMMDD_HHMM`). Dates of clinical recordings are identifying information, so
that one file is **not** redistributed here. Its arrays are provided in full in the per-participant Figure 2 files
above; only the date strings are dropped. The original file stays available from Dryad (see
`sourcedata/dryad-5qfttdz6t/WITHHELD.md` for its sha-256). No other names, dates, record numbers or paths were found in
the file names, MAT strings or text files (MAT headers carry only the 2021 file-creation time).

## Ethics approval

"Data were collected at the Clinical Center at the National Institutes of Health (NIH; Bethesda, MD). The Institutional
Review Board (IRB) approved the research protocol (11-N-0051), and informed consent was obtained from the participants
and their guardians." (Tong et al. 2021, *eLife* 10:e68401, Ethics, Human subjects; the same statement appears in
Materials and methods, Participants.)

## Funding

From the article's Funding Information: "National Institute of Neurological Disorders and Stroke F31 NS113400 to Alex P
Vaz." and "National Institute of Neurological Disorders and Stroke Intramural Research Program to Kareem A Zaghloul."

## License and citation

CC0-1.0 (Dryad record license). Please cite the article (doi:10.7554/eLife.68401) and the Dryad dataset
(doi:10.5061/dryad.5qfttdz6t).
