# SRE Interview Prep & Quiz: Project 01

### Q1: What happens under the hood when a Python process managed by systemd crashes with a Segmentation Fault or unhandled Exception?
**Answer:** The Linux kernel terminates the process and sends a SIGCHLD signal to parent process #1 (systemd). If Restart=always or Restart=on-failure is set in the [Service] block of the .service file, systemd waits for RestartSec (e.g. 5 seconds) and calls execve() to spawn a fresh instance. It logs the crash event and exit code into journald, accessible via journalctl -u skills-tracker.service.

### Q2: Why should you avoid storing SQLite on a shared network drive (NFS/EFS) in production?
**Answer:** SQLite relies on POSIX advisory locks on the local filesystem. Network filesystems (like NFS or AWS EFS) often have broken, buggy, or high-latency lock implementations, which can lead to database corruption or 'database is locked' runtime exceptions under concurrent writes.

### Q3: What is Configuration Drift and how does Terraform detect it?
**Answer:** Configuration drift occurs when an engineer manually changes infrastructure (e.g., adding an inbound rule in the AWS console) outside of Terraform. When terraform plan is executed, Terraform queries the cloud provider API to refresh its memory of real-world state, compares it against the local state file and your .tf code, and calculates the exact diff required to return infrastructure to the declared state.

### Q4: What is the difference between a Security Group and a Network ACL (NACL) in AWS?
**Answer:** Security Group is a stateful virtual firewall operating at the instance/ENI level. If inbound traffic is allowed, outbound return traffic is automatically permitted regardless of outbound rules. Network ACL (NACL) is a stateless firewall operating at the subnet boundary. Both inbound and outbound rules must explicitly permit the traffic packets.

