from pyspark import SparkContext

sc = SparkContext(appName="WordCount")
rdd = sc.textFile("file:///opt/bitnami/spark/purchases.txt")
word_counts = rdd.flatMap(lambda line: line.split()) \
                 .map(lambda word: (word, 1)) \
                 .reduceByKey(lambda a, b: a + b)

for word, count in word_counts.collect():
    print(f"{word}: {count}")

sc.stop()
