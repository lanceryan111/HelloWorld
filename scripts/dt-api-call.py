Here's a Python function to upload symbol files to the Dynatrace API using an API key and version information. This example assumes you have the requests library installed.

1. Install the `requests` library if you haven't already:

```sh
pip install requests
```

2. Use the following Python function to upload symbol files:

```python
import requests

def upload_symbol_file(api_key, version_info, file_path):
    url = "https://YOUR_ENVIRONMENT_ID.live.dynatrace.com/api/v2/symbols"
    
    headers = {
        'Authorization': f'Api-Token {api_key}',
        'Content-Type': 'multipart/form-data'
    }
    
    # Metadata for the symbol file
    metadata = {
        'version': version_info
    }
    
    # The file to be uploaded
    files = {
        'file': open(file_path, 'rb'),
        'metadata': (None, json.dumps(metadata), 'application/json')
    }
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage
api_key = 'YOUR_API_KEY'
version_info = '1.0.0'
file_path = 'path/to/your/symbol/file.sym'

try:
    result = upload_symbol_file(api_key, version_info, file_path)
    print("Upload successful:", result)
except Exception as e:
    print("Error during upload:", e)
```

### Explanation:
1. **URL**: Replace `YOUR_ENVIRONMENT_ID` with your actual Dynatrace environment ID.
2. **Headers**: The authorization header includes the API key.
3. **Files**: The `files` dictionary includes the symbol file and its metadata.
4. **Request**: A POST request is made to the Dynatrace API to upload the symbol file.
5. **Response Handling**: If the upload is successful, the function returns the JSON response. If not, it raises an error.

Ensure you replace the placeholder values (`YOUR_API_KEY`, `YOUR_ENVIRONMENT_ID`, and `path/to/your/symbol/file.sym`) with your actual data.