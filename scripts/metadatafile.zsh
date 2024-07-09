#!/bin/bash

# Configuration
NEXUS_URL="https://your-nexus-url.com"
REPOSITORY="your-repository"
GROUP_ID="com.example"
ARTIFACT_ID="your-artifact"
VERSION="latest"
USERNAME="your-username"
PASSWORD="your-password"

# Fetch JSON file from Nexus3
JSON_FILE=$(curl -s -u "$USERNAME:$PASSWORD" "$NEXUS_URL/service/rest/v1/search/assets?repository=$REPOSITORY&group=$GROUP_ID&name=$ARTIFACT_ID&version=$VERSION")

# Parse JSON and extract versionName and versionCode
VERSION_NAME=$(echo "$JSON_FILE" | grep -oP '"version"\s*:\s*"\K[^"]*')
VERSION_CODE=$(echo "$JSON_FILE" | grep -oP '"extension"\s*:\s*"\K[^"]*')

# Check if values are extracted successfully
if [ -z "$VERSION_NAME" ] || [ -z "$VERSION_CODE" ]; then
    echo "Error: Failed to extract version information from JSON"
    exit 1
fi

# Print extracted values
echo "Version Name: $VERSION_NAME"
echo "Version Code: $VERSION_CODE"

# Use the extracted values for Dynatrace API call
# Replace this with your actual Dynatrace API call
DYNATRACE_API_URL="https://your-dynatrace-url.com/api/v2/someEndpoint"
DYNATRACE_API_TOKEN="your-dynatrace-api-token"

curl -X POST "$DYNATRACE_API_URL" \
     -H "Authorization: Api-Token $DYNATRACE_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{
         \"versionName\": \"$VERSION_NAME\",
         \"versionCode\": \"$VERSION_CODE\"
     }"
