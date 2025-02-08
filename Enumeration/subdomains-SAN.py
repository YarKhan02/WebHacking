import subprocess
import re
import sys

"""
Subdomain Enumeration using Subject Alternative Name (SAN)  
When a website uses an SSL/TLS certificate it often includes SAN field. 
This field contains the list of all domains and subdomains for which the certificate is valid.
"""

def get_ssl_san(domain):
    try:
        # Run OpenSSL command to fetch SSL certificate details
        cmd = f"true | openssl s_client -connect {domain}:443 2>/dev/null | openssl x509 -noout -text"
        output = subprocess.check_output(cmd, shell=True, text=True)

        # Extract DNS names using regex
        dns_names = re.findall(r"DNS:([a-zA-Z0-9.-]+)", output)

        if dns_names:
            print(f"\n🔹 Subject Alternative Names for {domain}:")
            for name in dns_names:
                print(f"- {name}")
        else:
            print(f"No DNS names found in the SSL certificate for {domain}")

    except subprocess.CalledProcessError:
        print(f"Error retrieving SSL certificate for {domain}")

# Ensure domain is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python3 script.py <domain>")
    sys.exit(1)

# Get domain from command-line argument
target_domain = sys.argv[1]
get_ssl_san(target_domain)
