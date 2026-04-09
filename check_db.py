import sqlite3
import pandas as pd
import os

# 1. Exact path identify karo
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'drona_analytics.db')

if not os.path.exists(db_path):
    print(f"❌ ERROR: Database file nahi mili at: {db_path}")
    print("Pehle 'anal.py' run karo data load karne ke liye.")
else:
    conn = sqlite3.connect(db_path)
    try:
        # Check karo ki tables exist karti hain ya nahi
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📂 Database location: {db_path}")
        print(f"📊 Found tables: {[t[0] for t in tables]}")
        print("-" * 30)

        if not tables:
            print("⚠️ DATABASE EMPTY HAI! 'anal.py' ko dobara run karo.")
        else:
            # Main query
            query = "SELECT school_type, COUNT(*) as school_count FROM schools GROUP BY school_type"
            df = pd.read_sql_query(query, conn)
            print("--- School Distribution ---")
            print(df)

    except Exception as e:
        print(f"❌ Error logic mein hai: {e}")
    finally:
        conn.close()
