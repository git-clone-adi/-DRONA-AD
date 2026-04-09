import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="DRONA Analytics Dashboard", layout="wide")

st.title("🛡️ DRONA School Analytics Dashboard")
st.markdown("Real-time engagement and adoption metrics for the Eklavya Platform.")

# Database Connection
def get_data(query):
    conn = sqlite3.connect('drona_analytics.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
school_type = st.sidebar.multiselect(
    "Select School Type", 
    options=['Government', 'Private', 'Semi-Government'],
    default=['Government', 'Private', 'Semi-Government']
)

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)

# Fetch all KPI metrics in a single query using CTE (efficient single DB trip)
kpi_data = get_data("""
    WITH user_count AS (SELECT COUNT(*) as user_count FROM users),
         session_stats AS (SELECT COUNT(*) as session_count, AVG(duration_minutes) as avg_duration FROM sessions),
         active_users AS (SELECT COUNT(DISTINCT user_id) as distinct_users FROM sessions)
    SELECT 
        (SELECT user_count FROM user_count) as total_users,
        (SELECT session_count FROM session_stats) as total_sessions,
        (SELECT avg_duration FROM session_stats) as avg_duration,
        (SELECT (distinct_users * 100.0 / (SELECT user_count FROM user_count)) FROM active_users) as active_rate
""")

total_users = int(kpi_data['total_users'][0])
total_sessions = int(kpi_data['total_sessions'][0])
avg_duration = kpi_data['avg_duration'][0]
active_rate = kpi_data['active_rate'][0]

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Total Sessions", f"{total_sessions:,}")
col3.metric("Avg. Session", f"{avg_duration:.1f} min")
col4.metric("Active User Rate", f"{active_rate:.1f}%")

st.divider()

# --- CHARTS SECTION ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Daily Active Users (DAU) Trend")
    dau_data = get_data("""
        SELECT date(login_time) as date, COUNT(DISTINCT user_id) as dau 
        FROM sessions GROUP BY 1 ORDER BY 1 ASC
    """)
    fig_dau = px.line(dau_data, x='date', y='dau', template="plotly_white", color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig_dau, use_container_width=True)

with c2:
    st.subheader("Feature Adoption")
    feature_data = get_data("""
        SELECT feature_used, COUNT(*) as usage_count 
        FROM activities GROUP BY 1 ORDER BY 2 DESC
    """)
    fig_feat = px.bar(feature_data, x='usage_count', y='feature_used', orientation='h', color='feature_used')
    st.plotly_chart(fig_feat, use_container_width=True)

# --- SCHOOL LEVEL TABLE ---
st.subheader("School Performance Leaderboard")
# Use parameterized query instead of string slicing for better security and flexibility
placeholders = ','.join(['?' for _ in school_type])
conn = sqlite3.connect('drona_analytics.db')
school_perf = pd.read_sql_query(f"""
    SELECT 
        s.school_id, 
        s.school_type, 
        s.city, 
        COUNT(DISTINCT u.user_id) as active_students,
        COUNT(sess.session_id) as total_interactions
    FROM schools s
    JOIN users u ON s.school_id = u.school_id
    JOIN sessions sess ON u.user_id = sess.user_id
    WHERE s.school_type IN ({placeholders})
    GROUP BY 1, 2, 3
    ORDER BY total_interactions DESC
    LIMIT 10
""", conn, params=school_type)
conn.close()
st.dataframe(school_perf, use_container_width=True)

st.success("Dashboard loaded successfully. All data is simulated based on DRONA platform architecture.")


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

st.divider()
st.subheader("🤖 AI-Driven Student Segmentation (K-Means Clustering)")
st.markdown("Using Machine Learning to automatically group students based on engagement patterns to identify **At-Risk** accounts.")

# Cache clustering computation to avoid recalculation on every page refresh
@st.cache_data
def perform_clustering():
    """Perform K-Means clustering with centroid-based mapping."""
    # Get data for clustering
    cluster_data = get_data("""
        SELECT 
            u.user_id,
            COUNT(s.session_id) as total_sessions,
            SUM(s.duration_minutes) as total_minutes
        FROM users u
        JOIN sessions s ON u.user_id = s.user_id
        WHERE u.role = 'Student'
        GROUP BY u.user_id
    """)
    
    # Prepare and scale data
    X = cluster_data[['total_sessions', 'total_minutes']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Run K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_data['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # CRITICAL FIX: Sort clusters by centroid activity (total_sessions) to ensure consistency
    centroid_activity = {}
    for cluster_id in range(3):
        # Calculate mean total_sessions for each cluster
        mean_sessions = cluster_data[cluster_data['Cluster'] == cluster_id]['total_sessions'].mean()
        centroid_activity[cluster_id] = mean_sessions
    
    # Sort clusters: low activity -> At-Risk, medium -> Casuals, high -> Champions
    sorted_clusters = sorted(centroid_activity.items(), key=lambda x: x[1])
    cluster_mapping = {
        sorted_clusters[0][0]: 'At-Risk',      # Lowest activity
        sorted_clusters[1][0]: 'Casuals',      # Medium activity
        sorted_clusters[2][0]: 'Champions'     # Highest activity
    }
    
    cluster_data['Segment'] = cluster_data['Cluster'].map(cluster_mapping)
    return cluster_data, cluster_mapping

# Get cached clustering results
cluster_data, cluster_mapping = perform_clustering()

# Visualize the AI Output
fig_cluster = px.scatter(
    cluster_data, 
    x='total_sessions', 
    y='total_minutes', 
    color='Segment',
    title="Student Engagement Clusters",
    color_discrete_sequence=['#EF553B', '#FFA15A', '#00CC96']  # At-Risk, Casuals, Champions
)
st.plotly_chart(fig_cluster, use_container_width=True)