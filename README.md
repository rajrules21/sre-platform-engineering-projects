# SRE & Platform Engineering Portfolio

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions_%7C_ADO_%7C_GitLab_CI-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Multi-Cloud](https://img.shields.io/badge/Cloud-AWS_%7C_Azure_%7C_GCP-orange?style=flat-square&logo=amazonwebservices&logoColor=white)
![IaC](https://img.shields.io/badge/IaC-Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes_%7C_Argo_CD-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Languages](https://img.shields.io/badge/Languages-Python_%7C_Golang-3776AB?style=flat-square&logo=python&logoColor=white)

Welcome to the **Site Reliability & Platform Engineering Portfolio**. This repository documents an end-to-end, production-grade engineering progression spanning monolithic web systems, containerized microservices, distributed asynchronous architectures, Kubernetes orchestration, GitOps automation, and production observability across the three major hyperscale clouds (**AWS**, **Azure**, and **Google Cloud Platform**).

---

## 🗺️ The 12-Project Core Matrix & Roadmap

The curriculum is structured across five progressive phases, transitioning from foundational operating system fundamentals up to enterprise-scale distributed platforms.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           THE 12-WEEK SRE PROGRESSION                            │
└──────────────────────────────────────────────────────────────────────────────────┘
  [Phase 1] Linux, Web Fundamentals & Cloud VMs with Terraform (Projects 01 - 03)
      │
  [Phase 2] Managed Serverless Containers Across 3 Clouds (Projects 04 - 06)
      │
  [Phase 3] Caching & Asynchronous Distributed Systems (Projects 07 - 08)
      │
  [Phase 4] Kubernetes Core Fundamentals & Application Packaging (Projects 09 - 10)
      │
  [Phase 5] Declarative GitOps & Production SRE Observability (Projects 11 - 12)
```

---

### Project Overview Table

| # | Project Name | Cloud | App / Language | IaC / Tooling | CI/CD Platform | Core SRE Focus | Status |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| **01** | [**Python Flask Monolith & Linux Systemd on AWS EC2**](./Project%2001%20-%20Python%20Flask%20Monolith%20and%20Linux%20Systemd%20on%20AWS%20EC2) | **AWS** | Python 3.12 (Flask) + SQLite | Terraform (Raw `main.tf`) | GitHub Actions | Linux `systemd` process supervision, `CAP_NET_BIND_SERVICE`, synthetic probes, chaos failure drills, Locust load testing. | **Completed** ✅ |
| **02** | **Go Microservice with Gin on Azure VM** | **Azure** | Golang (Gin) + JSON Store | Terraform (Remote State + Blob Lock) | Azure DevOps (ADO) | Go compilation, binary deployments, distributed state locking in cloud storage. | *Upcoming* ⏳ |
| **03** | **Modular Terraform & Docker on GCP Compute Engine** | **GCP** | Python (FastAPI) | Reusable Terraform Modules | GitLab CI | Multi-stage non-root Dockerfiles, reusable module patterns, automated OpenAPI contracts. | *Upcoming* ⏳ |
| **04** | **AWS ECS Fargate with GitHub Actions** | **AWS** | Python (FastAPI) | Terraform + AWS ECR / ALB | GitHub Actions | Serverless container orchestration, task definitions, zero-downtime blue/green deployments. | *Upcoming* ⏳ |
| **05** | **Azure Container Apps (ACA) with Golang & Dragonfly** | **Azure** | Golang (Gin) + Dragonfly Cache | Terraform (ACA + VNet integration) | Azure DevOps (ADO) | Serverless microservices, internal private VNet communication, high-performance in-memory caching. | *Upcoming* ⏳ |
| **06** | **GCP Cloud Run with FastAPI & Secret Manager** | **GCP** | Python (FastAPI) | Terraform (Cloud Run + Secret Manager) | GitLab CI | Scale-to-zero economics, cold-start mitigation, enterprise cloud secret injection. | *Upcoming* ⏳ |
| **07** | **Distributed Caching with Redis (Cache-Aside Pattern)** | Multi-Cloud | Python (FastAPI) + Redis | Docker Compose / Terraform | GitHub Actions | Cache-Aside design, TTL policies, cache hit/miss observability, tail latency reduction. | *Upcoming* ⏳ |
| **08** | **Asynchronous Task Processing with RabbitMQ & Celery** | Multi-Cloud | Python + Celery + RabbitMQ | Docker Compose / Terraform | GitHub Actions | Decoupling synchronous HTTP requests, producer-consumer queues, dead-letter exchanges (DLX). | *Upcoming* ⏳ |
| **09** | **Kubernetes Fundamentals on Managed K8s** | **AWS** / Local | Go Gin & Python apps | K8s Manifests (kubectl) | GitHub Actions | Pod lifecycles, Liveness vs Readiness probes, Services (ClusterIP/NodePort/LB), rolling updates. | *Upcoming* ⏳ |
| **10** | **Application Packaging with Helm & Cloud-Native Storage** | Multi-Cloud | Python (FastAPI) + PostgreSQL | Helm (`values.yaml`, templates) | GitHub Actions | Helm chart packaging, dynamic templating, Kubernetes PersistentVolumes (PV/PVC). | *Upcoming* ⏳ |
| **11** | **Declarative GitOps with Argo CD** | Multi-Cloud | Full Microservices Suite | Argo CD + Kubernetes | GitHub Actions + Argo CD | Git as single source of truth, automated cluster drift detection, self-healing continuous delivery. | *Upcoming* ⏳ |
| **12** | **Production Observability with Prometheus & Grafana** | Multi-Cloud | Instrumentd Microservices | Prometheus + Grafana + Alertmanager | GitHub Actions | The Four Golden Signals (Latency, Traffic, Errors, Saturation), OpenMetrics scraping, P95/P99 alerting. | *Upcoming* ⏳ |

---

## 🛠️ Technology Stack Breakdown

* **Cloud Providers**: Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform (GCP).
* **Infrastructure as Code**: Terraform (HashiCorp AWS, AzureRM, and Google providers).
* **Process & Container Runtimes**: Linux `systemd`, Docker, AWS ECS Fargate, Azure Container Apps, GCP Cloud Run, Kubernetes.
* **CI/CD & GitOps Engines**: GitHub Actions, Azure DevOps Pipelines, GitLab CI, Argo CD.
* **Programming & Scripting**: Python 3.12, Golang (Gin), Bash, POSIX Shell.
* **Observability & SRE Tooling**: Prometheus, Grafana, Locust (Load Testing), Black-Box Synthetic Health Probes, Flake8.

---

## 📁 Repository Organization

```text
├── .github/
│   └── workflows/                # Global and per-project CI/CD pipeline definitions
├── Project 01 - Python Flask Monolith and Linux Systemd on AWS EC2/
│   ├── app/                      # Production Flask application & SQLite data access layer
│   ├── systemd/                  # Linux systemd unit configuration (Restart=always, capabilities)
│   ├── terraform/                # Infrastructure as Code (VPC, Subnet, Route Table, SG, EC2)
│   ├── sre-tests/                # Synthetic probes, chaos failure drills, and Locust load suites
│   ├── tests/                    # Application unit test suites
│   └── README.md                 # Detailed architectural walkthrough & verification proof
├── Project 02 - Go Microservice with Gin on Azure VM/
├── Project 03 - Modular Terraform and Docker on GCP Compute Engine/
└── ... [Projects 04 - 12]
```

---

## 📜 Principles & SRE Philosophy

1. **Automate Everything**: No manual console clicks; all infrastructure is provisioned through declarative IaC.
2. **Quality Gates Gated by Default**: Syntax checking, unit tests, and validation must pass before deployment can trigger.
3. **Resilience by Design**: Every service must implement self-healing (OS-level process supervisors or container restarts).
4. **Observable by Default**: Every application exposes `/healthz` deep health probes and `/metrics` in standard OpenMetrics exposition format.
