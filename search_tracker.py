from SRC.database import get_connection
 
def save_search(username, question):
 
    question = question.lower().strip()
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("""
        SELECT search_count FROM search_history
        WHERE username=? AND question=?
    """, (username, question))
 
    result = cursor.fetchone()
 
    # If already searched
    if result:
 
        new_count = result[0] + 1
 
        cursor.execute("""
            UPDATE search_history
            SET search_count=?, last_searched=CURRENT_TIMESTAMP
            WHERE username=? AND question=?
        """, (new_count, username, question))
 
    else:
 
        cursor.execute("""
            INSERT INTO search_history(username, question, search_count)
            VALUES (?, ?, 1)
        """, (username, question))
 
    conn.commit()
    conn.close()
 
 
def get_top_questions():
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("""
        SELECT question, SUM(search_count) as total
        FROM search_history
        GROUP BY question
        ORDER BY total DESC
    """)
 
    data = cursor.fetchall()
 
    conn.close()
 
    return data
 
 
def get_top_users():
 
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("""
        SELECT username, SUM(search_count) as total
        FROM search_history
        GROUP BY username
        ORDER BY total DESC
    """)
 
    data = cursor.fetchall()
 
    conn.close()
 
    return data