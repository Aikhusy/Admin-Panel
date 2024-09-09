import re

# Fungsi untuk memvalidasi IP address
def validate_ip(ip_address):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return ip_pattern.match(ip_address) is not None
