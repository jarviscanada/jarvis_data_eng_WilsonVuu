# JavaGrep App

## Introduction
The **JavaGrep App** is a **Java-based application** that mimics the behavior of the Linux `grep` command. 
It searches through every file inside a given root folder and its subdirectories, matches each line against a 
user-given **regular expression**, and writes all **matching lines** to an output file. 
The app is built on **Java 8** and uses the **Java 8 Streams API** for lazy, memory-efficient file processing, 
and **Java NIO** (`java.nio.file`) for efficient file and directory traversal. 
Libraries and tools used include **SLF4J** and **Log4j** for logging and debugging
, **Maven** with the `maven-shade` plugin to create a fat JAR, 
and **Docker** for containerized distribution. 

## Quick Start

**Build the fat JAR:**
```bash
cd core_java/grep
mvn clean package
```

**Run with the JAR directly:**
```bash
java -jar target/grep-1.0-SNAPSHOT.jar <regex> <rootPath> <outFile>

# Example: find all lines containing "Romeo" and write matches to result.txt
java -jar target/grep-1.0-SNAPSHOT.jar ".*Romeo.*" ./data/txt ./out/result.txt
```

**Run with Docker:**
```bash
# Build the image
docker build -t wilsonvuu/grep .

# Run the container
docker run --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/out:/out \
  wilsonvuu/grep ".*Romeo.*" /data/txt /out/result.txt
```

> Note: create an `out/` directory before running the application!

## Implementation

### Pseudocode

```
process():
  matchedLines = listFiles(rootPath)          // recursively find all files under rootPath
    .flatMap(file -> readLines(file))    // read each file and flatten into one stream of lines
    .filter(line -> containsPattern(line))  // keep only lines matching the regex

  writeToFile(matchedLines)                   // write all matched lines to the output file
```

### Performance Issue
The naive approach of loading all file lines into an **`ArrayList`** in memory can exhaust the **JVM heap** 
when processing large directory trees. 
This is solved by using the **Java 8 Streams API** with `Files.lines()`, which reads lines **lazily**,
only one line is held in memory at a time rather than loading entire files upfront.

## Test

To test the application manually, the included `data/txt/shakespeare.txt` file was used as sample input data. 
The packaged JAR was executed with several regex patterns, including:

- `".*Romeo.*"` to find all lines containing “Romeo”
- `"^[A-Z].*"` to find lines beginning with a capital letter

The generated output file was reviewed to confirm that all matched lines were correct. 
Results were also cross-checked against the Linux `grep` command by running `grep -r "Romeo" data/txt/` 
and comparing the number of matches returned.

During development, SLF4J/Log4j logging was used to trace file traversal, regex matching, and output generation, 
which helped verify the application's execution flow and simplify debugging. 
IntelliJ IDEA’s debugger was also used to step through the application, 
inspect variables, and validate recursive file processing behavior.

## Deployment

**Docker**: The app is dockerized using `adoptopenjdk/openjdk8:alpine` as the base image, keeping the container lightweight. 
The fat JAR produced by Maven is copied into the image and set as the entrypoint, 
allowing users to run the app without needing a local Java or Maven installation.

```bash
# Build the image
docker build -t wilsonvuu/grep .

# Push to Docker Hub
docker push wilsonvuu/grep
```

## Improvements

**Parallel file processing:** Use a parallel stream and making it multi-threaded to scan files concurrently, 
significantly reducing runtime on large directory trees with many files.
