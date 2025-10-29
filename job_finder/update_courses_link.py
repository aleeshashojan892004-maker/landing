import sqlite3

conn = sqlite3.connect("job_finder.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE courses ADD COLUMN link TEXT")
    conn.commit()
    print("✅ Column 'link' added successfully!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ Column 'link' already exists, no change needed.")
    else:
        print("❌ Error:", e)

# Optional: show updated table columns
cursor.execute("PRAGMA table_info(courses)")
print("\n📋 Updated courses table columns:")
for col in cursor.fetchall():
    print(col)

conn.close()
