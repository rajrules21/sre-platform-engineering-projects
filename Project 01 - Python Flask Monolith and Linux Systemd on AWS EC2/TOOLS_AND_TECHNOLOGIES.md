# Tools & Technologies: Project 01

| Tool / Technology | Role in Project | Why Chosen? | Industry Alternative | SRE Relevance |
| :--- | :--- | :--- | :--- | :--- |
| **Python (Flask)** | Application Runtime | Minimal microframework with zero magic. Easy to understand HTTP routing and lifecycle. | Django, FastAPI, Express.js | Fast prototyping; widely used for internal SRE automation tools. |
| **SQLite** | Embedded Database | Zero-config, single-file ACID transactional database. No daemon to manage. | PostgreSQL, MySQL | Standard for local state, testing, and embedded tools. |
| **systemd** | OS Service Manager | The standard Linux init system and service manager since 2015. | SysVinit, Upstart, Supervisord | Fundamental Linux SRE skill: process supervision, cgroups, resource limits, auto-recovery. |
| **Terraform (Raw)** | Infrastructure as Code | De facto standard declarative multi-cloud infrastructure tool. | OpenTofu, CloudFormation, Pulumi | Guarantees reproducible, audit-able cloud infrastructure without manual drift. |
| **AWS EC2 & VPC** | Cloud Virtual Compute | Industry benchmark for IaaS (Infrastructure as a Service). | Azure VM, GCP Compute Engine | Foundational cloud primitives that every higher-level service (ECS, EKS) is built on. |
| **GitHub Actions** | CI/CD Engine | Market leader in modern CI/CD, tightly integrated with source control. | GitLab CI, Jenkins, Azure DevOps | Automates testing, linting, and continuous delivery via SSH. |
