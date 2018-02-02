package billg;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

/**
 * Test class
 */
public class MainTest {

  @Test
  public void test() {
    Main main = new Main();
    main.hello();
  }

  @Test
  public void test_transform_input() throws IOException {
    String[] inputData = readData("test/resources/input_data.txt");
    String outputFile = "out/output_data.txt";

    writeData(outputFile, "1 2 9 5 3");

    assertExpectedOutput("test/resources/expected_output_data.txt", outputFile);
  }

  private void assertExpectedOutput(String expectedOutputFile,
                                    String outputFile) throws IOException {
    String[] expectedOutputData = readData(expectedOutputFile);
    String[] outputData = readData(outputFile);
    assertEquals(expectedOutputData[0], outputData[0]);
  }

  private static void writeData(String file, String value) throws IOException {
    BufferedWriter writer = new BufferedWriter(new FileWriter(file));
    writer.write(value);
    writer.close();
  }

  private static String[] readData(String file) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(file));
    String line;
    List<String> lines = new ArrayList<>();
    while ((line = reader.readLine()) != null) {
      lines.add(line);
    }
    reader.close();
    return lines.toArray(new String[lines.size()]);
  }

  private static void debug(Object object) {
    System.out.println(object);
  }
}
