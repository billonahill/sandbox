package billg;

public class Main {

  public void hello() {
    debug("Hello world");
  }

  public static void main(String[] args) {
    Main main = new Main();
    main.hello();
  }

  private static void debug(Object object) {
    System.out.println(object);
  }
}
