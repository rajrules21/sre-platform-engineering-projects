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

---

## Incident #03: Cloud-Init vs SSH Race Condition & Ephemeral Runner Resource Duplication
* **Date & Severity:** 2026-11-13 | Severity: **Sev-2 (Deployment Failure & Cloud Resource Duplication)**
* **Components Affected:** GitHub Actions CD Runner (`project-01.yml`), Ubuntu Cloud-Init (`user_data`), Linux Package Manager (`apt`), Terraform Local State (`terraform.tfstate`).
* **Symptoms:**
  * The GitHub Actions CD pipeline failed at the deployment step with `Process completed with exit code 7` (`curl: (7) Failed to connect to host: Connection refused`).
  * Inspection of the deployment logs revealed: `ModuleNotFoundError: No module named 'flask'`.
  * The AWS EC2 instance was left running in AWS, but the application was dead on port 80.
  * Re-triggering the pipeline created a **second duplicate EC2 instance**, doubling running compute costs while leaving the first instance orphaned.
* **Root Cause Analysis:**
  1. **The Cloud-Init vs SSH Race Condition:** When AWS provisions an EC2 instance, SSH port 22 becomes reachable within 15–20 seconds. The GitHub Actions SSH action connected immediately and began executing deployment commands (`python3 -m venv`). Simultaneously, Linux `cloud-init` was running `apt-get install -y python3-pip python3-venv` in the background and holding the dpkg lock (`/var/lib/dpkg/lock-frontend`). Because the deployment script raced ahead before `python3-venv` had finished unpacking, it created a broken virtual environment lacking `pip` and dependencies. Flask failed to launch, leaving port 80 closed.
  2. **Ephemeral Runner State Loss:** In GitHub Actions, each pipeline run boots on a brand-new, isolated virtual machine. Because Terraform had not yet been configured with a remote backend (Amazon S3 + DynamoDB state locking), the `terraform.tfstate` file was destroyed when the first runner exited. On the next push, Terraform checked its blank local state, concluded zero infrastructure existed in AWS, and provisioned a second duplicate EC2 instance.
* **Mitigation / Fix:**
  1. **OS Bootstrap Synchronization:** Injected `cloud-init status --wait` at the beginning of the SSH deployment script. This forces the deployment pipeline to block and poll until the OS bootstrap script has completed 100% of its package installations before executing application setup.
  2. **Orphan Cleanup:** Queried `aws ec2 describe-instances` via AWS CLI and terminated the zombie instance (`i-0ec11981e45eaed61`).
  3. **Architectural Gating:** Standardized that all future CI/CD pipelines (starting from Project 02) must use remote state storage with distributed locking to prevent duplicate cloud provisioning.
* **Prevention / Lessons Learned:**
  * An open SSH port only signals that `sshd` is running, not that the operating system has finished provisioning.
  * CI/CD pipelines deploying directly to VMs must always synchronize with the OS bootstrap manager (`cloud-init status --wait`).
  * Running Terraform in ephemeral CI runners with local state is an operational anti-pattern that leads to phantom cloud billing and resource drift.

