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

    - Options for `spatial_resolution` --> Europe, NUTS0, NUTS1, NUTS2, NUTS3, LAU 

    - `api_key` --> The secret API key. **Note:** Please use the key shared with you in the email 

    - `region` --> If you wish to filter on a particular region, provide a region code here



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>