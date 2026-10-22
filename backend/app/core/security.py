import ipaddress
import socket
from urllib.parse import urlparse

FORBIDDEN_HOSTS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "169.254.169.254", # AWS / Cloud metadata
    "metadata.google.internal",
}

def is_safe_url(url: str) -> bool:
    """
    Validate that URL is an HTTP/HTTPS scheme and does not target localhost,
    private IP spaces, link-local, or cloud metadata endpoints (SSRF protection).
    Allows standard NAT64 (RFC 6052 64:ff9b::/96) global translation.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
            
        hostname = parsed.hostname
        if not hostname:
            return False
            
        hostname_lower = hostname.lower()
        if hostname_lower in FORBIDDEN_HOSTS:
            return False
            
        # Resolve hostname to IP addresses and check if private
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            for item in addr_info:
                ip_str = item[4][0]
                ip_obj = ipaddress.ip_address(ip_str)

                # Skip checking is_reserved if it's NAT64 well-known prefix 64:ff9b::/96
                if isinstance(ip_obj, ipaddress.IPv6Address) and str(ip_obj).startswith("64:ff9b:"):
                    continue

                if (
                    ip_obj.is_private
                    or ip_obj.is_loopback
                    or ip_obj.is_link_local
                    or ip_obj.is_multicast
                ):
                    return False
        except socket.gaierror:
            pass

        return True
    except Exception:
        return False
