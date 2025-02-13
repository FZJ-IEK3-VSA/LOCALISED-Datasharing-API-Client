# CoM Template Filling

This module automates the process of filling the Covenant of Mayors (CoM) reporting template with data from the LOCALISED Data Sharing Platform (DSP).

## Overview

The script performs the following main functions:
1. Retrieves region-specific data from the DSP
2. Calculates Socio-economic Output Indicators (SOIs)
3. Fills the CoM template with calculated values

## Directory Structure

```
CoM_template_filling/
├── data/
│   ├── input/
│   │   ├── variables_with_details_and_tags.xlsx
│   │   └── CoM-Europe_reporting_template_2023_v3.xlsx
│   └── output/
│       ├── SOIs_{region_code}.xlsx
│       └── CoM_{region_code}.xlsx
├── CoM_template_filling.py
└── README.md
```

## Prerequisites

- Python 3.11 or higher
- Required Python packages (specified in requirements.yml)
- Access to LOCALISED Data Sharing Platform
- Input files in the correct directory structure

## Setup

1. Ensure you have the correct directory structure with required input files
2. Create and activate the conda environment:

```bash
conda env create -f requirements.yml
conda activate dsp_client
```

## Usage

By default, the script will:
1. Process data for region code "DEA23"
2. Generate SOI calculations in `data/output/SOIs_{region_code}.xlsx`
3. Create filled CoM template in `data/output/CoM_{region_code}.xlsx`

To process a different region, modify the region code at **line 357** in the script `CoM_template_filling.py`

```bash
python CoM_template_filling/CoM_template_filling.py
```

## Output

The script generates the following outputs:
1. Calculated SOIs in Excel format
2. Filled CoM template in Excel format

## Output Files

1. **SOIs_{region_code}.xlsx**: Contains calculated Socio-economic Output Indicators
2. **CoM_{region_code}.xlsx**: Filled CoM template with region-specific data
3. **CoM_template_filling.log**: Execution log file

## Error Handling

The script includes comprehensive error handling and logging. Check the log file `CoM_template_filling.log` for execution details and any error messages.

## Contributing

Please ensure any contributions:
1. Follow the existing code style
2. Include appropriate error handling
3. Update documentation as needed



