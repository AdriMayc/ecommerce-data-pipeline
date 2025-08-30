'''
Código ilustrativo, executado no console do AWS Glue (apenas como referência).

'''

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# 1. Definir schemas explicitamente
customers_schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("registration_date", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True)
])

orders_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("order_date", StringType(), True),
    StructField("total_value", DoubleType(), True),
    StructField("payment_type", StringType(), True),
    StructField("status", StringType(), True)
])

# 2. Ler CSV do S3 (raw) com curingas para ano/mês
customers_df = spark.read.option("header", True).schema(customers_schema).csv("s3://ecommerce-data-raw-proj/raw/customers/*/*/*.csv")
orders_df    = spark.read.option("header", True).schema(orders_schema).csv("s3://ecommerce-data-raw-proj/raw/orders/*/*/*.csv")

# 3. Criar staging
stg_customers = customers_df.selectExpr(
    "customer_id",
    "customer_name",
    "email",
    "registration_date",
    "city",
    "state"
)

stg_orders = orders_df.selectExpr(
    "order_id",
    "customer_id",
    "order_date",
    "total_value",
    "payment_type",
    "status"
)

# 4. Criar marts
fact_sales   = stg_orders.filter("status = 'completed'")
dim_customers = stg_customers

# 5. Gravar em S3
stg_customers.write.mode("overwrite").parquet("s3://ecommerce-data-raw-proj/stg/customers/")
stg_orders.write.mode("overwrite").parquet("s3://ecommerce-data-raw-proj/stg/orders/")
fact_sales.write.mode("overwrite").parquet("s3://ecommerce-data-raw-proj/mart/fact_sales/")
dim_customers.write.mode("overwrite").parquet("s3://ecommerce-data-raw-proj/mart/dim_customers/")

job.commit()