package ca.jrvs.apps.grep;

import java.io.File;
import java.io.IOException;
import java.util.stream.Stream;

public interface JavaGrepStream {

  void process() throws IOException;
  Stream<File> listFiles(String rootDir) throws IOException;
  Stream<String> readLines(File inputFile);
  boolean containsPattern(String line);
  void writeToFile(Stream<String> lines) throws IOException;

  String getRootPath();
  String getRegex();
  String getOutFile();

  void setRootPath(String rootPath);
  void setRegex(String regex);
  void setOutFile(String outFile);
}
