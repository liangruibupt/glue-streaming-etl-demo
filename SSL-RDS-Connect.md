# Connect the RDS which SSL enabled

1. Check the JDBC Driver Version based on the link: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect.html#aws-glue-programming-etl-connect-jdbc

If the DB engine is not supported by built-in JDBC driver you need:

- Do not test the connection after creating a successful connection, because Glue's default MySQL JDBC driver does not support MySQL8.0**
- But we can use specify the MySQL8.0 JDBC in ETL Job**. [Bring your own JDBC drivers to your Glue Spark ETL jobs](https://aws.amazon.com/about-aws/whats-new/2019/11/aws-glue-now-enables-you-to-bring-your-own-jdbc-drivers-to-your-glue-spark-etl-jobs/)

2. For built-in JDBC driver, set the correct [Glue Connection SSL Properties](https://docs.aws.amazon.com/glue/latest/dg/connection-defining.html#connection-properties-SSL)

3. For custom JDBC driver, you can use the code:
```python
glueContext = GlueContext(SparkContext.getOrCreate())

source_df = spark.read.format("jdbc").option("url","jdbc:postgresql://<hostname>:<port>/<datbase>").option("dbtable", "<table>").option("driver", "org.postgresql.Driver").option("sslfactory", "org.postgresql.ssl.NonValidatingFactory").option("ssl", "true").option("user", "<username>").option("password", "<password>").load()

dynamic_dframe = DynamicFrame.fromDF(source_df, glueContext, "dynamic_df")
```

4. More trouble shooting, please check [Why does my AWS Glue test connection fail?](https://aws.amazon.com/premiumsupport/knowledge-center/glue-test-connection-failed/)