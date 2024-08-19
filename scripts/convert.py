Here's the `publish_to_dynatrace` function converted to Python:

```python
def publish_to_dynatrace():
    print(f"{SIGNATURE}: Publishing {DYNATRACE_SYMBOL_FILE} to Dynatrace ({DYNATRACE_URL})")
    
    DYNATRACE_FULL_URL = f"{DYNATRACE_URL}/api/config/v1/symfiles/{DYNATRACE_APPLICATION_ID}/{APP_PACKAGE_NAME}/IOS/{RELEASE_TRAIN}/{APP_VERSION}"
    
    read_api_token()
    print(f"DYNATRACE_FULL_URL IS: {DYNATRACE_FULL_URL}")
    
    curl_command = [
        "curl", "-X", "PUT",
        DYNATRACE_FULL_URL,
        "-H", f"Authorization: Api-Token {API_TOKEN}",
        "-H", "Content-Type: application/zip",
        "--data-binary", f"@build/{DYNATRACE_SYMBOL_FILE}"
    ]
    
    process = subprocess.Popen(curl_command, stderr=subprocess.PIPE, universal_newlines=True)
    stderr = process.communicate()[1]
    
    handle_curl_returncode(process.returncode)
```

Would you like me to explain or break down this code?​​​​​​​​​​​​​​​​