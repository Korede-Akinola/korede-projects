import javax.swing.JPanel;
import java.awt.*;

public class GamePanel extends JPanel implements Runnable {
    final int tileWidth = 48;
    final int tileHeight = 48;
    final int screenHeightTiles = 5;
    final int screenWidthTiles = 5;
    final int widthBuffer = 1;
    final int heightBuffer = 1;
    final int screenWidth = tileWidth * screenWidthTiles;
    final int screenHeight = tileHeight * screenHeightTiles;
    final MazeBuilder mazeBuilder = new MazeBuilder(screenWidthTiles-(widthBuffer*2), screenHeightTiles-(heightBuffer*2));
    Thread thread;
    public GamePanel() {
        mazeBuilder.buildMaze();
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
                MazeBuilder maze = new MazeBuilder(screenWidthTiles-widthBuffer, screenHeight-heightBuffer);
            }
    }
    public void update() {

    }
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        Graphics2D g3 = (Graphics2D) g.create();
        Graphics2D g4 = (Graphics2D) g.create();
        g2.setColor(Color.WHITE);
        g3.setColor(Color.blue);


        g2.drawRect(tileWidth * widthBuffer, tileHeight * heightBuffer , tileWidth*(screenWidthTiles -(widthBuffer*2)),tileHeight*(screenHeightTiles-(heightBuffer*2)));
        int x = widthBuffer+1;

        while (x < screenWidthTiles-widthBuffer+1) {

            int y = heightBuffer;

            while (y < screenHeightTiles-heightBuffer) {
                if (x == screenWidthTiles-widthBuffer && y == heightBuffer) {
                    y++;
                    continue;
                }
                if (x == screenWidthTiles-widthBuffer){
                     g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * (x - 1), tileHeight * y);


                } else if (y == heightBuffer) {
                    g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * x, tileHeight * (y + 1));

                } else {
                    g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * x, tileHeight * (y + 1));
                    g2.drawLine(tileWidth * x, tileHeight * y, tileWidth * (x - 1), tileHeight * y);
                }
                y++;
            }


            x++;
        }


        boolean left = false;
        boolean right = false;
        boolean up = false;
        boolean down = false;
        for(int xCord = 0; xCord < screenWidthTiles-(widthBuffer*2);xCord++){
            for(int yCord = 0; yCord < screenHeightTiles-(heightBuffer*2);yCord++){
                MazeObject mazeAt = mazeBuilder.getObjectAt(xCord,yCord);
                if (mazeAt.leftExplored()){

                    g3.drawLine(tileWidth * (1+xCord), tileHeight * (1+yCord), tileWidth * (1+xCord), tileHeight * (1 + 1+yCord));
                }
                if (mazeAt.bottomExplored()){
                    g3.drawLine(tileWidth * (2+xCord), tileHeight * (2 + yCord), tileWidth * (2 - 1 + xCord), tileHeight * (2+yCord));


                }
                if (mazeAt.topExplored()){
                    g3.drawLine(tileWidth * (2+xCord), tileHeight * (1+yCord), tileWidth * (2 - 1+xCord), tileHeight * (1+yCord));

                }
                if (mazeAt.rightExplored()){
                    g3.drawLine(tileWidth * (2+xCord), tileHeight * (1+yCord), tileWidth * (2+xCord), tileHeight * (1 + 1+yCord));
                }

            }
        }




        g2.dispose();
        g3.dispose();
    }
}

