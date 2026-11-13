import os
import sys
import tempfile
import unittest

# Add parent directory to sys.path so test can import 'app' and 'database'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class SkillsAppTestCase(unittest.TestCase):
    """
    Automated Test Suite for SRE Skills Tracker.
    Ensures application endpoints, database persistence, and observability work correctly.
    """

    def setUp(self):
        """
        Runs BEFORE every single test:
        Creates a temporary isolated SQLite database so real data is never touched or corrupted.
        """
        self.db_fd, self.db_path = tempfile.mkstemp()
        os.environ["DB_PATH"] = self.db_path
        
        # Import app and database with our isolated DB_PATH
        import app
        import database
        self.app = app.app
        self.app.config["TESTING"] = True
        
        # Initialize schema and seed data in the temporary DB
        database.init_db()
        
        # Virtual in-memory HTTP test client
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Runs AFTER every single test:
        Closes and removes the temporary SQLite database file.
        """
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    # --------------------------------------------------------------------------
    # SRE HEALTH & OBSERVABILITY TESTS
    # --------------------------------------------------------------------------
    def test_healthz_endpoint(self):
        """Verify that /healthz returns HTTP 200 OK and reports database connectivity."""
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        self.assertIn("uptime_seconds", data)

    def test_metrics_endpoint(self):
        """Verify that /metrics returns HTTP 200 OK with Prometheus exposition format."""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"app_uptime_seconds", response.data)
        self.assertIn(b"app_http_requests_total", response.data)
        self.assertIn(b"app_skills_total", response.data)
        self.assertEqual(response.headers.get("Content-Type"), "text/plain; version=0.0.4")

    # --------------------------------------------------------------------------
    # WEB UI & DASHBOARD TESTS
    # --------------------------------------------------------------------------
    def test_index_dashboard(self):
        """Verify that the homepage renders correctly with title and seed skills."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SRE Skills Tracker", response.data)
        self.assertIn(b"Linux Systemd", response.data)

    # --------------------------------------------------------------------------
    # API FUNCTIONALITY & PERSISTENCE TESTS
    # --------------------------------------------------------------------------
    def test_add_skill(self):
        """Verify submitting form data to /api/skills saves to SQLite and redirects."""
        new_skill_data = {
            "name": "AWS VPC Peering",
            "category": "Networking",
            "status": "In Progress",
            "proficiency": "45",
            "notes": "Testing network isolation"
        }
        # Post form-encoded data
        response = self.client.post("/api/skills", data=new_skill_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify the new skill text appears in the rendered dashboard
        self.assertIn(b"AWS VPC Peering", response.data)

    def test_add_skill_validation_error(self):
        """Verify submitting a skill without a name returns HTTP 400 Bad Request."""
        invalid_data = {
            "name": "",
            "category": "Networking",
            "status": "In Progress"
        }
        response = self.client.post("/api/skills", data=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_update_skill_status(self):
        """Verify updating status and proficiency for an existing skill."""
        update_data = {
            "status": "Completed",
            "proficiency": "100"
        }
        # Update skill with ID 1 (Linux Systemd from seed data)
        response = self.client.post("/api/skills/1/update", data=update_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
