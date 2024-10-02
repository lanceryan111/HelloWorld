import subprocess
import sys

ACF2ID = subprocess.getoutput("whoami")
KEYCHAIN_PASSWORD_NAME = "YourKeychainPasswordName"  # Replace with the actual keychain password name

def read_api_token():
    try:
        # Try to retrieve the API token from the keychain
        result = subprocess.check_output(
            ["security", "find-generic-password", "-a", ACF2ID, "-s", KEYCHAIN_PASSWORD_NAME, "-w"],
            universal_newlines=True
        ).strip()
        
        if not result:
            raise ValueError("No API token found.")
        
        print(f"API token found: {result}")
        return result

    except subprocess.CalledProcessError:
        # Prompt for Dynatrace PROD API token if not found
        api_token = input("Enter your Dynatrace PROD API Token: ").strip()
        if not api_token:
            print("No API token entered – exiting.")
            sys.exit(1)
        
        # Store the token in the keychain for future use
        print("Writing API token to keychain for subsequent runs...")
        subprocess.run(
            ["security", "add-generic-password", "-a", ACF2ID, "-s", KEYCHAIN_PASSWORD_NAME, "-w", api_token, "-j", "Used by TD development scripts when accessing Dynatrace API"],
            check=True
        )
        
        return api_token