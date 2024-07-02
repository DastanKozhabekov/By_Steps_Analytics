import traceback
import requests
import json
import time
from jsonschema import validate, ValidationError

headers = {
    'Authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE2OTgxLCJpc3MiOiJodHRwczovL2x'
                     'vZ2luLmNybS5hY3NvbHV0aW9ucy5haS9hcGkvdjIvdXNlcnMvYXV0aCIsImlhdCI6MTcxOTczMDQ1OSwiZXhw'
                     'IjoxNzUxMjY2NDU5LCJuYmYiOjE3MTk3MzA0NTksImp0aSI6Im9kbGhxck50eVF4VnhNcjAifQ.zsG-lBcMn1s'
                     'T0gYb8FbB2c2Us3Srrb4b5sNIEGjNYfI'
}
session = requests.Session()
all_data = []
# СМЕНИ ID КОМПАНИИ
company_id = 6305
# JSON schema for validation
schema = {
    "type": "object",
    "properties": {
        "current_page": {"type": "integer"},
        "total": {"type": "integer"},
        "per_page": {"type": "string"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "client_name": {"type": "string"},
                    "key": {"type": "string"},
                    "phone": {"type": "string"},
                    "created_at": {"type": "string"},
                    "segment_title": {"type": "string"},
                    "info": {
                        "type": "object",
                        "properties": {
                            "rfm_segment": {"type": "string"}
                        }
                    },
                    "age": {"type": ["null", "integer"]},
                    "sex": {"type": "string"},
                    "race": {"type": "integer"},
                    "city_id": {"type": ["null", "integer"]},
                    "communication": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title_robot": {"type": "string"},
                                "call_id": {"type": "string"},
                                "billing_time": {"type": "string"},
                                "record_link": {"type": "string"},
                                "status": {"type": "string"},
                                "call_type": {"type": "string"},
                                "dialogs": {
                                    "type": ["null", "array"],
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "text": {"type": "string"},
                                            "position": {"type": "string"}
                                        }
                                    }
                                },
                                "created_at": {"type": "string"},
                                "type": {"type": "string"},
                                "type_robot": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    },
    "required": ["current_page", "total", "per_page", "data"]
}

start_time_perf = time.perf_counter()
try:
    '''
    ЕСЛИ НУЖНО БОЛЬШЕ ТО МЕНЯЕМ 10 НА 20 
    '''
    for i in range(1, 10):
        host = f'https://back.crm.acsolutions.ai/api/v2/campaigns/get_details_analytic/{company_id}?get_type=all&phone=&key=&page={i}&per_page=200'
        response = session.get(host, headers=headers)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            traceback.print_exc()
            break

        data = response.json()

        # Validate the JSON response against the schema
        try:
            validate(instance=data, schema=schema)
            all_data.extend(data['data'])
        except ValidationError as ve:
            print(f"JSON validation error: {ve.message}")
            continue

    with open('json/data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False)

    end_time_perf = time.perf_counter()
    elapsed_time_perf = end_time_perf - start_time_perf
    print(f"Elapsed time using time.perf_counter(): {elapsed_time_perf:.6f} seconds")

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()