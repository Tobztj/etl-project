import pandas as pd
import ast

def clean_data(df):

    # Explode the 'policy_type' column if it contains a string representation of a dictionary
    first_df = df.copy()

    # Deduplicate the DataFrame based on PolicyId, CustomerId, and EventTimestamp
    first_df = first_df.drop_duplicates(subset=['policy_id', 'customer_id', 'event_timestamp'])

    # Convert the 'policy_type' string to a dictionary
    first_df['policy_type'] = first_df['policy_type'].apply(ast.literal_eval)

    # Extract 'type' and 'brand' from the 'policy_type' dictionary
    first_df['PolicyType'] = first_df['policy_type'].apply(lambda x: x.get('type'))
    first_df['PolicyBrand'] = first_df['policy_type'].apply(lambda x: x.get('brand'))

    # Drop the original 'policy_type' column
    first_df = first_df.drop(columns=['policy_type'])

    # Rename columns to match table definition in the database
    first_df = first_df.rename(columns={
        'policy_id': 'PolicyId',
        'customer_id': 'CustomerId',
        'event_type': 'EventType',
        'event_timestamp': 'EventTimestamp',
        'premium_amount': 'PremiumAmount',
        'coverage_amount': 'CoverageAmount',
        'region': 'Region',
        'age_of_insured': 'AgeOfInsured',
        'source_file': 'SourceFile'
    })

    # Reorder columns if needed
    first_df = first_df[['PolicyId', 'CustomerId', 'EventType', 'EventTimestamp',
                     'PolicyType', 'PolicyBrand', 'PremiumAmount',
                     'CoverageAmount', 'AgeOfInsured', 'Region', 'SourceFile']]

    # Replace None values with "Unknown" for PolicyType and PolicyBrand
    first_df['PolicyType'] = first_df['PolicyType'].fillna("unknown")
    first_df['PolicyBrand'] = first_df['PolicyBrand'].fillna("Unknown")

    # Replace None values with 0 for numeric and integer columns
    numeric_columns = ['PremiumAmount', 'CoverageAmount']
    mandatory_values = ['purchase', 'renewal']
    for col in numeric_columns:
        # Set column to 0.00 where EventType is not in mandatory_values or value is <= 0
        first_df.loc[((first_df[col].isnull()) | (first_df[col] <= 0)) & (~first_df["EventType"].isin(mandatory_values)), col] = 0.00


    # Ensure AgeOfInsured is set to 0 if it is None or less than or equal to 0
    first_df.loc[((first_df['AgeOfInsured'].isnull()) | (first_df['AgeOfInsured'] <= 0)) & (~first_df["EventType"].isin(mandatory_values)), 'AgeOfInsured'] = 0


    final_df = first_df

    return final_df