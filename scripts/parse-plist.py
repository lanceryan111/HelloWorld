Here's the `parse_plist_file` function converted to Python:

```python
import os
import subprocess

def parse_plist_file():
    if not os.path.isfile(f"build/{SOURCE_SYMBOL_FILE}"):
        print(f"Missing file - build/{SOURCE_SYMBOL_FILE}.")
        exit(1)
    else:
        # Extract APP_VERSION_NAME
        cmd = f"unzip -p build/{SOURCE_SYMBOL_FILE} AccountManager.app.dSYM/Contents/Info.plist | grep -A 1 CFBundleVersion | grep string | sed 's/.*<string>//;s/<\\/string>.*//'"
        APP_VERSION_NAME = subprocess.check_output(cmd, shell=True).decode().strip()

        # Extract APP_PACKAGE_NAME
        cmd = f"unzip -p build/{SOURCE_SYMBOL_FILE} AccountManager.app.dSYM/Contents/Info.plist | grep -A 1 CFBundleIdentifier | grep string | sed 's/.*<string>//;s/<\\/string>.*//'"
        APP_PACKAGE_NAME = subprocess.check_output(cmd, shell=True).decode().strip()

        # Dynatrace rejects package names with the following prefix, so the following trims it off if found
        if APP_PACKAGE_NAME.startswith("com.apple.xcode.dsym."):
            APP_PACKAGE_NAME = APP_PACKAGE_NAME.replace("com.apple.xcode.dsym.", "", 1)

    return APP_VERSION_NAME, APP_PACKAGE_NAME

# Note: This function assumes the SOURCE_SYMBOL_FILE variable is defined globally
```

This Python version of the `parse_plist_file` function does the following:

1. Checks if the source symbol file exists.
2. If it doesn't exist, it prints an error message and exits.
3. If it exists, it extracts the `APP_VERSION_NAME` and `APP_PACKAGE_NAME` from the plist file inside the .dSYM package.
4. It removes the "com.apple.xcode.dsym." prefix from the package name if it exists.
5. Returns both `APP_VERSION_NAME` and `APP_PACKAGE_NAME`.

To use this function, you'll need to:
- Import necessary modules (os, subprocess)
- Define the global variable SOURCE_SYMBOL_FILE

The function uses `subprocess.check_output` to run shell commands, which is similar to using `unzip` and `grep` in the original script. It also uses Python's string methods for trimming the package name prefix if needed.

Would you like me to explain any part of this code in more detail?​​​​​​​​​​​​​​​​