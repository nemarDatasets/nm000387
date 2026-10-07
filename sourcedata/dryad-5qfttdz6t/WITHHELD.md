# File of the Dryad release not redistributed here

| file | Dryad file id | bytes | sha-256 |
|---|---|---|---|
| `fig2_contspk_LFP_iEEG_data.mat` | 1227896 | 1712953646 | `4dd56315e478973c0f91b6cb9059444367c78e830d094253392814331b23bf65` |

Reason: its `subjsessions` variable holds the participants' recording session names, which are date and time stamps
(`YYMMDD_HHMM`). All of its numeric arrays (`iEEGripple_sig_cont`, `iEEGripple_win`, `lfpripple_sig_cont`,
`lfpripple_win`, `spkrt_Z_win`) and the participant codes (`subjnames`) are carried over unchanged in
`sub-02` .. `sub-07/ieeg/sub-XX_desc-fig2session<N>_ripplewindows.mat` (exact round-trip, see `code/f05x_build054.py`).
The original file remains available from Dryad: https://doi.org/10.5061/dryad.5qfttdz6t
