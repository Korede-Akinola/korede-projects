import javax.swing.JPanel;
import java.awt.*;

public class GamePanel extends JPanel implements Runnable {
    final int tileWidth = 48;
    final int tileHeight = 48;
    final int screenHeightTiles = 12;
    final int screenWidthTiles = 16;
    final int screenWidth = tileWidth * screenWidthTiles;
    final int screenHeight = tileHeight * screenHeightTiles;
    Thread thread;
    public GamePanel() {
        System.out.println(screenHeight);
        System.out.println(screenWidth);
        this.setPreferredSize(new Dimension(screenWidth, screenHeight));
        this.setBackground(Color.BLACK);
        this.setDoubleBuffered(true);
    }
    public void startGameThread() {
        thread = new Thread(this);
        thread.start();

    }
    public void run(){
            while (thread != null) {
                update();
                repaint();
            }
    }
    public void update() {

    }
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        Graphics2D g3 = (Graphics2D) g.create();
        g2.setColor(Color.WHITE);
        g3.setColor(Color.GREEN);
        int widthBuffer = 2;
        int heightBuffer = 1;
        g2.drawRect(tileWidth * widthBuffer, tileHeight * heightBuffer , tileWidth*(screenWidthTiles -(widthBuffer*2)),tileHeight*(screenHeightTiles-(heightBuffer*2)));
        int x = 3;
        while (x < 15){
            int y = 1;
            while (y < 11){
                if (x == 14 && y == 1){
                    y++;
                    continue;
                }
                if (x == 14){
                     g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * (x - 1), tileHeight * y);


                } else if (y == 1) {
                    g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * x, tileHeight * (y + 1));

                } else {
                    g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * x, tileHeight * (y + 1));
                    g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * (x - 1), tileHeight * y);
                }
                y++;
            }
            x++;
        }

        g2.dispose();
    }
}

