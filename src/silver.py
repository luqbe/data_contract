import dlt
from pyspark.sql.functions import *
@dlt.table(
    name="orders_silver",
    comment="Cleaned orders data enforced by the Data Contract"
)
# --- DATA CONTRACT ENFORCEMENT ---

# Rule 1: Critical Failure - If ID is missing, stop the pipeline
@dlt.expect_or_fail("valid_order_id", "order_id IS NOT NULL")

# Rule 2: Row Drop - If amount is negative, remove the row but keep running
@dlt.expect_or_drop("positive_amount", "cast(total_amount as double) > 0")

# Rule 3: Warning - If email is malformed, flag it in the logs but keep the data
@dlt.expect("valid_email_format", "customer_email LIKE '%@%.%'")

def orders_silver():
    return (
        dlt.readStream("data_contract_demo.orders_data.orders_bronze")
        .select(
            col("order_id").cast("string"),
            col("total_amount").cast("double"),
            col("customer_email").cast("string"),
            current_timestamp().alias("processing_time")
        )
    )