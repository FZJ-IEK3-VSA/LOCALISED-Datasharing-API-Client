LOCALISED Datasharing API Client
==============================

Step-by-step instructions to access data, published on LOCALISED datasharing platform, via our API client. The official API documentation can be found under http://data.localised-project.eu/api/v1/docs/)

0. Before you begin, please make sure you have mamba installed in your base environment:
    ```bash
    conda install mamba -c conda-forge
    ```

1. Clone the repository:
    ```bash
    git clone https://github.com/FZJ-IEK3-VSA/LOCALISED-Datasharing-API-Client.git
    ```

2. Installing dependencies in a clean conda environment:
    ```bash
    cd LOCALISED-Datasharing-API-Client
    mamba env create -n dsp_client -f requirements.yml 
    conda activate dsp_client
    ```

4. Installing the repository:
    ```bash
    pip install -e.
    ```

5. Run the example Jupyter notebooks -  `examples/single_variable_data.ipynb` and `examples/single_region_data.ipynb`

    **Depending on type of query, the list of required parameters change. Please refer to the doc strings of each funtion to get the entire list of relevant parameters. They would be a subset of the ones below:**

    - `api_key` --> The secret API key. **Note:** Please use the key shared with you in confidence

    - `country_code` --> The country for which you wish to query the data. For example: "de", "es", "nl", etc

    - `spatial_resolution` --> Options - NUTS0, NUTS1, NUTS2, NUTS3, LAU 

    - `region_code` --> If you wish to filter on a particular region, provide a region code here

    - `variable` --> If you wish to get data for a particular variable, provide the name here

    - `pathway_description` --> If you wish to filter on a particular EUCalc decarbonisation pathway, provide the name here. Can be either "national" or "with_behavioural_changes"

    - `climate_experiment` --> If you wish to filter on a particular climate experiment, provide the name here. Can be one of "RCP2.6", "RCP4.5", "RCP8.5", "Historical"



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>