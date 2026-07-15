import pandas as pd 

ds = pd.read_csv("customer_shopping_behavior.csv")
print(ds)
print(ds.head())
print(ds.shape)
print(ds.info())
print(ds.columns)
print(ds.describe)

print("Missing Value :\n", ds.isnull().sum())  #checking null value 

ds["Review Rating"] = ds.groupby("Category")["Review Rating"].transform(lambda x: x.fillna(x.median()))
print("Missing Value :\n", ds.isnull().sum())   #checking null value again after filling it 

ds.columns = ds.columns.str.lower()  # turning all column name into lowercase to easily remember 
ds.columns = ds.columns.str.replace(" ","_")  #replacing space betw name by _ 
ds = ds.rename(columns={"purchase_amount_(usd)":"purchase_amount"}) #rename the column 
print(ds.columns)

ds.to_csv("customer_shopping_behavior.csv" , index=False)  #to update the csv file 

# Creating age group::

labels = ["Young","Adults","Middle-Age","Senior"]
ds["age_group"] = pd.qcut(ds["age"] , q=4 ,labels=labels)
print(ds[["age","age_group"]])

ds.to_csv("customer_shopping_behavior.csv" , index=False) 
print(ds[(ds['age_group']=="Senior")]) # condition checking (filter)

# creating column purchase_frequency_days

frequency_mapping = {
    'Weekly':7,
    'Fortnightly':14,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months' :90 
}

ds["purchase_frequency_days"] = ds["frequency_of_purchases"].map(frequency_mapping)
ds.to_csv("customer_shopping_behavior.csv" , index=False)    #file update
print(ds[["purchase_frequency_days","frequency_of_purchases"]].head(15))  #checking

# in dataset there 2 column name discount and promo code used if both are same then we need to remove one of it 

print((ds["discount_applied"]==ds["promo_code_used"]).all())  #checking if both same or not (Output : if True means same)

ds =ds.drop("promo_code_used" , axis=1)
ds.to_csv("customer_shopping_behavior.csv" , index=False)
print(ds.columns)

# Connecting python file with mysql

import csv
import mysql.connector

# Step 1: Establish the connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="shivam",
    database="customer_analysis"
)

cursor = db_connection.cursor()
csv_file_path = 'customer_shopping_behavior.csv'

# Step 2: Open and read the CSV
with open(csv_file_path, mode='r') as file:
    csv_data = csv.reader(file)
    
    # Skip the header row (highly recommended since your CSV likely has these column names at the top)
    next(csv_data) 
    
    # Step 3: Loop through and insert
    for row in csv_data:
        # Update the query to include all 19 columns and 19 %s placeholders
        # Update the query to include purchase_frequency_days at the end
        sql_insert_query = """
            INSERT INTO customer_purchases (
                customer_id, age, gender, item_purchased, category, 
                purchase_amount, location, size, color, season, 
                review_rating, subscription_status, shipping_type, 
                discount_applied, previous_purchases, payment_method, 
                frequency_of_purchases, age_group, purchase_frequency_days
            ) 
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        # Execute the query with the current row's data
        cursor.execute(sql_insert_query, row)

# Step 4: Commit and close
db_connection.commit()
print(f"Dataset successfully imported into the customer_purchases table!")

cursor.close()
db_connection.close()