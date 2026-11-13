from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, time, sys
import database as db


app = Flask (__name__)
db.init_db()

START_TIME = time.time()
REQUEST_COUNT = 0
@app.before_request
def count_requests():
    """Automatically increments request counter on every incoming request."""
    global REQUEST_COUNT
    REQUEST_COUNT += 1



# ==============================================================================
# ROUTE 1: HOMEPAGE DASHBOARD
# ==============================================================================
@app.route("/")
def index():
    # 1. Fetch all skills from SQLite database as a list of dictionaries
    skills = db.get_all_skills()
    
    # 2. Compute summary metrics for dashboard stat cards
    total_skills = len(skills)
    completed = len([s for s in skills if s["status"] == "Completed"])
    in_progress = len([s for s in skills if s["status"] == "In Progress"])
    
    # 3. Calculate average proficiency (guarded against division by zero if DB is empty)
    if total_skills > 0:
        # Sum all proficiency scores first, then divide by total count
        avg_proficiency = int(sum([s["proficiency"] for s in skills]) / total_skills)
    else:
        avg_proficiency = 0

    # 4. Render HTML template and RETURN the response to the browser
    return render_template(
        "index.html",
        skills=skills,
        total_skills=total_skills,
        completed=completed,
        in_progress=in_progress,
        avg_proficiency=avg_proficiency,
        start_time=START_TIME,
        request_count=REQUEST_COUNT,
    )


# ==============================================================================
# ROUTE 2: ADD NEW SKILL (Form Submission)
# ==============================================================================
@app.route("/api/skills", methods=["POST"])
def api_add_skill():
    """
    Handles form submission to insert a new skill into the database.
    Reads form inputs, validates required fields, inserts row, and redirects.
    """
    # 1. Extract values submitted from the HTML dashboard form
    name = request.form.get("name")
    category = request.form.get("category")
    status = request.form.get("status")
    proficiency = int(request.form.get("proficiency", 0))

    # 2. Input validation: ensure critical fields are not empty
    if not name or not category:
        return jsonify({"error": "Missing required field"}), 400

    notes = request.form.get("notes", "")

    # 3. Insert record into SQLite database via our database module
    db.add_skill(name, category, status, proficiency, notes)

    # 4. Post/Redirect/Get (PRG) pattern: redirect back to home page
    return redirect(url_for("index"))
    
    

# ==============================================================================
# ROUTE 3: UPDATE SKILL STATUS & PROFICIENCY
# ==============================================================================
@app.route("/api/skills/<int:skill_id>/update", methods=["POST"])
def api_update_skill(skill_id):
    """
    Updates status and proficiency for an existing skill.
    The HTML table form sends 'status' (e.g. 'Completed') and 'proficiency' (100).
    """
    # 1. Read updated status and proficiency from form submission
    status = request.form.get("status", "Completed")
    proficiency = int(request.form.get("proficiency", 100))

    # 2. Update database record matching this skill_id
    db.update_skill_status(skill_id, status, proficiency)

    # 3. Redirect back to homepage dashboard (PRG pattern)
    return redirect(url_for("index"))





# ==============================================================================
# ROUTE 4: SRE HEALTHCHECK PROBE (Liveness & Readiness)
# ==============================================================================
@app.route("/healthz")
def healthz():
    """
    SRE Healthcheck Endpoint for Cloud Load Balancers & Process Supervisors.
    
    Performs a 'Deep' health check:
    - Queries the database ('SELECT 1') to verify SQLite file read access.
    - If healthy: returns HTTP 200 with uptime and database status.
    - If unhealthy: returns HTTP 503 so load balancers stop sending traffic.
    """
    try:
        # 1. Test database availability and responsiveness
        con = db.get_db_connection()
        con.execute("SELECT 1").fetchone()
        con.close()
        
        # 2. Return HTTP 200 OK
        return jsonify({
            "status": "healthy",
            "uptime_seconds": int(time.time() - START_TIME),
            "database": "connected"
        }), 200
        
    except Exception as e:
        # 3. Return HTTP 503 Service Unavailable if database fails
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503




# ==============================================================================
# ROUTE 5: SRE OBSERVABILITY METRICS (Prometheus Plain-Text Format)
# ==============================================================================
@app.route("/metrics")
def metrics():
    """
    Exposes application metrics in Prometheus plaintext exposition format.
    Scraped periodically by Prometheus / Grafana agents.
    Exposes:
      - app_uptime_seconds (gauge)
      - app_http_requests_total (counter)
      - app_skills_total (gauge)
    """
    # 1. Compute current metric values
    uptime = int(time.time() - START_TIME)
    skills = db.get_all_skills()
    total_skills = len(skills)

    # 2. Format metrics into official Prometheus exposition syntax
    metrics_payload = (
        f"# HELP app_uptime_seconds Total application uptime in seconds\n"
        f"# TYPE app_uptime_seconds gauge\n"
        f"app_uptime_seconds {uptime}\n\n"
        f"# HELP app_http_requests_total Total HTTP requests received\n"
        f"# TYPE app_http_requests_total counter\n"
        f"app_http_requests_total {REQUEST_COUNT}\n\n"
        f"# HELP app_skills_total Total skills tracked in database\n"
        f"# TYPE app_skills_total gauge\n"
        f"app_skills_total {total_skills}\n"
    )
    
    # 3. Return plain text payload with standard OpenMetrics Content-Type
    return metrics_payload, 200, {"Content-Type": "text/plain; version=0.0.4"}


# ==============================================================================
# ROUTE 6: SRE GAME DAY FAILURE DRILL (Simulated Crash)
# ==============================================================================
@app.route("/api/debug/crash", methods=["POST"])
def debug_crash():
    """
    Deliberate SRE Failure Drill Endpoint.
    Abruptly terminates the Python process with exit code 1 to test
    if Linux systemd automatically revives the service in production!
    """
    app.logger.warning("DELIBERATE SRE DRILL: Terminating process with exit code 1.")
    sys.exit(1)



# Starts the local development server when run via 'python app.py'
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    