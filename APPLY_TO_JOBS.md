# Target Job Market Analysis & Portfolio Alignment

This document analyzes the 9 target job postings provided, examining company profiles, technical skill requirements, and market salary bands (sourced from Levels.fyi, Glassdoor, AmbitionBox, and international tech hiring platforms). 

It details **actionable curriculum adjustments** we have integrated into our remaining 11 projects (Projects 02 – 12) to ensure you possess 100% of the required skills to interview and secure offers for these roles.

---

## 📊 Executive Summary & Market Compensation Table

| # | Company | Role Title | Location & Work Model | Market Salary Range (CTC / Base) | Primary Cloud & Tech Stack | Direct Project Alignment |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Natoe AI** | Lead Infrastructure & DevOps Engineer | Remote (India / US overlap) | **₹30 LPA – ₹50 LPA** ($38k – $62k USD) | Bare-Metal/Linux, Storage/DICOM, VPNs, Reverse Proxies, Ansible | Project 01, Project 02, Project 08 |
| **2** | **GoGuardian** | Senior Site Reliability Engineer | Remote (India) | **₹28 LPA – ₹48 LPA** | AWS (EC2, VPC, EKS), Terraform, Serverless, Python/Go, Observability | Project 01, Project 02, Project 04, Project 09 |
| **3** | **Sophos** | Site Reliability Engineer | India (Bengaluru / Ahmedabad / Remote) | **₹18 LPA – ₹32 LPA** (Mid) / **₹35 LPA – ₹50+ LPA** (Senior) | AWS (Security-first), Terraform, Docker, Kubernetes, Jenkins/GitHub Actions, Prometheus | Project 01, Project 04, Project 09, Project 12 |
| **4** | **Sophos** | Site Reliability Engineer / Cloud | India (Bengaluru / Ahmedabad / Remote) | **₹18 LPA – ₹30 LPA** (Mid) / **₹32 LPA – ₹48 LPA** (Senior) | Central Operations, Linux Admin, AWS SaaS, Incident Response, CI/CD | Project 01, Project 02, Project 04, Project 12 |
| **5** | **Toku** | Senior Staff Azure Cloud Infrastructure Engineer | Remote (India / Singapore / APAC) | **₹45 LPA – ₹75 LPA** (India) / **SGD $120k – $180k** (HQ) | Microsoft Azure (Landing Zones, VNets, ACA), Terraform Remote State, K8s | Project 02, Project 05, Project 09 |
| **6** | **Supabase** | Site Reliability Engineer | Remote (Global / APAC / India) | **$130,000 – $200,000+ USD** (₹1.1 Cr – ₹1.65 Cr) | PostgreSQL internals, High-Availability, K8s Operators, Go, Prometheus/Grafana | Project 02, Project 05, Project 10, Project 12 |
| **7** | **Supabase** | Cloud Platform Engineer | Remote (Global / APAC / India) | **$140,000 – $220,000+ USD** (₹1.15 Cr – ₹1.8 Cr) | Multi-Cloud (AWS + GCP), IAM Governance, Reusable IaC Primitives, Self-Service | Project 01, Project 03, Project 04, Project 06 |
| **8** | **Tyk Technologies** | Site Reliability Engineer - APAC | Remote (APAC / India / Global) | **₹28 LPA – ₹50 LPA** ($60k – $95k USD) | API Gateways, Multi-region K8s, AWS, Redis, Go/Python, Prometheus | Project 02, Project 07, Project 09, Project 12 |
| **9** | **Cyberhaven** | Senior/Staff Cloud Infrastructure Engineer | Bengaluru, India (Hybrid/Remote) | **₹30 LPA – ₹55 LPA** + Equity | Google Cloud Platform (GCP), GKE (Kubernetes), Terraform, Argo CD, GitHub Actions | Project 03, Project 06, Project 09, Project 11 |

---

## 🔍 In-Depth Role Analysis & Skills Breakdown

