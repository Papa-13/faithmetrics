# FaithMetrics - Multi-Church Analytics & Insights Platform

## 🎯 Overview

FaithMetrics is a comprehensive analytics platform designed for faith communities to gain actionable insights from their data. Built with advanced machine learning algorithms and beautiful data visualizations, it empowers church leadership to make data-driven decisions that strengthen community engagement.

## ✨ Key Features

### 📊 **Comprehensive Analytics Dashboard**
- **Overview Metrics**: Real-time KPIs including attendance, giving, member count, and engagement scores
- **Attendance Intelligence**: Weekly/monthly trends, seasonal patterns, and attendance heatmaps
- **Financial Analytics**: Giving trends, category breakdowns, payment methods, and top donor analysis
- **Member Insights**: AI-powered segmentation using K-means clustering (Highly Engaged, Moderately Engaged, At Risk)
- **Sermon Impact**: Topic analysis, series performance, and duration vs engagement correlation
- **Predictive Analytics**: 12-week attendance forecasting and member retention risk modeling

### 🤖 **AI/ML Capabilities**
- **Member Segmentation**: Unsupervised learning (K-means) to identify engagement clusters
- **Attendance Forecasting**: Time-series trend analysis with polynomial regression
- **Risk Scoring**: Multi-factor analysis to identify at-risk members
- **Pattern Recognition**: Automated insights from historical data

### 🎨 **Elegant Design**
- Faith-inspired aesthetic with sophisticated gradients and animations
- Responsive layout optimized for all screen sizes
- Custom typography (Crimson Pro + Montserrat)
- Interactive Plotly charts with smooth transitions
- Professional color palette (#667eea, #764ba2, #f093fb)

## 📁 Project Structure

```
FaithMetrics/
├── faithmetrics_app.py          # Main Streamlit application
├── generate_church_data.py      # Synthetic data generator
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── DEPLOYMENT_GUIDE.md          # Deployment instructions
└── data/                        # Generated datasets
    ├── data_members.csv         # 1,410 member records
    ├── data_attendance.csv      # 116,166 attendance records
    ├── data_donations.csv       # 36,992 donation records
    ├── data_events.csv          # 1,485 event records
    ├── data_sermons.csv         # 520 sermon records
    └── data_churches.json       # Church metadata
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone or download the project files**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate synthetic data** (if not already present)
```bash
python generate_church_data.py
```

4. **Run the application**
```bash
streamlit run faithmetrics_app.py
```

5. **Access the dashboard**
- Open your browser to `http://localhost:8501`
- Select a church from the sidebar
- Choose your date range
- Explore the analytics tabs!

## 📊 Data Overview

### Churches Included
1. **Riverside Methodist Church** - London, UK (250 members, synthetic)
2. **Grace Community Church** - Accra, Ghana (450 members)
3. **St. Paul's Anglican** - Birmingham, UK (200 members)
4. **New Life Baptist** - Kumasi, Ghana (380 members)
5. **Trinity Fellowship** - Manchester, UK (130 members)

### Dataset Statistics
- **Total Members**: 1,410
- **Attendance Records**: 116,166 (2 years)
- **Donations**: 36,992 transactions
- **Events**: 1,485 church events
- **Sermons**: 520 sermon records
- **Time Period**: 2 years (2024-2026)

## 🔧 Technical Stack

### Core Technologies
- **Frontend Framework**: Streamlit 1.39+
- **Data Processing**: Pandas 2.2+, NumPy 2.0+
- **Visualization**: Plotly 5.18+
- **Machine Learning**: Scikit-learn 1.4+

### Key Algorithms
- **K-Means Clustering**: Member segmentation (3 clusters)
- **Polynomial Regression**: Attendance forecasting
- **StandardScaler**: Feature normalization
- **Statistical Analysis**: Trend detection, correlation analysis

## 📈 Key Metrics & Insights

### Dashboard Capabilities
- **Attendance Tracking**: Weekly patterns, monthly trends, seasonal variations
- **Financial Health**: Total giving, donor retention, category analysis
- **Member Engagement**: Active vs inactive, age distribution, volunteer participation
- **Predictive Insights**: 12-week forecasts, retention risk scores
- **Sermon Analytics**: Topic popularity, series performance, engagement correlation

### AI-Generated Insights
- Growth trajectory analysis
- Demographic profiling
- At-risk member identification
- Optimal service time recommendations
- Small group impact assessment

## 🎨 Design Philosophy

### Visual Identity
- **Primary Colors**: Purple gradients (#667eea → #764ba2)
- **Accent Colors**: Coral (#f5576c), Pink (#f093fb)
- **Typography**: Crimson Pro (headings) + Montserrat (body)
- **Animation**: Fade-in, slide-up, and slide-right effects

### User Experience
- **Progressive Disclosure**: Information revealed contextually
- **Visual Hierarchy**: Clear metric cards, chart containers
- **Responsive Design**: Adapts to all screen sizes
- **Interactive Elements**: Hover effects, smooth transitions

## 🔐 Data Privacy & Security

- **Demo data in this repository is synthetic.** The five churches, 1,410 members and all records
  under data/ are artificially generated by generate_church_data.py for demonstration.
- **Pilot.** The application has since been piloted for one month with Edgware Methodist Church
  using the church's own data. That data is held privately by the church and is not part of this
  repository.
- No personally identifiable information is stored in this repository.

## 🌟 Future Enhancements

### Potential Features
- **Email Automation**: Automated outreach to at-risk members
- **Mobile App**: Native iOS/Android applications
- **API Integration**: Connect with church management systems
- **Advanced ML**: LSTM for time-series, NLP for sermon analysis
- **Federated Learning**: Multi-church insights while preserving privacy
- **Report Generation**: Automated PDF reports for leadership

### Scalability Roadmap
- PostgreSQL database backend
- Multi-tenant SaaS architecture
- Role-based access control (RBAC)
- Real-time data synchronization
- Cloud deployment (AWS/GCP/Azure)

## 📧 Contact & Support

**Developer**: Papa Kwadwo Bona Owusu
- Building innovative solutions for faith communities
- MSc Applied AI & Data Science (Southampton Solent University)
- MSc Business Analytics (KNUST)


## 📄 License

Prototype. Contact the author before reusing or deploying.

## 🙏 Acknowledgments

- Edgware Methodist Church for piloting the application

---

**Built with ❤️ for Faith Communities**

*FaithMetrics - Empowering churches through data-driven insights*
