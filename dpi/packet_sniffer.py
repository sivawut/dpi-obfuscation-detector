# Captures network packets using scapy
from scapy.all import sniff, TCP, Raw, IP
import re
import sqlite3
import sys

DEBUG = "--debug" in sys.argv

# Connect to SQLite DB
conn = sqlite3.connect("data/db.sqlite3")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS urls (url TEXT, src_ip TEXT, timestamp TEXT)")

url_pattern = re.compile(rb'https?://[\w./?=&%-]+')

def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        if DEBUG:
            print("=== PACKET START ===")
            print(payload)
            print("=== PACKET END ===\n")

        found = url_pattern.findall(payload)
        for url in found:
            url_str = url.decode('utf-8', errors='ignore')
            src_ip = packet[IP].src if packet.haslayer(IP) else "unknown"
            print(f"[+] Detected URL: {url_str}")
            c.execute("INSERT INTO urls VALUES (?, ?, datetime('now'))", (url_str, src_ip))
            conn.commit()

sniff(filter="tcp port 80", prn=process_packet, store=0)

