# Sub_ANE: admission subphenotypes of childhood acute encephalopathy

Analysis code for the study *A hyperinflammatory subphenotype of childhood acute encephalopathy identifiable from routine admission
tests* (manuscript in preparation; the citation will be added on publication).

The analysis follows a plan registered on OSF (https://osf.io/ygtr2, under embargo; Preregistration Template for Secondary Data
Analysis). It applies
latent profile analysis to 24 routine laboratory tests and vital signs at admission in children with acute encephalopathy admitted
to Wuhan Children's Hospital from 2019 to 2026. It then tests whether the subphenotypes differ in IL-6, IL-10 and death or critical
discharge against medical advice (H2), reappear in two admission periods (H3) and add prognostic information beyond age and
consciousness (H4). Bootstrap stability, sensitivity analyses and two exploratory analyses that were not registered (E1, prognostic
information within the infection-triggered encephalopathy syndromes; E2, timing of immunomodulatory treatment) complete it.

## Contents

| File | Purpose |
|---|---|
| `AE_subphenotypes_analysis.ipynb` | The complete analysis, from the frozen dataset to every table, figure, figure legend, run log and supplementary file |
| `AE_subphenotypes_redraw_figures.ipynb` | Redraws the figures from the results saved by a full run, in about a minute, without rerunning the analysis |
| `requirements.txt` | Package versions of the reported run (Python 3.13) |
| `reference/load_frozen.py` | Copy of the loader shipped inside the frozen dataset (`AE_freeze_v1.4/code/`): reads its tables and checks every file against the dataset manifest. The notebook uses the copy inside the dataset. |

The computational module `ae_lpa_tools.py` (expectation-maximization for the resampling refits, bias-corrected three-step
estimation and related functions) is embedded in the analysis notebook, which writes it to `output_subphenotypes/code/` when it runs.

## Data

The patient-level data come from hospital medical records and are not publicly available; access is described in the data
availability statement of the article. This repository contains code only: no data, no child-level results and no outputs.

## Running the analysis

1. Put both notebooks in one folder with the frozen dataset `AE_freeze_v1.4/` (the folder that contains `manifest.json`) and, if
   available, the completed chart-review sheet `chart_review_completed.xlsx` (without it, the chart-review step is skipped).
2. Create the environment once:
   ```
   conda create -n ae_subpheno python=3.13 -y
   conda activate ae_subpheno
   pip install -r requirements.txt
   ```
3. Run the analysis from the command line (or open the notebook in JupyterLab and choose Run All):
   ```
   jupyter nbconvert --to notebook --execute AE_subphenotypes_analysis.ipynb --output AE_subphenotypes_run.ipynb --ExecutePreprocessor.timeout=-1
   ```

The notebook checks every file of the frozen dataset against its manifest and stops if StepMix is not version 3.0.0. Resampling
runs in up to 8 parallel processes; the reported run took 3.3 hours on 2 cores. Progress is written to
`output_subphenotypes/logs/progress.log`.

Outputs, all aggregated, are written to `output_subphenotypes/`: `tables/`, `figures/` (PDF and PNG, with `figure_legends.md`),
`logs/run_log.md` (settings, software, every check and every deviation from the registered plan) and `submission/` (the
supplementary tables and figures). Figures use Arial when it is installed. The last cell checks that no research number or
admission date appears in any output.

To change figures only, replace the analysis notebook with a version whose analysis cells are unchanged and run
`AE_subphenotypes_redraw_figures.ipynb`; it stops and asks for a full run if the analysis cells differ from those of the saved run.

## Child-level files stay local

A run writes two folders that hold child-level data: `cache_frozen_tables/` (typed copies of the frozen tables) and
`cache_figure_state/` (the saved results used for redrawing). Keep them on the computer that ran the analysis. `.gitignore`
excludes them, the dataset, the chart-review sheet and all outputs from this repository.

## Citation

To be added on publication.

## License

MIT License; see [LICENSE](LICENSE).
