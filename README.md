# literacy-analyser

A python based Map-Reduce program to analyse the literacy rate among districts of a state

## Problem Statement
Given the MHA population dataset, find the impact of education policies implemented by the Government between 2001 to 2011

Data Source - https://www.kaggle.com/datasets/prasad22/mha-population-dataset

## Methodology
To find the impact of educational policies and to understand the ground-truth about the policy implementations on the population of the state, we are going to compare the literacy rate between 2001 and 2011.

Using Map-Reduce technique on the dataset, we will derive the literacy rate for each district for the Census Years in consideration.

## Implementation
Given dataset (in CSV format) on MHA population, contains multiple fields (refer: [resources/MHA_Population_Report.csv](https://github.com/thegoodparticle/literacy-analyser/blob/main/resources/MHA_Population_Report.csv)), out of which we are intereseted in the following fields.

| Census Year | District | Total literates | Total population |
| ----------- | -------- | --------------- | ---------------- |


### Map-Reduce Diagrams

![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/599e3b08-595a-47e0-a925-407119707504)


### Map Function Pseudocode

```
read the dataset CSV file as std-input

for all the lines in the input:
  if Census Year in (2001, 2011):
    output to std-output <(District, Census Year), (Total_Literates, Total_Population)>

```

### Reduce Function Pseudocode

```
read the shuffle-sorted map output as std-input

key = "", total_population = 0, total_literates = 0

// input format: Key - (District, Census Year), Value - (Total_Literates, Total_Population)

for all the key, value pairs from the input:
  literates, population = value.split(',')
  if key is current_key:
    total_population += population
    total_literates += literates

  if key != ""
    compute literacy rate as total_literates/total_population*100
    output to std-output <(District, Census Year), (literacy rate in %)>

  // initialize global values
  key = current_key
  total_population = population
  total_literates = literates

```

## How to Run?

1. Run a terminal from the project root
2. Let us try running the Map Reduce programs locally with test data, before executing it on Hadoop
```
cat resources/test_data.csv | python3 src/mapper.py | sort -k1,1 | python3 src/reducer.py
```
The output should look like 
![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/5533d993-53d6-4ce5-ad77-4d4f7688cffc)

3. Create a resource directory in HDFS and copy the dataset to that folder
```
hadoop fs -mkdir resources
hadoop fs -put resources/MHA_Population_Report.csv resources/
```
4. Copy map and reduce files to hdfs (*)
```
hadoop fs -put src/mapper.py mapper.py
hadoop fs -put src/reducer.py reducer.py
```
5. Provide executable permission to the Map-Reduce scripts
```
chmod 777 src/mapper.py src/reducer.py
```
6. Provide executable permission to the scripts in HDFS (*)
```
hadoop fs -chmod 777 mapper.py reducer.py
```
7. Run the hadoop map reduce command
```
hadoop jar <path-to-hadoop-streaming-3.2.4.jar> -file src/mapper.py -file src/reducer.py -input resources -output literacy_rate -mapper mapper.py -reducer reducer.py 
```
<br>
On executing this command, Map Reduce job starts running

![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/f2b1ff64-4e56-4fb2-b7c4-597ecd7f8ce3)

## Output

Output of the Map Reduce job can be found under the path mentioned as _'-output'_ in the _'hadoop jar ...'_ command.

```
$ hadoop fs -ls literacy_rate

Found 2 items
-rw-r--r--   3 centos hadoop          0 2023-09-28 18:20 literacy_rate/_SUCCESS
-rw-r--r--   3 centos hadoop       1420 2023-09-28 18:20 literacy_rate/part-00000

$ hadoop fs -cat literacy_rate/part-00000
AHMADNAGAR,2001	64.31%
AHMADNAGAR,2011	69.38%
AKOLA,2001	69.64%
AKOLA,2011	77.80%
AMRAVATI,2001	71.21%
AMRAVATI,2011	77.96%
AURANGABAD,2001	61.15%
AURANGABAD,2011	67.65%
BEED,2001	57.44%
BEED,2011	66.48%
BHANDARA,2001	67.83%
BHANDARA,2011	74.97%
BULDANA,2001	64.23%
BULDANA,2011	72.69%
...

```

Complete output file can be found here - https://github.com/thegoodparticle/literacy-analyser/blob/main/output/part-00000

Screenshots: 
![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/af3c9a6e-c972-479f-b36a-df22c46c1fe1)
![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/8135de09-5d9c-4b94-89fa-598300fec562)
![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/9af2dd6c-86f4-4e3b-ba92-665fa559f6f3)
![image](https://github.com/thegoodparticle/literacy-analyser/assets/140166948/7b344e8f-fb1b-4ad7-a0a6-54df66736b65)


## Statistics

On running the _'hadoop jar ...'_ command, jobs start executing and as the execution progresses, we will start seeing the statistics one-by-one. As soon as the job ends, it prints out the total statistics of the run.

```
2023-09-28 18:20:29,511 INFO mapreduce.Job: Counters: 54
	File System Counters
		FILE: Number of bytes read=1971893
		FILE: Number of bytes written=4671852
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=16475592
		HDFS: Number of bytes written=1420
		HDFS: Number of read operations=11
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters 
		Launched map tasks=2
		Launched reduce tasks=1
		Data-local map tasks=2
		Total time spent by all maps in occupied slots (ms)=28160
		Total time spent by all reduces in occupied slots (ms)=14046
		Total time spent by all map tasks (ms)=14080
		Total time spent by all reduce tasks (ms)=4682
		Total vcore-milliseconds taken by all map tasks=14080
		Total vcore-milliseconds taken by all reduce tasks=4682
		Total megabyte-milliseconds taken by all map tasks=28835840
		Total megabyte-milliseconds taken by all reduce tasks=14383104
	Map-Reduce Framework
		Map input records=132316
		Map output records=82967
		Map output bytes=1805953
		Map output materialized bytes=1971899
		Input split bytes=236
		Combine input records=0
		Combine output records=0
		Reduce input groups=70
		Reduce shuffle bytes=1971899
		Reduce input records=82967
		Reduce output records=70
		Spilled Records=165934
		Shuffled Maps =2
		Failed Shuffles=0
		Merged Map outputs=2
		GC time elapsed (ms)=351
		CPU time spent (ms)=4860
		Physical memory (bytes) snapshot=1618956288
		Virtual memory (bytes) snapshot=10730037248
		Total committed heap usage (bytes)=1468006400
		Peak Map Physical memory (bytes)=716197888
		Peak Map Virtual memory (bytes)=3008458752
		Peak Reduce Physical memory (bytes)=187342848
		Peak Reduce Virtual memory (bytes)=4713586688
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters 
		Bytes Read=16475356
	File Output Format Counters 
		Bytes Written=1420
2023-09-28 18:20:29,512 INFO streaming.StreamJob: Output directory: literacy_rate
```

## Conclusion
