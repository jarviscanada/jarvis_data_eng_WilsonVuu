package ca.jrvs.apps.grep;

import java.io.*;
import java.util.List;
import java.util.stream.Stream;



public interface JavaGrep {

  void process();
  List<File> listFiles(String rootDir);
  List<String> readLines(File inputFile);
  boolean containsPattern(String line);
  void writeToFile(Stream<String> lines) throws IOException;


  String getRootPath();
  String getRegex();
  String getOutFile();

  void setRootPath(String rootPath);
  void setRegex(String regex);
  void setOutFile(String outFile);

}
