import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Define the schema explicitly
order_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("total_amount", StringType(), True), # Load as string first to handle "FREE" or "NAN"
    StructField("customer_email", StringType(), True)
])

@dlt.table(
    name="orders_bronze",
    comment="Raw orders data ingested from the Volume"
)
def orders_bronze():
    return (
        spark.readStream
        .format("csv")
        .option("header", "true")
        .schema(order_schema)
        .load("/Volumes/data_contract_demo/orders_data/orders_raw/raw_data/")
    )