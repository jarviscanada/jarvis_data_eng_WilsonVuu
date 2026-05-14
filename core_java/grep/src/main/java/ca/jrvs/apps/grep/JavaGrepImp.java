package ca.jrvs.apps.grep;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.log4j.BasicConfigurator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepImp implements JavaGrep {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepImp.class);
  private String regex;
  private String rootPath;
  private String outFile;
  private Pattern pattern;
  @Override
  public void process() {
    List<String> foundLines = new ArrayList<>();

    for (File file : listFiles(this.getRootPath())) {
      for (String line : readLines(file)) {
        if (containsPattern(line)) {
          foundLines.add(line);
        }
      }
    }
    writeToFile(foundLines);
  }

  @Override
  public List<File> listFiles(String rootDir) {
    if (rootDir == null || rootDir.trim().isEmpty()) {
      throw new IllegalArgumentException("rootDir cannot be null or empty");
    }

    Path path = Paths.get(rootDir);
    if (!Files.exists(path)) {
      throw new IllegalArgumentException("Path does not exist: " + rootDir);
    }
    if (!Files.isDirectory(path)) {
      throw new IllegalArgumentException("Path is not a directory: " + rootDir);
    }

    try (Stream<Path> paths = Files.walk(path)) {
      return paths
          .filter(Files::isRegularFile)
          .map(Path::toFile)
          .collect(Collectors.toList());
    } catch (IOException e) {
      logger.error("Failed to list files in: {}", rootDir, e);
      return new ArrayList<>();
    }
  }

  @Override
  public List<String> readLines(File inputFile) {
    if (inputFile == null) {
      throw new IllegalArgumentException("inputFile cannot be null");
    }
    if (!inputFile.exists() || !inputFile.isFile()) {
      throw new IllegalArgumentException ("inputFile does not exist or is not a file: " + inputFile);
    }

    try {
      return Files.readAllLines(inputFile.toPath());
    } catch (IOException e) {
      logger.error("Failed to read file: {}", inputFile.getPath(), e);
      return new ArrayList<>();
    }
  }

  @Override
  public boolean containsPattern(String line) {
    if (line == null) return false;
    return pattern.matcher(line).find();
  }

  @Override
  public void writeToFile(List<String> lines) {
    if (lines == null || lines.isEmpty()) {
      logger.warn("No lines to write, skipping writeToFile step");
      return;
    }

    Path outPath = Paths.get(getOutFile());

    try (BufferedWriter writer = Files.newBufferedWriter(outPath)) {
      for (String line : lines) {
        writer.write(line);
        writer.newLine();
      }
      logger.info("File written successfully: {}", outPath);
    } catch (IOException e) {
      logger.error("Failed to write to file: {}", outPath, e);
      throw new RuntimeException(e);
    }
  }

  //Getters
  @Override public String getRegex()    {
    return regex;
  }
  @Override public String getRootPath() {
    return rootPath;
  }
  @Override public String getOutFile()  {
    return outFile;
  }

  //Setters
  @Override
  public void setRegex(String regex) {
    if (regex == null || regex.trim().isEmpty()) {
      throw new IllegalArgumentException("regex cannot be null or empty");
    }
    this.regex = regex;
    //so that it doesn't keep compiling the pattern
    this.pattern = Pattern.compile(this.getRegex());
  }

  @Override
  public void setRootPath(String rootPath) {
    if (rootPath == null || rootPath.trim().isEmpty()) {
      throw new IllegalArgumentException("rootPath cannot be null or empty");
    }
    this.rootPath = rootPath;
  }

  @Override
  public void setOutFile(String outFile) {
    if (outFile == null || outFile.trim().isEmpty()) {
      throw new IllegalArgumentException("outFile cannot be null or empty");
    }

    Path parent = Paths.get(outFile).getParent();
    if (parent != null && !Files.exists(parent)) {
      throw new IllegalArgumentException("Parent directory does not exist: " + parent);
    }

    this.outFile = outFile;
  }

  public static void main(String[] args) {
    BasicConfigurator.configure();
    if (args.length != 3) {
      throw new IllegalArgumentException("USAGE: JavaGrep regex rootPath outFile");
    }

    JavaGrepImp javaGrep = new JavaGrepImp();
    javaGrep.setRegex(args[0]);
    javaGrep.setRootPath(args[1]);
    javaGrep.setOutFile(args[2]);

    try {
      javaGrep.process();
    } catch (Exception e) {
      logger.error("JavaGrep failed. regex={}, rootPath={}, outFile={}",
          args[0], args[1], args[2], e);
    }
  }
}
