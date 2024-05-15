#!/bin/bash

# Define value1 and value2
value1="example_value1"
value2="example_value2"

# Function to extract download URLs from JSON response using grep, sed, and awk
extract_urls() {
    # Extract lines containing "download_url" and remove surrounding whitespace
    urls=$(echo "$1" | grep -o '"download_url":.*' | sed 's/.*: "\(.*\)".*/\1/')
    # Print each URL on a new line
    echo "$urls"
}

# Main script

# Create a temporary folder using value1 and value2 as its name
temp_folder="./$value1$value2"
mkdir -p "$temp_folder"

# Define API endpoint URL with parameters including value1 and value2
api_url="https://api.example.com/endpoint?param1=$value1&param2=$value2"

# Call the API endpoint using curl with the defined URL and store the JSON response in a variable
api_response=$(curl -s -w "%{http_code}" "$api_url")

# Extract the HTTP status code from the end of the response
http_status=$(echo "${api_response: -3}")

# Check if the HTTP status code is 200 (OK)
if [ "$http_status" -eq 200 ]; then
    # Extract URLs from JSON response
    download_urls=$(extract_urls "${api_response:0:-3}")

    # Change to the temporary folder directory
    cd "$temp_folder"

    # Iterate over each download URL and download the file
    for url in $download_urls; do
        filename=$(basename "$url")
        echo "Downloading $filename..."
        curl -O "$url"
        if [ $? -ne 0 ]; then
            echo "Failed to download $filename"
        else
            echo "Downloaded $filename"
        fi
    done

    # Return to the original directory
    cd -
else
    echo "Failed to fetch data from the API endpoint. HTTP status code: $http_status"
fi
