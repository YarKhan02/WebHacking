"""
Subdomain enumeration subdomains from content security policy
Allows administrator to specify which domains and subdomains are allowed to load contents 
such as scripts, frame sources, and image sources, so on
"""

import requests
import re
import argparse

def get_csp_headers(url):
    response = requests.get(url)
    
    # Extract headers related to Content Security Policy (CSP)
    csp_headers = [
        v for k, v in response.headers.items()
        if re.search(r'content-security-policy|csp', k, re.IGNORECASE)
    ]
    
    domains = set()
    for header in csp_headers:
        # Replace spaces with newlines, extract domains, remove trailing semicolons
        words = header.replace(" ", "\n").split("\n")
        for word in words:
            if "." in word:  # Ensure it contains a dot (likely a domain)
                clean_word = word.replace(";", "").replace("*.", "")
                domains.add(clean_word)
    
    for domain in sorted(domains):
        print(domain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract CSP domains from a website's headers.")
    parser.add_argument("url", help="Website URL to fetch headers from")
    args = parser.parse_args()
    get_csp_headers(args.url)
