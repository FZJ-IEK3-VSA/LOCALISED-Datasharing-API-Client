<a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://raw.githubusercontent.com/OfficialCodexplosive/README_Assets/862a93188b61ab4dd0eebde3ab5daad636e129d5/FJZ_IEK-3_logo.svg" alt="FZJ Logo" width="300px"></a>

LOCALISED Datasharing API Client
==============================

Step-by-step instructions to access data, published on LOCALISED datasharing platform, via our API client. The official API documentation can be found under http://data.localised-project.eu/api/v1/docs/)

1. Clone the repository:
    ```bash
    git clone https://github.com/FZJ-IEK3-VSA/LOCALISED-Datasharing-API-Client.git
    ```

2. Installing dependencies in a clean conda environment:
    ```bash
    cd LOCALISED-Datasharing-API-Client
    conda env update -n zoomin-client -f requirements.yml 
    conda activate zoomin-client
    ```

3. Run the example Jupyter notebook `examples/data_access.ipynb` 

    **Parameters:**

    - Options for `spatial_resolution` --> NUTS0, NUTS1, NUTS2, NUTS3, LAU 

    - `api_key` --> The secret API key. **Note:** Please use the key shared with you in the email 

    - `region_code` --> If you wish to filter on a particular region, provide a region code here

    - `country_code` --> If you wish to filter on a particular region, provide its country code here



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## About Us
<p align="center"><a href="https://www.fz-juelich.de/en/iek/iek-3"><img src="https://github.com/OfficialCodexplosive/README_Assets/blob/master/iek3-wide.png?raw=true" alt="Institut TSA"></a></p>
We are the <a href="https://www.fz-juelich.de/en/iek/iek-3">Institute of Energy and Climate Research - Techno-economic Systems Analysis (IEK-3)</a> belonging to the <a href="https://www.fz-juelich.de/en">Forschungszentrum Jülich</a>. Our interdisciplinary department's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.
