Datasharing API
==============================

Step-by-step instructions to access data via our datasharing API. The official API documentation can be found under http://data.localised-project.eu/api/v1/docs/)

First, clone the repository and install all the required Python libraries in a fresh conda environment.

1. Cloning the repository:
    ```bash
    git clone https://jugit.fz-juelich.de/iek-3/shared-code/localised/datasharing-api.git
    ```

2. Installing dependencies in a clean conda environment:
    ```bash
    cd datasharing-api
    conda env create -n datasharing_api -f requirements.yml 
    conda activate datasharing_api
    ```

Next, access the data and get it in a Pandas DataFrame. 

3. In a fresh Python file or Jupyter notebook, import the following libraries:
    ```bash
    import requests
    from pandas import json_normalize 
    ```

3. The API request can be made as shown below. The URL contains all the query parameters and must be provided in the format - 
"http://data.localised-project.eu/api/v1/<resolution>/?api_key=<API key>&region=<region code>&type=<request type>". For more information, please refer to the [API documentation](http://data.localised-project.eu/api/v1/docs/)
    ```bash
    response = requests.get("http://data.localised-project.eu/api/v1/NUTS3/?api_key=S3cr3TK3y&region=DEA23&type=data")
    ```

4. The data returned is in json format and can be accessed using the following command:
    ```bash
    response_json = response.json()
    response_json
    ```

5. Parts of the json file can be accessed separately. For example, the region name can be access using the following command:
    ```bash
    response_json.get('regions')[0].get('region_name')
    ```

6. Finally, all the regional data can be dumped into a Pandas DataFrame using the following command:
    ```bash
    data_df = json_normalize(response_json.get('regions')[0].get('region_data'))
    data_df
    ```
