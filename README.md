LOCALISED Datasharing API Client
==============================

Step-by-step instructions to access data via our API client. The official API documentation can be found under http://data.localised-project.eu/api/v1/docs/)

1. Clone public repository or repository of your choice first:
    ```bash
    git clone https://github.com/FZJ-IEK3-VSA/LOCALISED-Datasharing-API-Client.git
    ```

2. Installing dependencies in a clean conda environment:
    ```bash
    cd LOCALISED-Datasharing-API-Client
    conda env update -n datasharing_api -f requirements.yml 
    conda activate datasharing_api
    ```

3. Query the data. 

    The Python file, `data_access.py`, contains an example script that queries the data of a region and saves it as `.csv` and `.json` files. Simply run the script in the command line:
    ```bash
    python data_access.py
    ```

    Now, you can create a similar workflow in a fresh Python file or Jupyter notebook. 
    * First, import the required libraries
        ```bash
        import requests
        from pandas import json_normalize 
        ```

    * The command to make the API request is given below:
        ```bash
        request_url = "http://data.localised-project.eu/api/v1/NUTS3/?api_key=S3cr3TK3y&region=DEA23&type=data"
        response = requests.get(request_url)
        ```

    **The format of the request URL** - 

    `http://data.localised-project.eu/api/v1/<resolution>/?api_key=<API key>&region=<region code>&type=<request type>`. 

    The parameters are contained in this request URL. 

    **Parameters:**

    - Options for `resolution` --> Europe, NUTS0, NUTS1, NUTS2, NUTS3, LAU (Required parameter)

    - `api_key` --> The secret API key. **Note:** The key in the above URL is a dummy key. Please use the key shared with you in the email (Required parameter)

    - `region` --> The region code you want to filter on. If not specfied, a list of all regions are returned (Optional parameter)

    - `type` --> type=`data` if data needs to be accessed. If not specified, regional data is not returned (Optional parameter) 

    For more information, please refer to the [API documentation](http://data.localised-project.eu/api/v1/docs/)
    

    * The data returned is in json format and can be accessed using the following command:
        ```bash
        response_json = response.json()
        response_json
        ```

    * Parts of the json file can be accessed separately. For example, the region name can be accessed using the following command:
        ```bash
        response_json.get('regions')[0].get('region_name')
        ```

    * If you would like to save the entire response as a `.json` file, run the following commands: 
        ```bash
        import json
        with open('data.json', 'w') as f:
            json.dump(response_json, f)
        ```

    * Alternatively, all the regional data can be dumped into a Pandas DataFrame and saved using the following commands:
        ```bash
        data_df = json_normalize(response_json.get('regions')[0].get('region_data'))
        data_df.to_csv('region_data.csv')
        ```
