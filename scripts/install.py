Here's the `install` function converted to Python:

```python
def install():
    if not os.path.isfile(CLIENT_SCRIPT):
        print(f"{SIGNATURE}: Installing symbol service client...")
        CLIENT_FILE = "SymbolServiceClient.zip"
        CLIENT_URL = f"https://mobileagent.downloads.dynatrace.com/ios/${CLIENT_VERSION}/dynatrace-mobile-agent-ios-${CLIENT_VERSION}.zip"
        fetch_artifact("Dynatrace Symbol Client", CLIENT_FILE, CLIENT_URL)
        print("Unpacking Dynatrace Symbol Client")
        os.makedirs(f"build/Dynatrace/${CLIENT_VERSION}", exist_ok=True)
        shutil.unpack_archive(f"build/{CLIENT_FILE}", f"build/Dynatrace/${CLIENT_VERSION}")
    
    # We always do this part, since upgrading Xcode will break it.
    select_xcode()
    LLDB_FRAMEWORK = os.popen(f"echo ${DEVELOPER_DIR} | sed 's/Developer/SharedFrameworks/LLDB.framework/'").read().strip()
    TARGET_SOFTLINK = os.path.dirname(CLIENT_SCRIPT) + "/LLDB.framework"
    print(f"Soft-Linking LLDB Framework - {LLDB_FRAMEWORK} to {TARGET_SOFTLINK}")
    os.symlink(LLDB_FRAMEWORK, TARGET_SOFTLINK)

# Note: This function assumes the following variables are defined:
# SIGNATURE, CLIENT_SCRIPT, CLIENT_VERSION, DEVELOPER_DIR
# It also assumes the fetch_artifact and select_xcode functions are defined
```

This Python version of the `install` function does the following:

1. Checks if the client script exists.
2. If not, it downloads and unpacks the Dynatrace Symbol Client.
3. Calls the `select_xcode` function (which we converted earlier).
4. Sets up a soft link for the LLDB framework.

To use this function, you'll need to:
- Import necessary modules (os, shutil)
- Define the global variables (SIGNATURE, CLIENT_SCRIPT, CLIENT_VERSION, DEVELOPER_DIR)
- Implement the `fetch_artifact` function
- Ensure the `select_xcode` function is available

Would you like me to explain any part of this code in more detail?​​​​​​​​​​​​​​​​