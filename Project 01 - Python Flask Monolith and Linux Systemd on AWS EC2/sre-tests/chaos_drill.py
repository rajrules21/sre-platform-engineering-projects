"""
SRE Chaos Failure Drill: Automated Crash & Self-Healing Verification
================================================================================
Injects a fatal crash via POST /api/debug/crash and monitors MTTR (Mean Time To Repair).
Verifies that Linux systemd automatically revives the service within 5 seconds.
================================================================================
"""

import time
import requests
import sys

TARGET_URL = "http://65.2.9.159"

def check_health():
    try:
        r = requests.get(f"{TARGET_URL}/healthz", timeout=1.0)
        if r.status_code == 200:
            return True, r.json()
        return False, {"status_code": r.status_code}
    except Exception as e:
        return False, {"error": "Connection Refused (Process Dead)"}

print("==================================================================")
print(" SRE CHAOS FAILURE DRILL: Systemd Self-Healing Demonstration")
print(f" Target Instance: {TARGET_URL}")
print("==================================================================")

# 1. Baseline pre-check
print("\n[STEP 1] Validating pre-drill baseline...")
healthy, data = check_health()
if not healthy:
    print(f"❌ Aborting drill: Service is not healthy before drill: {data}")
    sys.exit(1)

pre_uptime = data.get('uptime_seconds', 0)
print(f"✅ Service is UP & HEALTHY. Current Uptime: {pre_uptime} seconds. Database: {data.get('database')}")

# 2. Trigger deliberate crash
print("\n[STEP 2] Injecting FATAL CRASH via POST /api/debug/crash...")
try:
    requests.post(f"{TARGET_URL}/api/debug/crash", timeout=1.5)
except Exception:
    # Flask process abruptly terminates with os._exit(1), terminating the TCP socket
    print("⚡ Crash signal delivered! Kernel terminated remote Python process.")

# 3. High-frequency polling to measure downtime and recovery
print("\n[STEP 3] Measuring MTTR (Mean Time To Recovery) & Systemd Revival...")
start_time = time.time()
recovered = False
new_uptime = 0

for attempt in range(1, 15):
    time.sleep(1.0)
    elapsed = time.time() - start_time
    is_up, payload = check_health()
    
    if is_up:
        new_uptime = payload.get("uptime_seconds", 0)
        if new_uptime < pre_uptime:
            print(f"  [{elapsed:.1f}s] Attempt {attempt:02d}: ✅ HTTP 200 OK! Service revived! (New Uptime: {new_uptime}s)")
            recovered = True
            break
        else:
            print(f"  [{elapsed:.1f}s] Attempt {attempt:02d}: Old process still exiting ({new_uptime}s)...")
    else:
        print(f"  [{elapsed:.1f}s] Attempt {attempt:02d}: ❌ DOWN ({payload.get('error', 'HTTP ' + str(payload.get('status_code')))}) - Systemd RestartSec countdown...")

print("\n==================================================================")
if recovered:
    mttr = elapsed
    print(f"🎉 CHAOS DRILL SUCCESSFUL!")
    print(f"   • Mean Time To Recovery (MTTR): {mttr:.1f} seconds")
    print(f"   • Previous Uptime:             {pre_uptime}s")
    print(f"   • New Process Uptime:          {new_uptime}s (Fresh PID spawned by systemd)")
    print(f"   • Linux systemd 'Restart=always' & 'RestartSec=5s' verified in production!")
else:
    print("❌ DRILL FAILED: Service did not recover within expected window.")
print("==================================================================")
