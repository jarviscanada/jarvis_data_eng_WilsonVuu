package ca.jrvs.apps.grep;

import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.*;
import java.util.regex.Pattern;
import java.util.stream.Stream;
import org.apache.log4j.BasicConfigurator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class JavaGrepStreamImp implements JavaGrepStream {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepStreamImp.class);
  private String regex;
  private String rootPath;
  private String outFile;
  private Pattern pattern;

  /**
   *
   *
   */
  @Override
  public void process() throws IOException {
    try (Stream<File> files = listFiles(getRootPath())) {
        Stream <String> matchedLines = files
            .flatMap(this::readLines)
            .filter(this::containsPattern);

      writeToFile(matchedLines);
    } 

  }

  /**
   * Returns all regular files under rootDir as a List.
   *
   */
  @Override
  public Stream<File> listFiles(String rootDir) throws IOException {
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

    return Files.walk(path)
          .filter(Files::isRegularFile)
          .map(Path::toFile);
  }

  /**
   * Returns a lazy Stream of lines from the file.
   *
   */
  @Override
  public Stream<String> readLines(File inputFile) {
    if (inputFile == null) {
      throw new IllegalArgumentException("inputFile cannot be null");
    }
    if (!inputFile.exists() || !inputFile.isFile()) {
      throw new IllegalArgumentException(
          "inputFile does not exist or is not a file: " + inputFile);
    }

    try {
      return Files.lines(inputFile.toPath());
    } catch (IOException e) {
      logger.warn("Skipping unreadable file: {}", inputFile.getPath(), e);
      return Stream.empty();
    }
  }

  /**
   * Receives a single String line (not a Stream).
   *
   */
  @Override
  public boolean containsPattern(String line) {
    if (line == null) return false;
    return pattern.matcher(line).find();
  }

  /**
   * Consumes the matched-lines Stream for each line
   *
   */
  @Override
  public void writeToFile(Stream<String> lines) throws IOException {
    if (lines == null) {
      logger.warn("No lines to write, skipping file creation.");
      return;
    }

    Path outPath = Paths.get(this.outFile);
    try (BufferedWriter writer = Files.newBufferedWriter(outPath);
        Stream<String> stream = lines) {
      stream.forEach(line -> {
        try {
          writer.write(line);
          writer.newLine();
        } catch (IOException e) {
          throw new UncheckedIOException(e);
        }
      });
      logger.info("File written successfully: {}", outPath);
    } catch (IOException e) {
      logger.error("Failed to write to file: {}", outPath, e);
      throw new UncheckedIOException(e);
    }
  }

  //Getters
  @Override public String getRegex()    {
    return regex;
  }
  @Override public String getRootPath() {
    return rootPath;
  }
  @Override public String getOutFile()  {return outFile; }

  //Setters
  @Override
  public void setRegex(String regex) {
    if (regex == null || regex.trim().isEmpty()) {
      throw new IllegalArgumentException("regex cannot be null or empty");
    }
    this.regex = regex;
    // compile once here so containsPattern() doesn't recompile on every line
    this.pattern = Pattern.compile(this.regex);
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
      throw new IllegalArgumentException("USAGE: JavaGrepStream regex rootPath outDir");
    }

    JavaGrepStreamImp javaGrep = new JavaGrepStreamImp();
    javaGrep.setRegex(args[0]);
    javaGrep.setRootPath(args[1]);
    javaGrep.setOutFile(args[2]);

    try {
      javaGrep.process();
    } catch (Exception e) {
      logger.error("JavaGrepStream failed. regex={}, rootPath={}, outFile={}",
          args[0], args[1], args[2], e);
    }
  }
}