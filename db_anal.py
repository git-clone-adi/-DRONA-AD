import sqlite3
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'drona_analytics.db')

print(f"Loading data from: {current_dir}")
print(f"Creating database at: {db_path}")

conn = sqlite3.connect(db_path)

pd.read_csv(os.path.join(current_dir, 'drona_schools.csv')).to_sql('schools', conn, if_exists='replace', index=False)
pd.read_csv(os.path.join(current_dir, 'drona_users.csv')).to_sql('users', conn, if_exists='replace', index=False)
pd.read_csv(os.path.join(current_dir, 'drona_sessions.csv')).to_sql('sessions', conn, if_exists='replace', index=False)
pd.read_csv(os.path.join(current_dir, 'drona_activities.csv')).to_sql('activities', conn, if_exists='replace', index=False)

conn.close()
print("Database populated successfully! Ready for queries.")
