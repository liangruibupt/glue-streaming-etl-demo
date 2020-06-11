import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext, SparkConf
from awsglue.context import GlueContext
from awsglue.job import Job
import time
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

args = getResolvedOptions(sys.argv, ['s3OutputPath'])

df = spark.sql("select w_warehouse_name, w_city,count(*) as cnt_sales, sum(cs_list_price) as total_revenue,sum(cs_net_profit_double) as total_net_profit,sum(cs_wholesale_cost) as total_cost from mysql_ingest.catalog_sales join mysql_ingest.warehouse on cs_warehouse_sk = w_warehouse_sk group by w_warehouse_name, w_city")
df.write.mode("overwrite").format("parquet").save(
    args['s3OutputPath']+"warehouse_report/")
