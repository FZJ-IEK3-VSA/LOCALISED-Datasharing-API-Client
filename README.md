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

3. Run the example Jupyter notebooks -  `examples/all_regions_single_variable.ipynb` and `examples/single_region_all_variables.ipynb`

    **Depending on type of query, the list of required parameters change. Please refer to the doc strings of each funtion to get the entire list of relevant parameters. They would be a subset of the ones below:**

    - `api_key` --> The secret API key. **Note:** Please use the key shared with you in confidence

    - `spatial_resolution` --> Options - NUTS0, NUTS1, NUTS2, NUTS3, LAU 

    - `country_code` --> If you wish to filter on a particular region, provide its country code here

    - `region_code` --> If you wish to filter on a particular region, provide a region code here

    - `variable_name` --> If you wish to get data for a particular variable, provide the name here



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>