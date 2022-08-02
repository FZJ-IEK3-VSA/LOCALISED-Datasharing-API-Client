#load required libraries 
import os
import json
import requests
from pandas import json_normalize

from dotenv import load_dotenv, find_dotenv

#load environment variables 
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#get the secret API key.

#NOTE: Please create a file named ".env" (note the dot) in the repository and save your secret key there.
#should look something like: SECRET_API_KEY=S3cr3TK3y
#This is then automatically loaded into your environment. 

SECRET_API_KEY = os.environ.get("SECRET_API_KEY")

#send API access request 
resolution = "NUTS3"
region = "DEA29"
type = "data"

request_url = f"http://data.localised-project.eu/api/v1/{resolution}/?api_key={SECRET_API_KEY}&region={region}&type={type}"
response = requests.get(request_url)

#get the json response 
response_json = response.json()

#save the entire json response in a json file 
with open('data.json', 'w') as f:
    json.dump(response_json, f)

#alternatively, save only the regional data (region_data) as a .csv file 
data_df = json_normalize(response_json.get('regions')[0].get('region_data'))
data_df.to_csv('region_data.csv')