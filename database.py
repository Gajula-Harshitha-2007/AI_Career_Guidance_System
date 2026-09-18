import sqlite3


# Connect to database
conn = sqlite3.connect("career.db")

cursor = conn.cursor()


# =========================
# USERS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

)
""")


# =========================
# ASSESSMENT HISTORY TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS assessments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_name TEXT NOT NULL,

    interest TEXT,

    programming INTEGER,

    problem_solving INTEGER,

    mathematics INTEGER,

    ai_interest INTEGER,

    design INTEGER,

    security INTEGER,

    communication INTEGER,

    recommended_career TEXT NOT NULL

)
""")


# Save changes
conn.commit()

# Close database
conn.close()


print("Database setup completed successfully!")