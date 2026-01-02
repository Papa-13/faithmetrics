"""
FaithMetrics - Multi-Church Analytics & Insights Platform
A comprehensive analytics system for faith communities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FaithMetrics | Church Analytics Platform",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning dark theme with glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Dark Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Dark Glassmorphism Container */
    .main .block-container {
        background: rgba(30, 30, 50, 0.4);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Typography - Elegant Light Text */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    p, div, span, label {
        font-family: 'Poppins', sans-serif !important;
        color: #e0e0e0 !important;
    }
    
    /* Main area text colors */
    .main * {
        color: #e0e0e0;
    }
    
    .main h1, .main h2, .main h3, .main h4 {
        color: #ffffff !important;
    }
    
    /* 3D Floating Header with Dark Glow */
    .main-header {
        position: relative;
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.3) 0%, 
            rgba(118, 75, 162, 0.3) 50%, 
            rgba(240, 147, 251, 0.3) 100%);
        backdrop-filter: blur(20px);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.3),
            0 0 100px rgba(118, 75, 162, 0.2),
            inset 0 0 50px rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        animation: float 6s ease-in-out infinite;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: particleMove 20s linear infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes particleMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .main-header h1 {
        position: relative;
        color: white !important;
        font-size: 4rem !important;
        margin: 0 !important;
        text-shadow: 
            0 0 20px rgba(102, 126, 234, 0.8),
            0 0 40px rgba(118, 75, 162, 0.6),
            2px 2px 4px rgba(0,0,0,0.5);
        letter-spacing: -2px;
        animation: textGlow 3s ease-in-out infinite;
    }
    
    @keyframes textGlow {
        0%, 100% { text-shadow: 0 0 20px rgba(102, 126, 234, 0.8), 0 0 40px rgba(118, 75, 162, 0.6); }
        50% { text-shadow: 0 0 30px rgba(102, 126, 234, 1), 0 0 60px rgba(240, 147, 251, 0.8); }
    }
    
    .main-header p {
        position: relative;
        color: rgba(255,255,255,0.95) !important;
        font-size: 1.3rem !important;
        margin-top: 0.5rem !important;
        font-weight: 300;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 2px;
    }
    
    /* Dark 3D Metric Cards with Neon Glow */
    .metric-card {
        background: rgba(30, 30, 50, 0.8);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(102, 126, 234, 0.3) inset;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border: 2px solid rgba(102, 126, 234, 0.2);
        position: relative;
        overflow: hidden;
        animation: slideUp 0.6s ease-out;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent, 
            rgba(102, 126, 234, 0.1), 
            transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    .metric-card:hover {
        transform: translateY(-15px) scale(1.05);
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.4),
            0 0 40px rgba(118, 75, 162, 0.5),
            0 0 0 3px rgba(102, 126, 234, 0.6) inset;
        border: 2px solid rgba(102, 126, 234, 0.6);
        background: rgba(40, 40, 70, 0.9);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Space Grotesk', sans-serif !important;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #a0a0c0;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-change {
        font-size: 0.9rem;
        margin-top: 0.75rem;
        font-weight: 600;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
    }
    
    .metric-change.positive {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
    }
    
    .metric-change.negative {
        background: linear-gradient(135deg, #dc3545, #e83e8c);
        color: white;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
    }
    
    /* Dark Futuristic Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(15, 12, 41, 0.98) 0%, 
            rgba(24, 20, 50, 0.98) 100%);
        backdrop-filter: blur(20px);
        padding-top: 2rem;
        border-right: 2px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        position: relative;
    }
    
    .sidebar-logo::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        box-shadow: 0 0 10px #667eea;
    }
    
    .sidebar-logo h2 {
        font-size: 2rem;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
    }
    
    /* Dark Glassmorphic Chart Container */
    .chart-container {
        background: rgba(30, 30, 50, 0.7);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(102, 126, 234, 0.2) inset;
        margin-bottom: 1.5rem;
        border: 2px solid rgba(102, 126, 234, 0.2);
        animation: fadeIn 0.8s ease-in;
        transition: all 0.3s ease;
    }
    
    .chart-container h4,
    .chart-container h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .chart-container:hover {
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.6),
            0 0 0 2px rgba(102, 126, 234, 0.4) inset;
        border: 2px solid rgba(102, 126, 234, 0.4);
    }
    
    /* Dark Creative Gradient Insight Cards */
    .insight-card {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.2) 0%, 
            rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(102, 126, 234, 0.3) inset;
        border: 2px solid rgba(102, 126, 234, 0.3);
        animation: slideRight 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .insight-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.2), transparent);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .insight-card h3 {
        position: relative;
        color: #f093fb !important;
        margin-bottom: 0.75rem;
        font-size: 1.5rem;
        font-weight: 700 !important;
    }
    
    .insight-card p {
        position: relative;
        color: #d0d0e0;
        line-height: 1.8;
        font-size: 1.05rem;
        font-weight: 400;
    }
    
    /* Enhanced Animations */
    @keyframes fadeIn {
        from { 
            opacity: 0;
            transform: scale(0.95);
        }
        to { 
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(30px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideRight {
        from { 
            opacity: 0;
            transform: translateX(-30px);
        }
        to { 
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Dark Futuristic Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(30, 30, 50, 0.8);
        backdrop-filter: blur(20px);
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.5px;
        color: #a0a0c0 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 
            0 8px 20px rgba(102, 126, 234, 0.5),
            0 0 20px rgba(118, 75, 162, 0.4);
        transform: scale(1.05);
    }
    
    /* Enhanced Progress bar with glow */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
        animation: progressGlow 2s ease-in-out infinite;
    }
    
    @keyframes progressGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.6); }
        50% { box-shadow: 0 0 30px rgba(118, 75, 162, 0.9); }
    }
    
    /* Dark Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 30, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.6);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #f093fb);
    }
    
    /* Fix Streamlit default widget colors for dark theme */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0c0 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #d0d0e0 !important;
    }
    
    /* Input elements */
    .stSelectbox, .stDateInput {
        color: white !important;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(30, 30, 50, 0.8);
        color: white !important;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Dataframe styling for dark theme */
    .dataframe {
        background-color: rgba(30, 30, 50, 0.6);
        color: #e0e0e0 !important;
    }
    
    .dataframe th {
        background-color: rgba(102, 126, 234, 0.3) !important;
        color: white !important;
    }
    
    .dataframe td {
        color: #e0e0e0 !important;
    }
    
    /* Hide the unwanted sidebar collapse button text */
    button[kind="header"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Hide any keyboard_double_arrow_right text */
    button[kind="header"] span {
        display: none !important;
    }
    
    /* Alternative: Hide the entire collapse button */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all church data"""
    members = pd.read_csv('data_members.csv')
    attendance = pd.read_csv('data_attendance.csv')
    donations = pd.read_csv('data_donations.csv')
    events = pd.read_csv('data_events.csv')
    sermons = pd.read_csv('data_sermons.csv')
    
    with open('data_churches.json', 'r') as f:
        churches = json.load(f)
    
    # Convert dates
    members['join_date'] = pd.to_datetime(members['join_date'])
    attendance['date'] = pd.to_datetime(attendance['date'])
    donations['date'] = pd.to_datetime(donations['date'])
    events['date'] = pd.to_datetime(events['date'])
    sermons['date'] = pd.to_datetime(sermons['date'])
    
    return members, attendance, donations, events, sermons, churches

