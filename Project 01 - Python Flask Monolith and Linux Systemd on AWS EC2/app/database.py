import sqlite3
import os

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# Defines where the SQLite database file will live on disk.
# - By default, it creates 'skills.db' in the same folder as this file.
# - 'os.environ.get("DB_PATH", ...)' allows us to override the path during
#   automated testing so tests don't overwrite production data.
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "skills.db"))


# ==============================================================================
# 1. CONNECTION FACTORY
# ==============================================================================
def get_db_connection():
    """
    Opens a connection to the SQLite database file on disk.
    
    KEY SRE CONCEPT - row_factory:
    By setting 'con.row_factory = sqlite3.Row', SQLite returns rows that behave
    like Python dictionaries (e.g. row['name'], row['proficiency']) instead of
    number-indexed tuples (e.g. row[0], row[1]). This makes code much safer and readable.
    """
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


# ==============================================================================
# 2. SCHEMA INITIALIZATION & SEEDING
# ==============================================================================
def init_db():
    """
    Initializes the database schema when the application boots up.
    
    1. Runs CREATE TABLE IF NOT EXISTS: Ensures the table exists without crashing
       if the database was already created on a previous run.
    2. Column Definitions:
       - id: Unique integer auto-incremented by SQLite (1, 2, 3...)
       - name: Title of the skill (cannot be null)
       - category: Grouping (e.g. OS, Infrastructure, Observability)
       - status: Current state ('Not Started', 'In Progress', 'Completed')
       - proficiency: Percentage integer (0 to 100)
       - notes: Free-form text notes
       - updated_at: Automatically populated with current UTC timestamp
    3. Seed Data: Checks if the table is empty; if so, inserts 2 starter skills
       so the dashboard isn't blank on first launch.
    4. Commit & Close: Saves changes to disk and releases the file lock.
    """
    con = get_db_connection()
    cur = con.cursor()
    
    # Create the table schema
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            proficiency INTEGER DEFAULT 0,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Check if the table is currently empty
    cur.execute("SELECT COUNT(*) FROM skills")
    count = cur.fetchone()[0]
    
    # If empty (first run), insert initial starter skills
    if count == 0:
        cur.execute("""
            INSERT INTO skills (name, category, status, proficiency, notes)
            VALUES (?, ?, ?, ?, ?)
        """, ("Linux Systemd", "OS", "In Progress", 60, "Learning service units and auto-restart"))

        cur.execute("""
            INSERT INTO skills (name, category, status, proficiency, notes)
            VALUES (?, ?, ?, ?, ?)
        """, ("Terraform Basics", "Infrastructure", "In Progress", 40, "Learning AWS VPC and EC2 provisioning"))

        # con.commit() writes and saves the changes permanently to disk
        con.commit()
        
    con.close()


# ==============================================================================
# 3. READ OPERATION (Get All Skills)
# ==============================================================================
def get_all_skills():
    """
    Fetches all skills from the database ordered by ID ascending.
    
    - 'SELECT * FROM skills ORDER BY id ASC' retrieves all rows.
    - 'cur.fetchall()' returns a list of sqlite3.Row objects.
    - '[dict(s) for s in skills]' converts the SQLite rows into standard Python
      dictionaries so Flask can render them in HTML or return them as JSON.
    """
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM skills ORDER BY id ASC")
    skills = cur.fetchall()
    con.close()

    return [dict(s) for s in skills]


# ==============================================================================
# 4. CREATE OPERATION (Add New Skill)
# ==============================================================================
def add_skill(name, category, status, proficiency, notes):
    """
    Inserts a new skill into the database.
    
    SECURITY CONCEPT - Parameterized Queries:
    Notice the 'VALUES (?, ?, ?, ?, ?)'. We pass variables as a tuple in the
    second argument instead of using string formatting (f'INSERT INTO ... {name}').
    This guarantees immunity against SQL Injection attacks.
    
    Returns:
    - 'cur.lastrowid': The newly generated primary key (id) for this record.
    """
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO skills (name, category, status, proficiency, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, status, proficiency, notes))

    con.commit()
    skill_id = cur.lastrowid
    con.close()

    return skill_id


# ==============================================================================
# 5. UPDATE OPERATION (Update Status & Proficiency)
# ==============================================================================
def update_skill_status(skill_id, status, proficiency):
    """
    Updates the status and proficiency percentage of an existing skill.
    
    CRITICAL SRE/SQL CONCEPT - The WHERE Clause:
    Always include 'WHERE id = ?'. If you omit the WHERE clause, SQL will
    accidentally overwrite EVERY row in the entire table!
    
    - 'updated_at = CURRENT_TIMESTAMP': Updates the record's modification date.
    """
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE skills
        SET status = ?, proficiency = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, proficiency, skill_id))

    con.commit()
    con.close()
