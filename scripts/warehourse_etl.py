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

args = getResolvedOptions(sys.argv, [
                          'tablename', 'dbuser', 'dbpassword', 'dburl', 'jdbcS3path', 's3OutputPath'])
## Construct JDBC connection options for mysql8, modify for your value
connection_mysql8_options = {
    "url": args['dburl'],
    "dbtable": args['tablename'],
    "user": args['dbuser'],
    "password": args['dbpassword'],
    #You need upload to S3
    "customJdbcDriverS3Path": args['jdbcS3path']+"mysql-connector-java-8.0.17.jar",
    "customJdbcDriverClassName": "com.mysql.cj.jdbc.Driver"}

# Read from JDBC databases with custom driver
df_warehouse = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql", connection_options=connection_mysql8_options)

# Write to S3
writer = glueContext.write_dynamic_frame.from_options(frame=df_warehouse, connection_type="s3", connection_options={
                                                      "path": args['s3OutputPath']+args['tablename']}, format="parquet")