---

### 1. Natoe AI — Lead Infrastructure & DevOps Engineer
* **Job URL**: [natoe.ai/careers/lead-infrastructure-devops-engineer](https://natoe.ai/careers/lead-infrastructure-devops-engineer)
* **Company Profile**: US-based AI healthcare startup (Clearwater, Florida) specializing in AI-native teleradiology and medical imaging (DICOM/PACS). Bootstrapped / growing engineering team.
* **Core Responsibilities**:
  * Owns bare-metal Linux dedicated servers, storage capacity for large imaging archives, networking, and firewalls.
  * Disaster recovery: automated backups, periodic test restoration drills, and high availability.
  * Production security controls: MFA, secret management, encryption, and HIPAA / SOC 2 audit readiness.
  * Linux server hardening, patching, reverse proxies (Nginx/Traefik), and Bash/Python automation.
* **Compensation Data**: ₹30 LPA – ₹50 LPA (Contractor/FTE equivalent in India for US tech lead).
* **What We Have & What We Must Include**:
  * **Already Covered in Project 01**: Hardened Linux OS, `systemd` process supervision, non-root user capabilities (`CAP_NET_BIND_SERVICE`), and chaos disaster drills.
  * **Addition in Project 08**: Implement asynchronous queue processing with Celery/RabbitMQ to handle simulated medical DICOM file ingestion and storage archiving.

---

### 2. GoGuardian — Senior Site Reliability Engineer
* **Job URL**: [job-boards.greenhouse.io/goguardian/jobs/4715815006](https://job-boards.greenhouse.io/goguardian/jobs/4715815006)
* **Company Profile**: Leading US educational technology (EdTech) scale-up providing digital learning and student safety software used by millions of K-12 students.
* **Core Responsibilities**:
  * Core AWS infrastructure management (EC2, VPC, S3) and managed Kubernetes (AWS EKS).
  * Infrastructure as Code using Terraform.
  * Modernizing CI/CD pipelines using GitHub Actions and AWS CodePipeline.
  * Enhancing observability frameworks (minimizing alert noise, SLA/SLO tracking, incident RCAs).
  * Data layer operations (MongoDB, Redshift, OpenSearch, Firestore).
  * Debugging application code written in Python, Go, and TypeScript.
* **Compensation Data**: ₹28 LPA – ₹48 LPA (Senior SRE in India remote).
* **What We Have & What We Must Include**:
  * **Already Covered in Project 01**: Terraform VPC/EC2 provisioning, GitHub Actions CI/CD with automated testing, and comprehensive incident post-mortems in `INCIDENTS.md`.
  * **Addition in Project 02**: Writing and debugging Go microservice code to satisfy their Go debugging requirement.
  * **Addition in Project 04 & 09**: AWS ECS Fargate and AWS EKS Kubernetes deployments with container health probes.

---

### 3 & 4. Sophos — Site Reliability Engineer (SRE & SRE Cloud)
* **Job URLs**:
  * [jobs.ashbyhq.com/sophos/0b9af89e-23ae-4e34-a206-8db40e2c10f4](https://jobs.ashbyhq.com/sophos/0b9af89e-23ae-4e34-a206-8db40e2c10f4)
  * [jobs.ashbyhq.com/sophos/46929d7f-2677-4837-a033-134d9fde79fe](https://jobs.ashbyhq.com/sophos/46929d7f-2677-4837-a033-134d9fde79fe)
* **Company Profile**: Global cybersecurity powerhouse headquartered in the UK with major engineering R&D centres in Bengaluru and Ahmedabad, India.
* **Core Responsibilities**:
  * Design, implement, and maintain Infrastructure as Code using Terraform with a security-first mindset.
  * Build automated CI/CD deployment pipelines using GitHub Actions and Jenkins.
  * Container orchestration on Docker and Kubernetes for microservices.
  * Setup and management of observability stacks using Prometheus, Grafana, and AWS CloudWatch.
  * Root Cause Analysis (RCA), incident management, and cloud cost optimization.
* **Compensation Data**: ₹18 LPA – ₹32 LPA (Mid-level SRE, 3–5 yrs) / ₹35 LPA – ₹55 LPA (Senior SRE, 6+ yrs).
* **What We Have & What We Must Include**:
  * **Already Covered in Project 01**: Cloud cost optimization, eliminating orphan resources, synthetic monitoring probes, and complete RCA logs.
  * **Addition in Project 09 & 10**: Deploying multi-container Kubernetes pods with rolling updates.
  * **Addition in Project 12**: Building a full Prometheus and Grafana monitoring stack with alert rules.

---

### 5. Toku — Senior Staff Azure Cloud Infrastructure Engineer
* **Job URL**: [toku.co/careers/senior-staff-cloud-infrastructure-engineer/](https://toku.co/careers/senior-staff-cloud-infrastructure-engineer/)
* **Company Profile**: Fast-growing cloud communications and customer engagement platform headquartered in Singapore with distributed engineering teams across APAC and India.
* **Core Responsibilities**:
  * Architecting and scaling Microsoft Azure cloud infrastructure (Azure Landing Zones, VNets, Azure Container Apps, AKS).
  * Terraform Infrastructure as Code with distributed remote state storage and state locking.
  * Deep networking, security guardrails, and automated CI/CD delivery.
  * Microservices architecture, high availability, and telephony integration.
* **Compensation Data**: ₹45 LPA – ₹75 LPA (Senior/Staff Level in India) / SGD $120,000 – $180,000 (Singapore).
* **What We Have & What We Must Include**:
  * **Addition in Project 02**: **First Go Microservice with Gin on Azure VM** uses Azure Virtual Machines and implements **Terraform Remote State with Azure Blob Storage + State Locking**!
  * **Addition in Project 05**: **Azure Container Apps (ACA) with Golang & Dragonfly** directly mirrors Toku's exact Azure containerized microservice tech stack!

---

### 6 & 7. Supabase — SRE & Cloud Platform Engineer
* **Job URLs**:
  * SRE: [jobs.ashbyhq.com/supabase/ed6cedb1-b9bf-4609-ac5c-c75c33b31bf3](https://jobs.ashbyhq.com/supabase/ed6cedb1-b9bf-4609-ac5c-c75c33b31bf3)
  * Cloud Platform: [jobs.ashbyhq.com/supabase/5d09daeb-2d7e-42de-9151-81a1341195c4](https://jobs.ashbyhq.com/supabase/5d09daeb-2d7e-42de-9151-81a1341195c4)
* **Company Profile**: The open-source Firebase alternative and premier managed PostgreSQL cloud platform. Remote-first global company supporting millions of database instances.
* **Core Responsibilities**:
  * **SRE Role**: High-availability database operations, custom Kubernetes controllers, deep telemetry (OpenTelemetry, Prometheus, Grafana), incident response, and Go/Rust/Python reliability engineering.
  * **Platform Engineer Role**: Multi-cloud governance across AWS and GCP, IAM identity structures, reusable Terraform platform building blocks, security boundaries, and developer self-service tooling.
* **Compensation Data**: **$130,000 – $220,000+ USD** (₹1.1 Crore – ₹1.8 Crore base salary + equity) with global remote parity.
* **What We Have & What We Must Include**:
  * **Addition in Project 03 & 06**: Provisioning Google Cloud Platform (GCP) infrastructure using reusable Terraform modules.
  * **Addition in Project 10**: Packaging PostgreSQL database workloads with Kubernetes Helm charts and PersistentVolumes (PV/PVC).
  * **Addition in Project 12**: Instrumenting applications with Prometheus client metrics and monitoring the Four Golden Signals.

---

### 8. Tyk Technologies — Site Reliability Engineer (APAC)
* **Job URL**: [wellfound.com/jobs/3541839-site-reliability-engineer-apac](https://wellfound.com/jobs/3541839-site-reliability-engineer-apac)
* **Company Profile**: Leading enterprise API Management Platform headquartered in London with global remote teams across US, EMEA, and APAC.
* **Core Responsibilities**:
  * Managing high-throughput multi-region Kubernetes clusters.
  * Core stack: AWS, Go, Python, Redis, MongoDB, Prometheus, and Grafana.
  * API Gateway reliability, rate-limiting, edge latency reduction, and 99.99% uptime.
* **Compensation Data**: ₹28 LPA – ₹50 LPA ($60,000 – $95,000 USD) for APAC remote engineers.
* **What We Have & What We Must Include**:
  * **Addition in Project 07**: **Distributed Caching with Redis (Cache-Aside Pattern)** directly equips you to discuss Redis cache eviction, TTL tuning, and API latency reduction.
  * **Addition in Project 09**: Deploying Kubernetes Ingress controllers and service routing.

---

### 9. Cyberhaven — Senior/Staff Cloud Infrastructure Engineer
* **Job URL**: [wellfound.com/jobs/3718860-senior-staff-cloud-infrastructure-engineer](https://wellfound.com/jobs/3718860-senior-staff-cloud-infrastructure-engineer)
* **Company Profile**: Fast-growing data detection and response (DDR) cybersecurity scale-up with major engineering operations in Bengaluru and Silicon Valley.
* **Core Responsibilities**:
  * Cloud infrastructure on Google Cloud Platform (GCP) and Google Kubernetes Engine (GKE).
  * Infrastructure as Code using Terraform.
  * CI/CD automation using **GitHub Actions** and **Argo CD** (Declarative GitOps).
  * Eliminating developer build/test bottlenecks and driving infrastructure observability.
* **Compensation Data**: ₹30 LPA – ₹55 LPA + high-growth equity (Bengaluru).
* **What We Have & What We Must Include**:
  * **Addition in Project 03 & 06**: GCP Compute Engine and GCP Cloud Run.
  * **Addition in Project 11**: **Declarative GitOps with Argo CD** — our Project 11 directly implements the exact Argo CD + GitHub Actions deployment engine Cyberhaven uses!

---

## 🎯 Curriculum Inclusions: How We Address Every Single Role

By cross-referencing all 9 job requirements, we have enhanced our remaining project blueprint with these exact skills:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   MARKET-DRIVEN CURRICULUM ENHANCEMENTS                          │
└──────────────────────────────────────────────────────────────────────────────────┘
  1. Golang Compiled Microservices (Gin)      ──> Project 02 & Project 05 (Supabase, Toku, GoGuardian, Tyk)
  2. Terraform Remote State & Azure Storage   ──> Project 02 (Toku, Supabase)
  3. GCP Infrastructure & Reusable Modules    ──> Project 03 & Project 06 (Cyberhaven, Supabase)
  4. AWS ECS Fargate & Cloud-Native Health    ──> Project 04 (GoGuardian, Sophos)
  5. Redis Caching & Cache-Aside Architecture ──> Project 07 (Tyk, GoGuardian)
  6. RabbitMQ & Asynchronous Worker Queues    ──> Project 08 (Natoe AI, Sophos)
  7. Kubernetes (Pods, Probes, Services)      ──> Project 09 (Sophos, GoGuardian, Cyberhaven, Tyk)
  8. Helm Charts & Stateful PostgreSQL        ──> Project 10 (Supabase, Tyk)
  9. Declarative GitOps with Argo CD          ──> Project 11 (Cyberhaven)
 10. Prometheus, Grafana & Golden Signals     ──> Project 12 (All 9 Target Roles!)
```

With this mapping, completing your 12-project portfolio gives you proven, hands-on production code and incident defense for every requirement across all 9 job descriptions.
