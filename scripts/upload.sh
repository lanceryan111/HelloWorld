#!/bin/bash

# Server URL
server_url="http://example.com/upload"

# Folder containing files to upload
folder="/path/to/folder"

# Iterate over files in the folder
for file in "$folder"/*; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Extract filename
        filename=$(basename "$file")
        
        # Upload the file using cURL
        echo "Uploading $filename..."
        curl -F "file=@$file" "$server_url"
        
        # Check cURL exit status
        if [ $? -eq 0 ]; then
            echo "Upload successful: $filename"
        else
            echo "Upload failed: $filename"
        fi
    fi
done
