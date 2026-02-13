
import requests
import socket
import sys

def check_dns(hostname):
    print(f"Testing DNS resolution for {hostname}...")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolved: {hostname} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS Failed: {e}")
        return False

def check_http(url):
    print(f"Testing HTTPS connection to {url}...")
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ Connection Successful. Status Code: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Failed: {e}")
        return False

if __name__ == "__main__":
    print("--- Connectivity Test ---")
    
    # 1. Test Google OAuth (Critical for Firebase)
    if not check_dns("oauth2.googleapis.com"):
        sys.exit(1)
    
    if not check_http("https://oauth2.googleapis.com/token"):
        sys.exit(1)
        
    print("\n--- Network seems OK ---")
