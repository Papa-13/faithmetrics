"""
Church Analytics Platform - Synthetic Data Generator
Generates realistic multi-church data for FaithMetrics platform
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Church configurations
CHURCHES = [
    {
        'id': 1,
        'name': 'Edgeware Methodist Church',
        'location': 'London, UK',
        'denomination': 'Methodist',
        'established': 1895,
        'avg_attendance': 180,
        'member_count': 250
    },
    {
        'id': 2,
        'name': 'Grace Community Church',
        'location': 'Accra, Ghana',
        'denomination': 'Pentecostal',
        'established': 2005,
        'avg_attendance': 320,
        'member_count': 450
    },
    {
        'id': 3,
        'name': 'St. Paul\'s Anglican',
        'location': 'Birmingham, UK',
        'denomination': 'Anglican',
        'established': 1920,
        'avg_attendance': 145,
        'member_count': 200
    },
    {
        'id': 4,
        'name': 'New Life Baptist',
        'location': 'Kumasi, Ghana',
        'denomination': 'Baptist',
        'established': 2010,
        'avg_attendance': 280,
        'member_count': 380
    },
    {
        'id': 5,
        'name': 'Trinity Fellowship',
        'location': 'Manchester, UK',
        'denomination': 'Non-denominational',
        'established': 2015,
        'avg_attendance': 95,
        'member_count': 130
    }
]

# Generate date range (2 years of data)
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=730)

def generate_members():
    """Generate member profiles for all churches"""
    members = []
    member_id = 1
    
    for church in CHURCHES:
        num_members = church['member_count']
        
        for _ in range(num_members):
            age = int(np.random.gamma(3, 15) + 18)  # Age distribution skewed toward adults
            age = min(age, 95)
            
            # Age-based engagement patterns
            if age < 25:
                engagement_base = np.random.uniform(0.5, 0.75)
                age_group = 'Youth (18-24)'
            elif age < 40:
                engagement_base = np.random.uniform(0.65, 0.85)
                age_group = 'Young Adult (25-39)'
            elif age < 60:
                engagement_base = np.random.uniform(0.75, 0.95)
                age_group = 'Adult (40-59)'
            else:
                engagement_base = np.random.uniform(0.70, 0.90)
                age_group = 'Senior (60+)'
            
            join_date = START_DATE + timedelta(days=random.randint(0, 730))
            
            members.append({
                'member_id': member_id,
                'church_id': church['id'],
                'age': age,
                'age_group': age_group,
                'gender': random.choice(['Male', 'Female']),
                'join_date': join_date,
                'membership_years': (END_DATE - join_date).days / 365.25,
                'engagement_score': engagement_base,
                'volunteer': random.random() < 0.35,
                'small_group': random.random() < 0.45,
                'status': random.choices(['Active', 'Inactive', 'New'], weights=[0.75, 0.15, 0.10])[0]
            })
            member_id += 1
    
    return pd.DataFrame(members)

def generate_attendance(members_df):
    """Generate weekly attendance records"""
    attendance_records = []
    
    # Generate Sundays
    current_date = START_DATE
    sundays = []
    while current_date <= END_DATE:
        if current_date.weekday() == 6:  # Sunday
            sundays.append(current_date)
        current_date += timedelta(days=1)
    
    for church in CHURCHES:
        church_members = members_df[members_df['church_id'] == church['id']]
        base_attendance = church['avg_attendance']
        
        for sunday in sundays:
            # Seasonal variations
            month = sunday.month
            if month in [12, 4]:  # Christmas, Easter
                seasonal_factor = 1.3
            elif month in [7, 8]:  # Summer vacation
                seasonal_factor = 0.75
            else:
                seasonal_factor = 1.0
            
            # Trend (slight growth over time)
            days_from_start = (sunday - START_DATE).days
            trend_factor = 1 + (days_from_start / 3650)  # 10% growth over 2 years
            
            # Random variation
            random_factor = np.random.normal(1.0, 0.15)
            
            expected_attendance = base_attendance * seasonal_factor * trend_factor * random_factor
            expected_attendance = int(max(expected_attendance, base_attendance * 0.5))
            
            # Determine which members attend
            for _, member in church_members.iterrows():
                attend_probability = member['engagement_score'] * seasonal_factor * random_factor
                
                if random.random() < attend_probability:
                    attendance_records.append({
                        'church_id': church['id'],
                        'member_id': member['member_id'],
                        'date': sunday,
                        'service_type': 'Sunday Service',
                        'attended': True
                    })
    
    return pd.DataFrame(attendance_records)

def generate_donations(members_df):
    """Generate donation records"""
    donations = []
    donation_id = 1
    
    for church in CHURCHES:
        church_members = members_df[members_df['church_id'] == church['id']]
        
        # Currency based on location
        currency = 'GBP' if 'UK' in church['location'] else 'GHS'
        exchange_rate = 1 if currency == 'GBP' else 12.5
        
        # Generate weekly donations
        current_date = START_DATE
        while current_date <= END_DATE:
            if current_date.weekday() == 6:  # Sunday
                # Regular givers (40% of active members)
                regular_givers = church_members[
                    (church_members['status'] == 'Active') & 
                    (church_members['engagement_score'] > 0.65)
                ].sample(frac=0.4)
                
                for _, member in regular_givers.iterrows():
                    if random.random() < 0.85:  # 85% consistency
                        # Age and engagement-based giving
                        if member['age'] < 30:
                            base_amount = np.random.gamma(2, 15)
                        elif member['age'] < 50:
                            base_amount = np.random.gamma(3, 25)
                        else:
                            base_amount = np.random.gamma(3, 30)
                        
                        amount = base_amount * exchange_rate
                        
                        # Special occasions boost
                        if current_date.month == 12:
                            amount *= np.random.uniform(1.5, 2.5)
                        
                        # Payment method based on location
                        if currency == 'GBP':  # UK churches
                            payment_method = random.choices(
                                ['Cash', 'Bank Transfer', 'Card', 'Direct Debit'],
                                weights=[0.20, 0.40, 0.35, 0.05]
                            )[0]
                        else:  # Ghana churches
                            payment_method = random.choices(
                                ['Cash', 'Bank Transfer', 'Card', 'Mobile Money'],
                                weights=[0.30, 0.25, 0.20, 0.25]
                            )[0]
                        
                        donations.append({
                            'donation_id': donation_id,
                            'church_id': church['id'],
                            'member_id': member['member_id'],
                            'date': current_date,
                            'amount': round(amount, 2),
                            'currency': currency,
                            'category': random.choices(
                                ['Tithe', 'Offering', 'Building Fund', 'Missions', 'Special'],
                                weights=[0.50, 0.25, 0.10, 0.10, 0.05]
                            )[0],
                            'method': payment_method
                        })
                        donation_id += 1
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(donations)

def generate_events():
    """Generate church events"""
    events = []
    event_id = 1
    
    event_types = [
        {'name': 'Prayer Meeting', 'frequency': 'weekly', 'avg_attendance_pct': 0.25},
        {'name': 'Bible Study', 'frequency': 'weekly', 'avg_attendance_pct': 0.30},
        {'name': 'Youth Service', 'frequency': 'monthly', 'avg_attendance_pct': 0.40},
        {'name': 'Women\'s Fellowship', 'frequency': 'monthly', 'avg_attendance_pct': 0.20},
        {'name': 'Men\'s Breakfast', 'frequency': 'monthly', 'avg_attendance_pct': 0.15},
        {'name': 'Community Outreach', 'frequency': 'quarterly', 'avg_attendance_pct': 0.35},
        {'name': 'Church Retreat', 'frequency': 'annual', 'avg_attendance_pct': 0.50},
    ]
    
    for church in CHURCHES:
        for event_type in event_types:
            current_date = START_DATE
            
            while current_date <= END_DATE:
                expected_attendance = int(church['member_count'] * event_type['avg_attendance_pct'])
                actual_attendance = int(expected_attendance * np.random.uniform(0.7, 1.3))
                
                events.append({
                    'event_id': event_id,
                    'church_id': church['id'],
                    'event_name': event_type['name'],
                    'date': current_date,
                    'expected_attendance': expected_attendance,
                    'actual_attendance': actual_attendance,
                    'attendance_rate': actual_attendance / expected_attendance if expected_attendance > 0 else 0
                })
                event_id += 1
                
                # Increment based on frequency
                if event_type['frequency'] == 'weekly':
                    current_date += timedelta(days=7)
                elif event_type['frequency'] == 'monthly':
                    current_date += timedelta(days=30)
                elif event_type['frequency'] == 'quarterly':
                    current_date += timedelta(days=90)
                else:  # annual
                    current_date += timedelta(days=365)
    
    return pd.DataFrame(events)

def generate_sermons():
    """Generate sermon data with topics"""
    sermons = []
    sermon_id = 1
    
    sermon_series = [
        {'title': 'Faith in Action', 'topics': ['Faith', 'Works', 'Service', 'Love']},
        {'title': 'The Gospel of Matthew', 'topics': ['Scripture', 'Jesus', 'Discipleship', 'Kingdom']},
        {'title': 'Prayers That Transform', 'topics': ['Prayer', 'Faith', 'Miracles', 'Hope']},
        {'title': 'Family Matters', 'topics': ['Family', 'Marriage', 'Parenting', 'Relationships']},
        {'title': 'Financial Freedom', 'topics': ['Stewardship', 'Giving', 'Contentment', 'Trust']},
        {'title': 'Living with Purpose', 'topics': ['Purpose', 'Calling', 'Mission', 'Service']},
        {'title': 'The Holy Spirit', 'topics': ['Spirit', 'Power', 'Gifts', 'Fruit']},
    ]
    
    for church in CHURCHES:
        current_date = START_DATE
        
        while current_date <= END_DATE:
            if current_date.weekday() == 6:  # Sunday
                series = random.choice(sermon_series)
                topic = random.choice(series['topics'])
                
                sermons.append({
                    'sermon_id': sermon_id,
                    'church_id': church['id'],
                    'date': current_date,
                    'series': series['title'],
                    'topic': topic,
                    'duration_minutes': int(np.random.normal(35, 8)),
                    'engagement_score': np.random.uniform(0.65, 0.95)
                })
                sermon_id += 1
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(sermons)

# Generate all datasets
print("Generating church analytics data...")
print("=" * 50)

members_df = generate_members()
print(f"✓ Generated {len(members_df)} member records")

attendance_df = generate_attendance(members_df)
print(f"✓ Generated {len(attendance_df)} attendance records")

donations_df = generate_donations(members_df)
print(f"✓ Generated {len(donations_df)} donation records")

events_df = generate_events()
print(f"✓ Generated {len(events_df)} event records")

sermons_df = generate_sermons()
print(f"✓ Generated {len(sermons_df)} sermon records")

# Save to CSV files
members_df.to_csv('data_members.csv', index=False)
attendance_df.to_csv('data_attendance.csv', index=False)
donations_df.to_csv('data_donations.csv', index=False)
events_df.to_csv('data_events.csv', index=False)
sermons_df.to_csv('data_sermons.csv', index=False)

# Save church metadata
with open('data_churches.json', 'w') as f:
    json.dump(CHURCHES, f, indent=2)

print("\n" + "=" * 50)
print("Data generation complete!")
print("\nFiles created:")
print("  - data_members.csv")
print("  - data_attendance.csv")
print("  - data_donations.csv")
print("  - data_events.csv")
print("  - data_sermons.csv")
print("  - data_churches.json")
print("\nReady for FaithMetrics platform!")