import javax.swing.JPanel;
import java.awt.*;

public class GamePanel extends JPanel implements Runnable {

    final int screenHeightTiles = 10;
    final int screenWidthTiles = 10;
    final int widthBuffer = 1;
    final int heightBuffer = 1;
    final int screenWidth = 600;
    final int screenHeight = 600;
    final int tileWidth = screenWidth/screenWidthTiles;
    final int tileHeight = screenHeight/screenHeightTiles;
    MazeBuilder mazeBuilder = new MazeBuilder(screenWidthTiles-(widthBuffer*2), screenHeightTiles-(heightBuffer*2));
    Thread thread;

    Keyhandler keyH = new Keyhandler();
    public GamePanel() {
        mazeBuilder.buildMaze();

        this.setPreferredSize(new Dimension(screenWidth, screenHeight));
        this.setBackground(Color.BLACK);
        this.setDoubleBuffered(true);
        this.addKeyListener(keyH);
        this.setFocusable(true);
    }
    public void startGameThread() {
        thread = new Thread(this);
        thread.start();

    }
    public void run(){
            while(thread != null) {
                update();
                repaint();
            }

    }
    public void winCondition(){
        if(mazeBuilder.startX == mazeBuilder.endX && mazeBuilder.startY == mazeBuilder.endY) {
            mazeBuilder = new MazeBuilder(screenWidthTiles-(widthBuffer*2), screenHeightTiles-(heightBuffer*2));
            mazeBuilder.buildMaze();

        }
    }
    public void update() {


        MazeObject squareAt = mazeBuilder.getObjectAt(mazeBuilder.startX,mazeBuilder.startY);
        if(keyH.upPressed && squareAt.topExplored()){
            keyH.upPressed = false;
            squareAt.makeStart();
            mazeBuilder.startX--;
            mazeBuilder.getObjectAt(mazeBuilder.startX,mazeBuilder.startY).makeStart();
            winCondition();
            return;
        }
        if(keyH.downPressed && squareAt.bottomExplored()){
            keyH.downPressed = false;
            squareAt.makeStart();
            mazeBuilder.startX++;
            mazeBuilder.getObjectAt(mazeBuilder.startX,mazeBuilder.startY).makeStart();
            winCondition();
            return;

        }
        if(keyH.leftPressed && squareAt.leftExplored()){
            keyH.leftPressed = false;
            squareAt.makeStart();
            mazeBuilder.startY--;
            mazeBuilder.getObjectAt(mazeBuilder.startX,mazeBuilder.startY).makeStart();
            winCondition();
            return;

        }
        if(keyH.rightPressed && squareAt.rightExplored()){
            keyH.rightPressed = false;
            squareAt.makeStart();
            mazeBuilder.startY++;
            mazeBuilder.getObjectAt(mazeBuilder.startX,mazeBuilder.startY).makeStart();
            winCondition();

        }

    }
    public void paintComponent(Graphics g) {

        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        Graphics2D g3 = (Graphics2D) g.create();
        Graphics2D g4 = (Graphics2D) g.create();
        Graphics2D g5 = (Graphics2D) g.create();
        g2.setColor(Color.WHITE);
        g3.setColor(Color.black);
        g4.setColor(Color.green);
        g5.setColor(Color.red);




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

        for(int yCord = 0; yCord < screenHeightTiles-(heightBuffer*2);yCord++){
            for(int xCord = 0; xCord < screenWidthTiles-(widthBuffer*2);xCord++){
                MazeObject mazeAt = mazeBuilder.getObjectAt(yCord,xCord);
                if (mazeAt.getIstart()){

                    g4.fillRect(tileWidth*(xCord+widthBuffer)+tileWidth/4,tileHeight*(yCord+heightBuffer)+tileHeight/4,tileWidth-tileWidth/2,tileHeight-tileHeight/2);
                };
                if (mazeAt.isEnd()){
                    g5.fillRect(tileWidth*(xCord+widthBuffer)+tileWidth/4,tileHeight*(yCord+heightBuffer)+tileHeight/4,tileWidth-tileWidth/2,tileHeight-tileHeight/2);

                }
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
        g4.dispose();
        g5.dispose();
    }
}

