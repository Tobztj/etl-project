import pandas as pd
from app.logging.load_logger import load_logger


def load_staging_data(df, connection, schema_name, table_name):

    valid = True
    cursor = connection.cursor()

    sql = (
            f"INSERT INTO {schema_name}.{table_name} "
            "(PolicyId, CustomerId, EventType, EventTimestamp, PolicyType, PolicyBrand, PremiumAmount, CoverageAmount, AgeOfInsured, Region, SourceFile) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )

    for index, row in df.iterrows():
        try:
            test =cursor.execute(
                                    sql,
                                    row['PolicyId'], row['CustomerId'], row['EventType'],
                                    row['EventTimestamp'], row['PolicyType'], row['PolicyBrand'], row['PremiumAmount'],
                                    row['CoverageAmount'], row['AgeOfInsured'], row['Region'], row['SourceFile']
            )
            connection.commit()

        except Exception as e:
            load_logger.error(f"Error inserting row {index}: {e}")
            connection.rollback()
            valid = False
    return valid