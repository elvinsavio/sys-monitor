from sys_calls.network import get_session_data
import time

print("Checking network session data...")
data = get_session_data()
if data:
    print(f"Interface: {data.interface}")
    print(f"RX: {data.rx_mb} MB")
    print(f"TX: {data.tx_mb} MB")
else:
    print("No active network interface found by auto-detection.")