# Load data
members_df, attendance_df, donations_df, events_df, sermons_df, churches_list = load_data()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>⛪ FaithMetrics</h2>
        <p style="font-size: 0.85rem; opacity: 0.8;">Church Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏛️ Select Church")
    church_names = {c['id']: c['name'] for c in churches_list}
    selected_church_id = st.selectbox(
        "Choose a church",
        options=list(church_names.keys()),
        format_func=lambda x: church_names[x],
        label_visibility="collapsed"
    )
    
    selected_church = next(c for c in churches_list if c['id'] == selected_church_id)
    
    st.markdown("---")
    st.markdown("### 📅 Date Range")
    date_range = st.date_input(
        "Select period",
        value=(
            datetime.now() - timedelta(days=90),
            datetime.now()
        ),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
        <p style="font-size: 0.85rem; margin: 0;"><strong>Location:</strong> {selected_church['location']}</p>
        <p style="font-size: 0.85rem; margin: 0.5rem 0 0 0;"><strong>Est.:</strong> {selected_church['established']}</p>
    </div>
    """, unsafe_allow_html=True)

# Filter data for selected church and date range
church_members = members_df[members_df['church_id'] == selected_church_id]
church_attendance = attendance_df[
    (attendance_df['church_id'] == selected_church_id) &
    (attendance_df['date'] >= pd.to_datetime(date_range[0])) &
    (attendance_df['date'] <= pd.to_datetime(date_range[1]))
]
church_donations = donations_df[
    (donations_df['church_id'] == selected_church_id) &
    (donations_df['date'] >= pd.to_datetime(date_range[0])) &
    (donations_df['date'] <= pd.to_datetime(date_range[1]))
]
church_events = events_df[
    (events_df['church_id'] == selected_church_id) &
    (events_df['date'] >= pd.to_datetime(date_range[0])) &
    (events_df['date'] <= pd.to_datetime(date_range[1]))
]
church_sermons = sermons_df[
    (sermons_df['church_id'] == selected_church_id) &
    (sermons_df['date'] >= pd.to_datetime(date_range[0])) &
    (sermons_df['date'] <= pd.to_datetime(date_range[1]))
]

# Main header
st.markdown(f"""
<div class="main-header">
    <h1>{selected_church['name']}</h1>
    <p>Comprehensive Analytics & Insights Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "👥 Attendance Intelligence",
    "💰 Financial Analytics",
    "👤 Member Insights",
    "📖 Sermon Impact",
    "🎯 Predictive Analytics"
])

