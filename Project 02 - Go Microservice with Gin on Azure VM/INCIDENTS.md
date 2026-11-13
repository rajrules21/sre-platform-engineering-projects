# Incident Post-Mortem & Troubleshooting Log

This document serves as your real-world SRE incident journal. Whenever a build fails, a container crashes, a Terraform lock times out, or a cloud permission is denied, log it here.
Hiring managers value engineers who can systematically diagnose, mitigate, and prevent failures.

---

## Template for New Incidents

### Incident #{ID}: [Brief Title - e.g., Terraform State Lock Timeout]
* **Date & Severity:** YYYY-MM-DD | Severity: [Sev-1 (Critical) / Sev-2 (Major) / Sev-3 (Minor)]
* **Component Affected:** [e.g. AWS EC2, GitHub Actions, Redis, Systemd]
* **Symptoms:** What failed? What exact error message appeared in the terminal or logs?
* **Root Cause:** Why did it happen? (e.g. Missing AWS IAM permission, port 80 already in use, invalid YAML indentation).
* **Mitigation / Fix:** What command or code change resolved the issue?
* **Prevention / Lessons Learned:** What rule or check can we add so this never happens again?

---

## Logged Incidents
*(Log your learning incidents below as you build and debug)*
