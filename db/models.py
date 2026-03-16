from datetime import datetime, timezone
from db.database import get_connection

def insert_documents(rows):
    conn = get_connection()
    cursor = conn.cursor()

    collected_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    inserted = 0

    for row in rows:
        try:
            cursor.execute("""
            INSERT INTO documents (source, title, published_at, collected_at)
            VALUES (?, ?, ?, ?)
            """, (
                row["source"],
                row["title"],
                row["date"],
                collected_at
            ))
            inserted += 1
        except Exception:
            pass

    conn.commit()
    conn.close()
    return inserted
