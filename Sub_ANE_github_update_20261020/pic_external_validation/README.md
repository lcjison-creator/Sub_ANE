# External validation in the PIC database

These notebooks apply the frozen admission-subphenotype model, without refitting, to children with acute encephalitis or
encephalopathy in the Paediatric Intensive Care (PIC) database, version 1.1.0 (PhysioNet). The cohort, measurements, outcomes,
replication criterion, sensitivity analyses and bedside rule were fixed in an addendum deposited on OSF (https://osf.io/ygtr2)
before the model was applied. The notebooks run on the computer that holds the PIC files and write aggregate tables only. PIC is
available on PhysioNet to credentialed users who sign its data use agreement; this folder contains no PIC data and no outputs.

| File | Purpose |
|---|---|
| `PIC_SUB_01_feasibility.ipynb` | Feasibility counts made before the addendum: children by diagnosis code, laboratory and vital-sign items, units and availability; nothing by subphenotype |
| `PIC_SUB_02_check.ipynb` | Checks the table files against the release's `SHA256SUMS.txt` and describes how the diagnosis codes match |
| `PIC_SUB_02_replication.ipynb` | Analysis of record: cohort, measurements, application of the frozen model, primary and secondary outcomes, sensitivity analyses S-a to S-g. SHA-256 of the cell sources, recorded by each run: `6193ed4ce89128519eb66ab93dd5fd1c16044a152e205a8c0217c027d1e42907` |
| `PIC_SUB_02_frozen_wuhan_model.json` | The frozen model (aggregate values only), as deposited on OSF. SHA-256 of the file: `a8a51287d7dd2cb67b623328ffedc663deb9a01b3c5364db3c4e9d8f39be2179`. `../AE_export_frozen_model.ipynb` rebuilds it |
| `PIC_SUB_02_config_template.txt` | Copy to `PIC_SUB_02_config.txt`: the OSF link and, if the PIC files are elsewhere, their folder |
| `PIC_SUB_03_posthoc.ipynb` | The code of PIC_SUB_02, unchanged, plus the post hoc analysis P-1 (inclusion codes among the discharge diagnoses). SHA-256 of the cell sources: `de0bea0faebb57565bb956b203f43119a74f47204f509be9ae1b0b37fd98fdc9` |
| `PIC_SUB_04_manuscript_outputs.ipynb` | Rebuilds from the exact tables every PIC number in the manuscript, Figure 7 with its legend and Additional file 2, Tables S27 to S33, and compares each with the manuscript build |
| `requirements_pic.txt` | Package versions of the PIC runs |

## Running

1. Create the environment once (Python 3.12):
   ```
   conda create -n ae_pic python=3.12 -y
   conda activate ae_pic
   pip install -r requirements_pic.txt
   ```
2. Put the notebooks, the model file and `PIC_SUB_02_config.txt` in one folder, with the PIC version 1.1.0 table files (the
   `v1.1.0` subfolder of the PhysioNet download, uncompressed `.csv`), or give the folder of the table files in the configuration
   file. PIC_SUB_01 reads `PIC_DIR` in its first code cell instead.
3. Run the notebooks in this order, each with *Restart Kernel and Run All Cells*: `PIC_SUB_01_feasibility`, `PIC_SUB_02_check`,
   `PIC_SUB_02_replication`, `PIC_SUB_03_posthoc`, `PIC_SUB_04_manuscript_outputs`. PIC_SUB_02 and PIC_SUB_03 take a few minutes
   each; the others under a minute.

Each notebook writes to its own folder. The folders ending in `_LOCAL_ONLY` hold the exact tables and stay on the computer that
ran the analysis; the other output folders hold the same tables in a coarse form (counts rounded to the nearest 5, counts of 1 to
4 shown as fewer than 5). PIC_SUB_04 reads the exact tables and prints MATCH or DIFFERENT for each of its five results.
`.gitignore` keeps the PIC files, the configuration file and every output folder out of the repository.
