"""
SRE Load & Stress Testing Suite (Locust)
================================================================================
Project: Project 01 - Python Flask Monolith & Linux Systemd on AWS EC2
Purpose: Simulates concurrent user traffic, Prometheus scraper load, and
         synthetic transactions to test system capacity, latency degradation,
         and error rates under load.
================================================================================
Usage:
    # Run interactive Web UI at http://localhost:8089:
    locust -f sre-tests/locustfile.py --host http://65.2.9.159

    # Run headless automated 30s load test (50 users, 5 users/sec ramp-up):
    locust -f sre-tests/locustfile.py --headless -u 50 -r 5 --run-time 30s --host http://65.2.9.159
================================================================================
"""

import random
from locust import HttpUser, task, between


class SkillsTrackerUser(HttpUser):
    """
    Simulates real-world traffic profiles:
    - 60% Dashboard Browsers (GET /)
    - 20% Healthcheck & Monitoring Scrapers (GET /healthz & GET /metrics)
    - 20% Active Users adding new skills (POST /api/skills)
    """

    # Wait 1 to 3 seconds between tasks per simulated user
    wait_time = between(1.0, 3.0)

    @task(6)
    def view_dashboard(self):
        """Browses the main dashboard page."""
        self.client.get("/", name="[GET] / (Dashboard)")

    @task(2)
    def check_health_and_metrics(self):
        """Simulates Prometheus scraper and AWS health monitoring probes."""
        self.client.get("/healthz", name="[GET] /healthz (Health Probe)")
        self.client.get("/metrics", name="[GET] /metrics (Prometheus Metrics)")

    @task(2)
    def add_skill_transaction(self):
        """Simulates an active user submitting a new skill via the web form."""
        random_id = random.randint(1000, 9999)
        payload = {
            "name": f"Stress-Test-Skill-{random_id}",
            "category": random.choice(["Cloud & AWS", "CI/CD & DevOps", "Linux Systems", "Monitoring"]),
            "status": random.choice(["In Progress", "Completed", "Not Started"]),
            "proficiency": random.randint(10, 100),
            "notes": "Automated Locust load-test transaction."
        }
        self.client.post("/api/skills", data=payload, name="[POST] /api/skills (Add Skill)")
