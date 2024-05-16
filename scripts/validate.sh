#!/bin/bash

# Function to validate a file against its SHA1 checksum
validate_file() {
    local file="$1"
    local sha1_file="$2"
    
    # Calculate the SHA1 checksum of the file
    local calculated_sha1=$(sha1sum "$file" | awk '{print $1}')
    
    # Read the expected SHA1 checksum from the SHA1 file
    local expected_sha1=$(cat "$sha1_file")
    
    # Compare the calculated and expected SHA1 checksums
    if [ "$calculated_sha1" == "$expected_sha1" ]; then
        echo "Validation successful: $file"
    else
        echo "Validation failed: $file"
    fi
}

# Main script

# Directory containing files and their SHA1 checksum files
folder="path/to/folder"

# Iterate over files in the folder
for file in "$folder"/*; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Check if a corresponding SHA1 checksum file exists
        sha1_file="${file}.sha1"
        if [ -f "$sha1_file" ]; then
            # Validate the file against its SHA1 checksum
            validate_file "$file" "$sha1_file"
        else
            echo "SHA1 checksum file not found for: $file"
        fi
    fi
done