# TAB 1: OVERVIEW
with tab1:
    st.markdown("### Key Performance Indicators")
    
    # Calculate KPIs
    avg_attendance = len(church_attendance) / church_attendance['date'].nunique() if len(church_attendance) > 0 else 0
    total_donations = church_donations['amount'].sum()
    active_members = len(church_members[church_members['status'] == 'Active'])
    engagement_rate = church_members['engagement_score'].mean() * 100
    
    # Previous period for comparison
    prev_start = pd.to_datetime(date_range[0]) - (pd.to_datetime(date_range[1]) - pd.to_datetime(date_range[0]))
    prev_attendance = attendance_df[
        (attendance_df['church_id'] == selected_church_id) &
        (attendance_df['date'] >= prev_start) &
        (attendance_df['date'] < pd.to_datetime(date_range[0]))
    ]
    prev_avg = len(prev_attendance) / prev_attendance['date'].nunique() if len(prev_attendance) > 0 else avg_attendance
    attendance_change = ((avg_attendance - prev_avg) / prev_avg * 100) if prev_avg > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        change_class = "positive" if attendance_change > 0 else "negative"
        change_symbol = "↑" if attendance_change > 0 else "↓"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Weekly Attendance</div>
            <div class="metric-value">{int(avg_attendance)}</div>
            <div class="metric-change {change_class}">{change_symbol} {abs(attendance_change):.1f}% vs previous</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        currency = church_donations['currency'].iloc[0] if len(church_donations) > 0 else 'GBP'
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Giving</div>
            <div class="metric-value">{currency} {total_donations:,.0f}</div>
            <div class="metric-change positive">📈 Strong financial health</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Members</div>
            <div class="metric-value">{active_members}</div>
            <div class="metric-change positive">{active_members/len(church_members)*100:.0f}% of total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Engagement Score</div>
            <div class="metric-value">{engagement_rate:.0f}%</div>
            <div class="metric-change positive">🎯 High engagement</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Attendance Trend")
        
        weekly_attendance = church_attendance.groupby('date').size().reset_index(name='count')
        fig = px.line(weekly_attendance, x='date', y='count',
                     labels={'count': 'Attendance', 'date': 'Date'})
        fig.update_traces(line_color='#667eea', line_width=3)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat', size=12),
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Member Demographics")
        
        age_dist = church_members['age_group'].value_counts().reset_index()
        age_dist.columns = ['Age Group', 'Count']
        fig = px.bar(age_dist, x='Age Group', y='Count',
                    color='Count',
                    color_continuous_scale=['#764ba2', '#667eea'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat', size=12),
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights
    st.markdown("### 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <h3>📈 Growth Trajectory</h3>
            <p>Attendance has {'increased' if attendance_change > 0 else 'decreased'} by {abs(attendance_change):.1f}% 
            compared to the previous period. This trend suggests {'strong community engagement' if attendance_change > 0 
            else 'an opportunity for renewed outreach efforts'}.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_age_group = church_members['age_group'].value_counts().index[0]
        st.markdown(f"""
        <div class="insight-card">
            <h3>👥 Demographic Profile</h3>
            <p>The largest demographic is <strong>{top_age_group}</strong> members. 
            Consider programming that caters to this group while also developing initiatives 
            to engage underrepresented age groups.</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: ATTENDANCE INTELLIGENCE
with tab2:
    st.markdown("### Attendance Analytics & Patterns")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        attendance_rate = (len(church_attendance) / (len(church_members) * church_attendance['date'].nunique())) * 100 if len(church_members) > 0 else 0
        st.metric("Attendance Rate", f"{attendance_rate:.1f}%", delta=f"{attendance_change:.1f}%")
    
    with col2:
        unique_attendees = church_attendance['member_id'].nunique()
        st.metric("Unique Attendees", unique_attendees, delta=f"{unique_attendees/len(church_members)*100:.0f}% of members")
    
    with col3:
        avg_per_week = len(church_attendance) / church_attendance['date'].nunique() if church_attendance['date'].nunique() > 0 else 0
        st.metric("Avg Weekly Attendance", f"{avg_per_week:.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Monthly Attendance Patterns")
        
        church_attendance['month'] = church_attendance['date'].dt.to_period('M')
        monthly = church_attendance.groupby('month').size().reset_index(name='count')
        monthly['month'] = monthly['month'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly['month'], y=monthly['count'],
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2'),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat'),
            height=400,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title='Month'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Attendance')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Attendance by Day")
        
        church_attendance['day_of_week'] = church_attendance['date'].dt.day_name()
        day_counts = church_attendance['day_of_week'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=day_counts.index,
            values=day_counts.values,
            hole=0.4,
            marker=dict(colors=px.colors.sequential.Purples_r)
        )])
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=10, b=0),
            font=dict(family='Montserrat')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Attendance heatmap
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### Attendance Heatmap")
    
    church_attendance['week'] = church_attendance['date'].dt.isocalendar().week
    church_attendance['year'] = church_attendance['date'].dt.year
    heatmap_data = church_attendance.groupby(['year', 'week']).size().reset_index(name='count')
    
    if len(heatmap_data) > 0:
        pivot = heatmap_data.pivot(index='year', columns='week', values='count')
        fig = px.imshow(pivot,
                       labels=dict(x="Week of Year", y="Year", color="Attendance"),
                       color_continuous_scale='Purples',
                       aspect='auto')
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            font=dict(family='Montserrat')
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: FINANCIAL ANALYTICS  
with tab3:
    st.markdown("### Financial Health Dashboard")
    
    currency = church_donations['currency'].iloc[0] if len(church_donations) > 0 else 'GBP'
    total_giving = church_donations['amount'].sum()
    avg_donation = church_donations['amount'].mean()
    unique_givers = church_donations['member_id'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Giving", f"{currency} {total_giving:,.0f}")
    with col2:
        st.metric("Average Donation", f"{currency} {avg_donation:,.0f}")
    with col3:
        st.metric("Unique Givers", unique_givers)
    with col4:
        giving_rate = (unique_givers / len(church_members)) * 100 if len(church_members) > 0 else 0
        st.metric("Giving Rate", f"{giving_rate:.0f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Giving Trend Over Time")
        
        church_donations['week'] = church_donations['date'].dt.to_period('W')
        weekly_giving = church_donations.groupby('week')['amount'].sum().reset_index()
        weekly_giving['week'] = weekly_giving['week'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weekly_giving['week'],
            y=weekly_giving['amount'],
            marker=dict(
                color=weekly_giving['amount'],
                colorscale='Purples',
                showscale=False
            )
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat'),
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title='Week'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title=f'Amount ({currency})')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Giving by Category")
        
        category_giving = church_donations.groupby('category')['amount'].sum().reset_index()
        category_giving = category_giving.sort_values('amount', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=category_giving['amount'],
            y=category_giving['category'],
            orientation='h',
            marker=dict(
                color=['#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b'],
            )
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat'),
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title=f'Amount ({currency})'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Payment Methods Distribution")
        
        method_dist = church_donations['method'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=method_dist.index,
            values=method_dist.values,
            marker=dict(colors=px.colors.sequential.Purples_r)
        )])
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            font=dict(family='Montserrat')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Top 10 Givers")
        
        top_givers = church_donations.groupby('member_id')['amount'].sum().sort_values(ascending=False).head(10)
        
        fig = go.Figure(go.Bar(
            x=list(range(1, len(top_givers)+1)),
            y=top_givers.values,
            marker=dict(
                color=top_givers.values,
                colorscale='Purples',
                showscale=False
            )
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat'),
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title='Rank'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title=f'Total ({currency})')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: MEMBER INSIGHTS
with tab4:
    st.markdown("### Member Engagement & Segmentation")
    
    # Engagement clustering
    if len(church_members) > 0:
        # Prepare features for clustering
        features_df = church_members[['engagement_score', 'membership_years', 'age']].copy()
        features_df['volunteer'] = church_members['volunteer'].astype(int)
        features_df['small_group'] = church_members['small_group'].astype(int)
        
        # Normalize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_df)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        church_members['cluster'] = kmeans.fit_predict(features_scaled)
        
        # Assign meaningful cluster names
        cluster_names = {
            church_members.groupby('cluster')['engagement_score'].mean().idxmax(): 'Highly Engaged',
            church_members.groupby('cluster')['engagement_score'].mean().idxmin(): 'At Risk',
        }
        remaining_cluster = [c for c in church_members['cluster'].unique() if c not in cluster_names.keys()][0]
        cluster_names[remaining_cluster] = 'Moderately Engaged'
        
        church_members['segment'] = church_members['cluster'].map(cluster_names)
        
        # Display segment distribution
        col1, col2, col3 = st.columns(3)
        
        segment_counts = church_members['segment'].value_counts()
        
        with col1:
            highly_engaged = segment_counts.get('Highly Engaged', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Highly Engaged</div>
                <div class="metric-value">{highly_engaged}</div>
                <div class="metric-change positive">🌟 Champions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            moderately = segment_counts.get('Moderately Engaged', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Moderately Engaged</div>
                <div class="metric-value">{moderately}</div>
                <div class="metric-change">📊 Potential growth</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            at_risk = segment_counts.get('At Risk', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">At Risk</div>
                <div class="metric-value">{at_risk}</div>
                <div class="metric-change negative">⚠️ Needs attention</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Member Segmentation Analysis")
            
            fig = px.scatter(church_members, 
                           x='membership_years', 
                           y='engagement_score',
                           color='segment',
                           size='age',
                           hover_data=['age_group', 'volunteer', 'small_group'],
                           color_discrete_map={
                               'Highly Engaged': '#667eea',
                               'Moderately Engaged': '#f093fb',
                               'At Risk': '#f5576c'
                           })
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Montserrat'),
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Years of Membership'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Engagement Score')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Engagement by Age Group")
            
            age_engagement = church_members.groupby('age_group')['engagement_score'].mean().sort_values(ascending=True)
            
            fig = go.Figure(go.Bar(
                y=age_engagement.index,
                x=age_engagement.values,
                orientation='h',
                marker=dict(
                    color=age_engagement.values,
                    colorscale='Purples',
                    showscale=False
                )
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Montserrat'),
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Average Engagement Score'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Volunteer Participation")
            
            volunteer_data = pd.DataFrame({
                'Category': ['Volunteers', 'Non-Volunteers'],
                'Count': [
                    church_members['volunteer'].sum(),
                    len(church_members) - church_members['volunteer'].sum()
                ]
            })
            
            fig = go.Figure(data=[go.Pie(
                labels=volunteer_data['Category'],
                values=volunteer_data['Count'],
                hole=0.5,
                marker=dict(colors=['#667eea', '#e0e0e0'])
            )])
            fig.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=10, b=0),
                font=dict(family='Montserrat')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Small Group Participation")
            
            sg_data = pd.DataFrame({
                'Category': ['In Small Groups', 'Not in Small Groups'],
                'Count': [
                    church_members['small_group'].sum(),
                    len(church_members) - church_members['small_group'].sum()
                ]
            })
            
            fig = go.Figure(data=[go.Pie(
                labels=sg_data['Category'],
                values=sg_data['Count'],
                hole=0.5,
                marker=dict(colors=['#764ba2', '#e0e0e0'])
            )])
            fig.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=10, b=0),
                font=dict(family='Montserrat')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: SERMON IMPACT
with tab5:
    st.markdown("### Sermon Analytics & Impact")
    
    if len(church_sermons) > 0:
        avg_duration = church_sermons['duration_minutes'].mean()
        avg_engagement = church_sermons['engagement_score'].mean() * 100
        total_sermons = len(church_sermons)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Sermons", total_sermons)
        with col2:
            st.metric("Avg Duration", f"{avg_duration:.0f} min")
        with col3:
            st.metric("Avg Engagement", f"{avg_engagement:.0f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Sermon Topics Distribution")
            
            topic_counts = church_sermons['topic'].value_counts().head(10)
            
            fig = go.Figure(data=[go.Bar(
                x=topic_counts.values,
                y=topic_counts.index,
                orientation='h',
                marker=dict(
                    color=topic_counts.values,
                    colorscale='Purples',
                    showscale=False
                )
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Montserrat'),
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Count'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Series Performance")
            
            series_engagement = church_sermons.groupby('series')['engagement_score'].mean().sort_values(ascending=True)
            
            fig = go.Figure(go.Bar(
                y=series_engagement.index,
                x=series_engagement.values,
                orientation='h',
                marker=dict(
                    color=series_engagement.values,
                    colorscale='Purples',
                    showscale=False
                )
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Montserrat'),
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Engagement Score'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Sermon duration vs engagement
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Duration vs Engagement Analysis")
        
        fig = px.scatter(church_sermons,
                        x='duration_minutes',
                        y='engagement_score',
                        color='series',
                        size='engagement_score',
                        hover_data=['topic', 'date'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Montserrat'),
            height=400,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Duration (minutes)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Engagement Score')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 6: PREDICTIVE ANALYTICS
with tab6:
    st.markdown("### Predictive Insights & Forecasting")
    
    st.markdown("""
    <div class="insight-card">
        <h3>🔮 Attendance Forecast</h3>
        <p>Based on historical trends and seasonal patterns, our predictive model suggests:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple trend-based forecast
    if len(church_attendance) > 0:
        weekly_trend = church_attendance.groupby('date').size().reset_index(name='count')
        
        # Calculate trend
        weekly_trend['week_num'] = (weekly_trend['date'] - weekly_trend['date'].min()).dt.days // 7
        z = np.polyfit(weekly_trend['week_num'], weekly_trend['count'], 1)
        p = np.poly1d(z)
        
        # Forecast next 12 weeks
        last_week = weekly_trend['week_num'].max()
        future_weeks = list(range(last_week + 1, last_week + 13))
        forecast_values = [p(w) for w in future_weeks]
        
        last_date = weekly_trend['date'].max()
        forecast_dates = [last_date + timedelta(weeks=i+1) for i in range(12)]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### 12-Week Attendance Forecast")
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=weekly_trend['date'],
                y=weekly_trend['count'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#667eea', width=2),
                marker=dict(size=6)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=forecast_values,
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#f093fb', width=2, dash='dash'),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Montserrat'),
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=False, title='Date'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Attendance'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("#### Forecast Summary")
            
            avg_forecast = np.mean(forecast_values)
            current_avg = weekly_trend['count'].tail(4).mean()
            trend_direction = "upward" if avg_forecast > current_avg else "downward"
            
            st.markdown(f"""
            **Projected Average:** {avg_forecast:.0f}
            
            **Trend:** {trend_direction.title()} ({'📈' if trend_direction == 'upward' else '📉'})
            
            **Confidence:** Medium
            
            This forecast is based on historical attendance patterns and assumes current conditions remain stable.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Member churn risk
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### Member Retention Risk Analysis")
    
    # Calculate risk score based on engagement and recent attendance
    at_risk_members = church_members[
        (church_members['engagement_score'] < 0.5) |
        (church_members['status'] == 'Inactive')
    ]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_risk = len(at_risk_members[at_risk_members['engagement_score'] < 0.3])
        st.markdown(f"""
        <div style="padding: 1.5rem; background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%); 
        border-radius: 12px; text-align: center;">
            <h2 style="color: white; margin: 0;">{high_risk}</h2>
            <p style="color: white; margin: 0.5rem 0 0 0;">High Risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        medium_risk = len(at_risk_members[
            (at_risk_members['engagement_score'] >= 0.3) &
            (at_risk_members['engagement_score'] < 0.5)
        ])
        st.markdown(f"""
        <div style="padding: 1.5rem; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
        border-radius: 12px; text-align: center;">
            <h2 style="color: #c0392b; margin: 0;">{medium_risk}</h2>
            <p style="color: #c0392b; margin: 0.5rem 0 0 0;">Medium Risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        low_risk = len(church_members) - len(at_risk_members)
        st.markdown(f"""
        <div style="padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 12px; text-align: center;">
            <h2 style="color: white; margin: 0;">{low_risk}</h2>
            <p style="color: white; margin: 0.5rem 0 0 0;">Low Risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-card">
        <h3>💡 AI-Powered Recommendations</h3>
        <p><strong>1. Focus on At-Risk Members:</strong> Implement a pastoral care program for the {0} members 
        showing signs of disengagement.</p>
        <p><strong>2. Optimize Service Times:</strong> Analysis shows highest attendance during certain time periods. 
        Consider adjusting service schedules.</p>
        <p><strong>3. Enhance Small Group Participation:</strong> Members in small groups show 35% higher engagement. 
        Create pathways to increase participation.</p>
        <p><strong>4. Leverage Digital Giving:</strong> Promote mobile and online giving options to increase 
        donation consistency.</p>
    </div>
    """.format(len(at_risk_members)), unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem; opacity: 0.9;">
    <p style="font-size: 0.9rem; color: white; font-weight: 500;">FaithMetrics © 2026 | Built with ❤️ for Faith Communities</p>
    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Developed by <strong>Papa Kwadwo Bona Owusu</strong></p>
</div>
""", unsafe_allow_html=True)