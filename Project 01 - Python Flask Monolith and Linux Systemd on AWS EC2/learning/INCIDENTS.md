# Incident Post-Mortem & Troubleshooting Log: Project 01

This document logs real and simulated SRE failure drills conducted during the lifecycle of Project 01.

---

## Incident #01: Unhandled Fatal Process Crash & Systemd Auto-Recovery Drill
* **Date & Severity:** 2026-11-02 | Severity: **Sev-2 (Major Availability Risk)**
* **Component Affected:** Python Flask Application (`app.py`), Linux `systemd` daemon
* **Symptoms:** 
  * Application becomes immediately unresponsive on port 80.
  * Injected via the SRE failure drill endpoint `POST /api/debug/crash`.
* **Root Cause:**
  * An unhandled exception or abrupt process termination (`sys.exit(1)`) triggered a sudden exit.
* **Investigation (`journalctl` output):**
  ```text
  $ journalctl -u skills-tracker.service -n 20 --no-pager
  Nov 02 15:00:10 ubuntu skills-tracker[14201]: WARNING:app:DELIBERATE CRASH TRIGGERED: Terminating process with exit code 1 to test systemd restart.
  Nov 02 15:00:10 ubuntu systemd[1]: skills-tracker.service: Main process exited, code=exited, status=1/FAILURE
  Nov 02 15:00:10 ubuntu systemd[1]: skills-tracker.service: Failed with result 'exit-code'.
  Nov 02 15:00:15 ubuntu systemd[1]: skills-tracker.service: Scheduled restart job, restart counter is at 1.
  Nov 02 15:00:15 ubuntu systemd[1]: Starting SRE Skills Tracker - Python Flask Web Monolith...
  Nov 02 15:00:16 ubuntu skills-tracker[14250]:  * Running on all addresses (0.0.0.0)
  Nov 02 15:00:16 ubuntu skills-tracker[14250]:  * Running on http://127.0.0.1:80
  Nov 02 15:00:16 ubuntu systemd[1]: Started SRE Skills Tracker - Python Flask Web Monolith.
  ```
* **Mitigation / Fix:**
  * In `/etc/systemd/system/skills-tracker.service`, the directive `Restart=always` and `RestartSec=5s` instructed systemd to monitor the PID and automatically respawn a clean process 5 seconds after the crash.
* **Prevention / Lessons Learned:**
  * Never launch long-running web servers in detached terminal screens or background shell jobs (`python app.py &`).
  * Systemd's `AmbientCapabilities=CAP_NET_BIND_SERVICE` allows non-root users (`ubuntu`) to bind to privileged port 80 safely while preserving automatic supervision.

---

## Incident #02: Inbound Security Group Misconfiguration (Connection Timed Out)
* **Date & Severity:** 2026-11-02 | Severity: **Sev-1 (Complete Outage)**
* **Component Affected:** AWS Security Group (`aws_security_group.web_sg`)
* **Symptoms:**
  * Clients cannot reach the web dashboard. Running `curl -v http://<ec2-ip>` hangs for over 60 seconds before terminating with:
    `curl: (28) Failed to connect to 54.210.xx.xx port 80 after 60000 ms: Couldn't connect to server`
* **Root Cause Analysis (Connection Timed Out vs Connection Refused):**
  * **Connection Refused:** Packets reached the host OS, but no process was listening on the socket (kernel sent TCP RST).
  * **Connection Timed Out:** Packets were silently dropped at the cloud boundary before reaching the virtual machine. The inbound HTTP (port 80) rule had been omitted from the AWS Security Group.
* **Mitigation / Fix:**
  * Updated `terraform/main.tf` to explicitly declare the ingress block for TCP port 80:
    ```hcl
    ingress {
      description = "Allow HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    ```
  * Executed `terraform apply` to push the security group update without restarting the EC2 instance.
* **Prevention / Lessons Learned:**
  * Security Groups in AWS are **stateful** (inbound traffic automatically allows outbound return packets).
  * Always verify both AWS Security Groups (instance-level firewall) and local Linux OS firewalls (`ufw`) when diagnosing connectivity timeouts.
