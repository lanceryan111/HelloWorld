#!/bin/bash

# Set variables
SOURCE_KEYCHAIN="/path/to/source/keychain.keychain"
DESTINATION_KEYCHAIN="/path/to/destination/keychain.keychain"
TEMP_FILE="/tmp/keychain_items.txt"

# Ensure both keychains are unlocked
echo "Please enter the password for the source keychain:"
security unlock-keychain "$SOURCE_KEYCHAIN"

echo "Please enter the password for the destination keychain:"
security unlock-keychain "$DESTINATION_KEYCHAIN"

# List all items in the source keychain
security dump-keychain -a "$SOURCE_KEYCHAIN" > "$TEMP_FILE"

# Read through each item and copy it to the destination keychain
while IFS= read -r line
do
    if [[ $line == "keychain: "* ]]; then
        continue
    fi
    
    item_name=$(echo "$line" | awk -F'"' '{print $2}')
    
    # Skip empty item names
    if [ -z "$item_name" ]; then
        continue
    fi
    
    echo "Migrating item: $item_name"
    
    # Export the item from source keychain
    security export -k "$SOURCE_KEYCHAIN" -t all -f pkcs12 -P "" -o /tmp/temp_item.p12 "$item_name"
    
    # Import the item to destination keychain
    security import /tmp/temp_item.p12 -k "$DESTINATION_KEYCHAIN" -t all -f pkcs12 -P ""
    
    # Remove temporary file
    rm /tmp/temp_item.p12
done < "$TEMP_FILE"

# Clean up
rm "$TEMP_FILE"

echo "Migration complete. Please verify that all items were transferred correctly."
