# Detects obfuscated URLs
import re
import base64
import urllib.parse

SHORTENERS = ['bit.ly', 'tinyurl', 'goo.gl']

def is_obfuscated(url: str) -> bool:
    if any(short in url for short in SHORTENERS):
        return True
    try:
        if re.search(r'%[0-9A-Fa-f]{2}', url):
            return True
        decoded = base64.b64decode(url).decode('utf-8')
        if 'http' in decoded:
            return True
    except:
        pass
    if 'url=' in url and 'http' in urllib.parse.unquote(url):
        return True
    return False
