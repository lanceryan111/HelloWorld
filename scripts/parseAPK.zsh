#!/bin/zsh

# Function to extract package name, versionCode, and versionName from an APK file
extract_apk_info() {
    # Check if the correct number of arguments is provided
    if [ "$#" -ne 1 ]; then
        echo "Usage: $0 path_to_apk"
        return 1
    fi

    APK_FILE=$1

    # Check if the APK file exists
    if [ ! -f "$APK_FILE" ]; then
        echo "File not found: $APK_FILE"
        return 1
    fi

    # Extract and convert AndroidManifest.xml to human-readable format
    MANIFEST=$(unzip -p "$APK_FILE" AndroidManifest.xml | xmllint --format - 2>/dev/null)

    # Extract package name using grep and sed
    PACKAGE_NAME=$(echo "$MANIFEST" | grep -oP '(?<=package=")[^"]+')
    # Extract versionCode and versionName using grep and sed
    VERSION_CODE=$(echo "$MANIFEST" | grep -oP 'android:versionCode="\K[0-9]+')
    VERSION_NAME=$(echo "$MANIFEST" | grep -oP 'android:versionName="\K[^"]+')

    # Print the extracted values
    echo "Package Name: $PACKAGE_NAME"
    echo "Version Code: $VERSION_CODE"
    echo "Version Name: $VERSION_NAME"

    return 0
}

# Call the function with the provided argument
extract_apk_info "$1"
