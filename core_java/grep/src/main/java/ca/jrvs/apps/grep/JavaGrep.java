package ca.jrvs.apps.grep;

import java.io.*;
import java.util.List;



public interface JavaGrep {


  void process() throws  IOException;
  List <File> listFiles(String rootDir) throws  IOException;
  List<String> readLines (File inputFile);
  boolean containsPattern(String line);
  void writeToFile(List<String> lines) throws IOException;


  String getRootPath();
  String getRegex();
  String getOutFile();

  void setRootPath(String rootPath);
  void setRegex(String regex);
  void setOutFile(String outFile);

}
