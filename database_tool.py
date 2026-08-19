import sqlite3

DB_FILE = "college_data.db"

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            allowed_role TEXT NOT NULL
        )
    """)

    cursor.execute("DELETE FROM records")

    sample_data = [
        ("DBMS exam is scheduled on 20th September, 10 AM, Room 204.", "all"),
        ("OOP exam is scheduled on 22nd September, 2 PM, Room 108.", "all"),
        ("HOD monthly salary is 150000 rupees.", "admin"),
        ("Assistant Professor monthly salary is 80000 rupees.", "admin"),
        ("Faculty meeting scheduled for 5th September, discussing curriculum changes.", "faculty"),
        ("Class average for AI course is 78 percent this semester.", "faculty"),
    ]

    cursor.executemany(
        "INSERT INTO records (text, allowed_role) VALUES (?, ?)",
        sample_data
    )

    conn.commit()
    conn.close()

ROLE_ACCESS = {
    "student": ["all"],
    "faculty": ["all", "faculty"],
    "admin": ["all", "faculty", "admin"]
}

def search_database(query: str, user_role: str, top_k: int = 3) -> list[dict]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    allowed_roles = ROLE_ACCESS.get(user_role, ["all"])
    placeholders = ",".join("?" * len(allowed_roles))

    cursor.execute(f"""
        SELECT text, allowed_role FROM records
        WHERE allowed_role IN ({placeholders})
        AND text LIKE ?
    """, (*allowed_roles, f"%{query}%"))

    rows = cursor.fetchall()
    conn.close()

    output = []
    for text, allowed_role in rows[:top_k]:
        output.append({
            "text": text,
            "source": "college_database",
            "type": "database",
            "relevance_score": 0.9
        })
    return output

if __name__ == "__main__":
    setup_database()

    print("\n--- As student, asking about salary ---")
    print(search_database("salary", "student"))

    print("\n--- As admin, asking about salary ---")
    print(search_database("salary", "admin"))

    print("\n--- As student, asking about exam ---")
    print(search_database("exam", "student"))