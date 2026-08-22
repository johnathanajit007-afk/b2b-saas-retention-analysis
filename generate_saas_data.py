import numpy as np
import pandas as pd
import random
import os
from datetime import datetime, timedelta

np.random.seed(101)
random.seed(101)

# Generate 300 unique B2B SaaS accounts
n_customers = 300
customer_ids = [f"CUST-{1000 + i}" for i in range(n_customers)]

plans = ['Starter', 'Professional', 'Enterprise']
plan_mrr = {'Starter': 29, 'Professional': 99, 'Enterprise': 299}

data = []
cohort_start = datetime(2025, 1, 1)

for cust in customer_ids:
    signup_month = random.randint(0, 11)
    signup_date = cohort_start + timedelta(days=signup_month*30 + random.randint(0, 20))
    plan = random.choice(plans)
    mrr = plan_mrr[plan]
    
    max_possible_months = max(1, 12 - signup_month)
    is_early_churn = random.random() < 0.30
    
    if is_early_churn or max_possible_months < 4:
        max_months = random.randint(1, min(3, max_possible_months))
    else:
        max_months = random.randint(4, max_possible_months)
    
    for month_offset in range(max_months):
        billing_date = signup_date + timedelta(days=month_offset * 30)
        if billing_date <= datetime(2025, 12, 31):
            data.append({
                'Customer_ID': cust,
                'Subscription_Plan': plan,
                'Monthly_MRR_USD': mrr,
                'Billing_Date': billing_date.strftime("%Y-%m-%d"),
                'Signup_Date': signup_date.strftime("%Y-%m-%d")
            })

df = pd.DataFrame(data)

# Guarantees saving directly into the B2B folder alongside this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "Raw_SaaS_Billing_Logs.csv")

df.to_csv(output_path, index=False)
print(f"Successfully saved Raw_SaaS_Billing_Logs.csv to: {output_path}")