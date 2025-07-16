<a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://raw.githubusercontent.com/OfficialCodexplosive/README_Assets/862a93188b61ab4dd0eebde3ab5daad636e129d5/FJZ_IEK-3_logo.svg" alt="FZJ Logo" width="300px"></a>

LOCALISED Datasharing API Client
==============================

Step-by-step instructions to access data, published on LOCALISED datasharing platform, via our API client. The official API documentation can be found under [http://data.localised-project.eu/api/docs/](http://data.localised-project.eu/dsp/docs/))

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
    mamba env create -f requirements.yml 
    conda activate dsp_client
    ```

4. Installing the repository:
    ```bash
    pip install -e.
    ```

5. Run the example Jupyter notebooks -  `examples/single_variable_data.ipynb` and `examples/single_region_data.ipynb`

    **Depending on type of query, the list of required parameters change. Please refer to the doc strings of each funtion to get the entire list of relevant parameters. They would be a subset of the ones below:**

    - `version` --> The DSP version that you want to query. For example: "v1", "v2", etc. **DSP latest version - v5**

    - `country_code` --> The country for which you wish to query the data. For example: "de", "es", "nl", etc

    - `spatial_resolution` --> Options - NUTS0, NUTS1, NUTS2, NUTS3, LAU 

    - `region_code` --> If you wish to filter on a particular region, provide a region code here. 
        Please note the following:
        - Region codes at NUTS0, follow the [EU country codes](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes)
        - Region codes at NUTS1, NUTS2, and NUTS3 can be found on [Eurostat](https://ec.europa.eu/eurostat/de/web/nuts/local-administrative-units). 
            These codes are subject to change every 4 years. We follow NUTS 2016 codes. 
        - Region codes at LAU can be found on [Eurostat](https://ec.europa.eu/eurostat/de/web/nuts/local-administrative-units). 
            These codes are subject to change every year. We follow LAU2019 for all countries, except France and Italy. For these countries, LAU2018 is followed. 
            The `region_code` parameter takes LAU codes in the form "< NUTS3 > _ < LAU >". Therefore, please prepend the parent NUTS3 region and an "_" to a LAU code. 
            For example, LAU code of Eixen, Germany is "13073022". And its parent NUTS3 code is "DE80L". Therefore, `region_code` = "DE80L_13073022". 

            For a list of region codes, please query the region metadata. 
        
    - `variable` --> If you wish to get data for a particular variable, provide the name here

    - `pathway_description` --> If you wish to filter on a particular EUCalc decarbonisation pathway, provide the name here. Can be either "national" or "with_behavioural_changes"

    - `climate_experiment` --> If you wish to filter on a particular climate experiment, provide the name here. Can be one of "RCP2.6", "RCP4.5", "RCP8.5", "Historical"



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## About Us
<p align="center"><a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://github.com/OfficialCodexplosive/README_Assets/blob/master/iek3-wide.png?raw=true" alt="Institut TSA"></a></p>
We are the <a href="https://www.fz-juelich.de/en/iek/iek-3">Institute of Energy and Climate Research - Techno-economic Systems Analysis (IEK-3)</a> belonging to the <a href="https://www.fz-juelich.de/en">Forschungszentrum Jülich</a>. Our interdisciplinary department's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.

## Acknowledgement
This work was developed as part of the project [LOCALISED](https://www.localised-project.eu/) —Localised decarbonization pathways for citizens, local administrations and businesses to inform for mitigation and adaptation action. This project received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No. 101036458. This work was also supported by the Helmholtz Association as part of the program “Energy System Design”. 
