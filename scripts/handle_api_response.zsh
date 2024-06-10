#!/bin/bash

# Function to handle API requests
function handle_api_request() {
    local url=$1
    local response_file=$(mktemp)
    local http_code

    # Make the API request
    http_code=$(curl -s -w "%{http_code}" -o "$response_file" "$url")

    # Read the response message
    local response_message=$(cat "$response_file")
    rm -f "$response_file"

    # Handle different HTTP response codes
    case "$http_code" in
        200)
            echo "Success: $response_message"
            ;;
        400)
            echo "Bad Request: $response_message"
            ;;
        401)
            echo "Unauthorized: $response_message"
            ;;
        403)
            echo "Forbidden: $response_message"
            ;;
        404)
            echo "Not Found: $response_message"
            ;;
        500)
            echo "Internal Server Error: $response_message"
            ;;
        502)
            echo "Bad Gateway: $response_message"
            ;;
        503)
            echo "Service Unavailable: $response_message"
            ;;
        504)
            echo "Gateway Timeout: $response_message"
            ;;
        *)
            echo "Unexpected response code ($http_code): $response_message"
            ;;
    esac
}

# Example usage
handle_api_request "https://api.example.com/endpoint"
