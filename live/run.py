from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import sys
import requests
# from operator import add

# 没用到
def update_total_count(current_count, previous_count):
    if previous_count is None:
        previous_count = 0
    return sum(current_count) + previous_count


# Create a local StreamingContext with two working thread and batch interval of 1 second
# sc = SparkContext("local[2]", "NetworkWordCount")
sc = SparkContext("spark://nutaochacbook13:7077", "NetworkWordCount")
ssc = StreamingContext(sc, 3)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
# Socket数据格式为 \ndata1\ndata2\n
words = lines.flatMap(lambda line: line.split("/n"))

word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
collections = {}
# # 计算总计数
# total_count = word_counts.map(lambda x: x[1]).reduce(add)
# total_count = word_counts.map(lambda x: x[1]).reduce(add)

# 打印结果
def print_results(rdd):
    for pair in rdd.collect():
        if pair[0] in collections:
            collections[pair[0]] += pair[1]
        else:
            collections[pair[0]] = pair[1]
    send_data_to_dashboard()


def send_data_to_dashboard():
    top_10 = sorted(collections.items(), key=lambda x: x[1], reverse=True)[:10]
    words = []
    counts = []
    for word, count in top_10:
        words.append(word)
        counts.append(count)
        print("{}: {}".format(word, count))

    print(words)
    print(counts)
    # initialize and send the data through REST API
    try:
        url = 'http://localhost:5001/updateData'
        request_data = {'label': str(words), 'data': str(counts)}
        response = requests.post(url, data=request_data)
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


# 打印每个单词的计数
word_counts.foreachRDD(print_results)

# 打印结果
ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
