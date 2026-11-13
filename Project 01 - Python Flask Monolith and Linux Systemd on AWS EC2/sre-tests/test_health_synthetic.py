"""
SRE Synthetic Probe Test Suite
================================================================================
Project: Project 01 - Python Flask Monolith & Linux Systemd on AWS EC2
Purpose: Black-box / Synthetic monitoring probe simulating user & scraper traffic
         against live production infrastructure. Validates Service Level
         Objectives (SLOs), latency budgets, and deep health indicators.
================================================================================
"""

import os
import time
import unittest
import requests

# Target endpoint configurable via environment variable (default: live Mumbai EC2)
TARGET_URL = os.getenv("TARGET_URL", "http://65.2.9.159").rstrip("/")

# SRE Latency SLO Budgets (in seconds)
# Set for external WAN probes over the public internet to AWS ap-south-1
LATENCY_BUDGET_DASHBOARD = 1.5     # 1500ms max for HTML dashboard
LATENCY_BUDGET_HEALTHCHECK = 1.0   # 1000ms max for /healthz deep probe
LATENCY_BUDGET_METRICS = 1.5       # 1500ms max for /metrics exposition
LATENCY_BUDGET_TRANSACTION = 2.0   # 2000ms max for synthetic write transactions


class SRESyntheticHealthTests(unittest.TestCase):
    """
    Automated synthetic test probes executed against live deployed infrastructure.
    Acts as an external probe verifying real-world availability and performance.
    """

    @classmethod
    def setUpClass(cls):
        print(f"\n=======================================================")
        print(f" [SRE SYNTHETIC PROBE RUNNER]")
        print(f" Target Infrastructure: {TARGET_URL}")
        print(f" Timestamp:             {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        print(f"=======================================================\n")

    def test_01_dashboard_availability(self):
        """
        Probe 1: User-Facing Dashboard Availability & Latency SLO.
        Validates: HTTP 200, HTML payload, and latency < 1000ms.
        """
        url = f"{TARGET_URL}/"
        start_time = time.time()
        response = requests.get(url, timeout=5)
        duration = time.time() - start_time

        print(f"[PROBE 1: Dashboard]    Latency: {duration*1000:.1f}ms | Status: {response.status_code}")

        self.assertEqual(
            response.status_code, 200,
            f"Dashboard returned unexpected status code {response.status_code}"
        )
        self.assertIn(
            "SRE Skills Tracker", response.text,
            "Expected dashboard header 'SRE Skills Tracker' not found in response HTML"
        )
        self.assertLess(
            duration, LATENCY_BUDGET_DASHBOARD,
            f"Dashboard latency ({duration*1000:.1f}ms) breached SLO budget ({LATENCY_BUDGET_DASHBOARD*1000:.0f}ms)"
        )

    def test_02_deep_healthz_probe(self):
        """
        Probe 2: Deep Healthcheck (/healthz) Verification.
        Validates: HTTP 200, JSON schema, database connection status, and latency < 500ms.
        """
        url = f"{TARGET_URL}/healthz"
        start_time = time.time()
        response = requests.get(url, timeout=5)
        duration = time.time() - start_time

        print(f"[PROBE 2: Healthz]      Latency: {duration*1000:.1f}ms | Status: {response.status_code}")

        self.assertEqual(
            response.status_code, 200,
            f"Healthcheck failed with HTTP {response.status_code}"
        )
        self.assertIn(
            "application/json", response.headers.get("Content-Type", ""),
            "Healthcheck Content-Type must be application/json"
        )

        data = response.json()
        self.assertEqual(
            data.get("status"), "healthy",
            f"Expected status 'healthy' but got '{data.get('status')}'"
        )
        self.assertEqual(
            data.get("database"), "connected",
            f"Database health check failed: '{data.get('database')}'"
        )
        self.assertIsInstance(
            data.get("uptime_seconds"), int,
            "Uptime seconds must be an integer"
        )
        self.assertGreaterEqual(
            data.get("uptime_seconds"), 0,
            "Uptime seconds must be non-negative"
        )
        self.assertLess(
            duration, LATENCY_BUDGET_HEALTHCHECK,
            f"Healthz latency ({duration*1000:.1f}ms) breached SLO budget ({LATENCY_BUDGET_HEALTHCHECK*1000:.0f}ms)"
        )

    def test_03_prometheus_metrics_exposition(self):
        """
        Probe 3: Prometheus Observability Metrics Scraping.
        Validates: HTTP 200, text/plain format, and required Prometheus metric lines.
        """
        url = f"{TARGET_URL}/metrics"
        start_time = time.time()
        response = requests.get(url, timeout=5)
        duration = time.time() - start_time

        print(f"[PROBE 3: Metrics]      Latency: {duration*1000:.1f}ms | Status: {response.status_code}")

        self.assertEqual(
            response.status_code, 200,
            f"Metrics endpoint failed with HTTP {response.status_code}"
        )
        self.assertIn(
            "text/plain", response.headers.get("Content-Type", ""),
            "Metrics Content-Type must be text/plain"
        )

        metrics_text = response.text
        # Assert required Prometheus metric gauges/counters exist
        self.assertIn("app_uptime_seconds", metrics_text)
        self.assertIn("app_http_requests_total", metrics_text)
        self.assertIn("app_skills_total", metrics_text)

        self.assertLess(
            duration, LATENCY_BUDGET_METRICS,
            f"Metrics latency ({duration*1000:.1f}ms) breached SLO budget ({LATENCY_BUDGET_METRICS*1000:.0f}ms)"
        )

    def test_04_synthetic_transaction_lifecycle(self):
        """
        Probe 4: Synthetic Write Transaction.
        Simulates an active user creating a new skill via the POST API.
        Validates: HTTP 200 (following redirect), successful persistence, and latency < 1000ms.
        """
        url = f"{TARGET_URL}/api/skills"
        synthetic_skill_name = f"SRE-Probe-{int(time.time())}"
        payload = {
            "name": synthetic_skill_name,
            "category": "Synthetic Monitoring",
            "status": "In Progress",
            "proficiency": "95",
            "notes": "Automated probe injected by SRE test harness."
        }

        start_time = time.time()
        response = requests.post(url, data=payload, allow_redirects=True, timeout=5)
        duration = time.time() - start_time

        print(f"[PROBE 4: Transaction]  Latency: {duration*1000:.1f}ms | Status: {response.status_code}")

        self.assertEqual(
            response.status_code, 200,
            f"Synthetic transaction failed with HTTP {response.status_code}"
        )
        self.assertIn(
            synthetic_skill_name, response.text,
            f"Newly created skill '{synthetic_skill_name}' was not found in rendered dashboard HTML"
        )
        self.assertLess(
            duration, LATENCY_BUDGET_TRANSACTION,
            f"Transaction latency ({duration*1000:.1f}ms) breached SLO budget ({LATENCY_BUDGET_TRANSACTION*1000:.0f}ms)"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
