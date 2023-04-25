# import pandas as pd
# import time
# import sys

# file_path="./new_york_training_tweets_15_06.csv"
# data= pd.read_csv(file_path, chunksize=10)
# for trunk in data:
#   print(trunk)
#   time.sleep(10)
#   print("sleep 10 second")
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 10)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
