# Association between maize transcriptome and microbiome in leaves

This repository has codes associated with the analyses of associations between maize transcriptome and microbiome in leaves, primarily associated with Dr. Renato Santos internship abroad at the University of Georgia ([FAPESP scholarship 2023/11133-3](https://bv.fapesp.br/en/bolsas/212537/integrating-metataxonomics-and-host-transcriptomics-data-in-maize/)), which comprised a collaboration between [the Wallace Lab](https://wallacelab.uga.edu/) (PI: Dr. Jason G. Wallace) and the [Computational, Evolutionary and Systems Biology Laboratory](https://labbces.cena.usp.br/) (PI: Dr. Diego M. Riaño-Pachón).

Folders:

 * `general/` : sample annotation (maize genotypes, subpopulations, diurnal periods, and field plots) and some helper codes.
 * `transcriptome/` : normalization and filtering steps, generation and analysis of co-expression networks, plot generation for circadian-associated genes, heatmap generation (eigengenes).
 * `microbiome/` : normalization and filtering steps, differential abundance analyses, reconstruction and analysis of co-occurrence networks, heatmap generation (differentially abundant OTUs).
 * `transcriptome_microbiome/` : cross-correlations between microbiome and transcriptome, KO enrichment analysis.
 * `figures/`: most figures in main text and supplementary data (high resolution PDFs).

Additional code is available on our [GitHub wiki](https://github.com/labbces/maize_transcriptome_microbiome_diurnal_periods/wiki).

## Funding

* Brazilian São Paulo Research Foundation (FAPESP) grant numbers:
    * 2021/11057-0
    * 2023/11133-3
    * 2014/50884-5 (National Institute of Science and Technology of Bioethanol)
    * 2020/15230-5 (Research Centre for Greenhouse Gas Innovation)
* National Council for Scientific and Technological Development (CNPq) grant numbers:
    * 465319/2014-9
    * 311558/2021-6

## Citation

Preprint available on BioRxiv:

[dos Santos, Renato Augusto Correa, et al. "Identifying associations between maize leaf transcriptome and bacteriome during different diurnal periods." bioRxiv (2025): 2025-07.](https://www.biorxiv.org/content/10.1101/2025.07.11.664371v1)
