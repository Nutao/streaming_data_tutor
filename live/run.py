from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from operator import add

def update_total_count(current_count, previous_count):
    if previous_count is None:
        previous_count = 0
    return sum(current_count) + previous_count
  
# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 3)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
words = lines.flatMap(lambda line: line.split("/n"))

word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
collections={}
# # 计算总计数
# total_count = word_counts.map(lambda x: x[1]).reduce(add)
# total_count = word_counts.map(lambda x: x[1]).reduce(add)

# 打印结果
def print_results(rdd):
    for pair in rdd.collect():
      if pair[0] in collections:
        collections[pair[0]]+=pair[1]
      else:
        collections[pair[0]]= pair[1]
    print_collections()
        
def print_collections():
    top_10 = sorted(collections.items(), key=lambda x: x[1], reverse=True)[:10]
    for word, count in top_10:
        print("{}: {}".format(word, count))
        
# 打印每个单词的计数
word_counts.foreachRDD(print_results)

# 打印结果

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate