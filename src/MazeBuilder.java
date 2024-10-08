import java.util.LinkedList;
import java.util.Random;
public class MazeBuilder {
    private MazeObject[][] maze;
    public MazeBuilder(int width, int height) {
        maze = new MazeObject[width][height];
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                maze[x][y] = new MazeObject(x,y);
            }
        }
    }
    private LinkedList<String> exploreDirection(int x,int y){
        LinkedList<String> directions = new LinkedList<String>();



        if (x+1<maze.length){
            if (maze[x+1][y].isUnexplored()){
                directions.add("S");

            }
        }
        if (y+1<maze[0].length){
            if (maze[x][y+1].isUnexplored()){
                directions.add("E");
            }
        }
        if (x - 1>= 0 ){
            if (maze[x-1][y].isUnexplored()){
                directions.add("N");
            }
        }
        System.out.println(y-1>0);
        try {
            System.out.println(maze[x][y-1].isUnexplored());
        }catch (Exception e){
            System.out.println(" ");
        }

        if (y - 1>= 0 ){
            if (maze[x][y-1].isUnexplored()){
                directions.add("W");
            }
        }

        return directions;
    }
    public void buildMaze(){
        Random rand = new Random();
        System.out.println("Building Maze");
        int placesReached = 1;
        int x = 0, y = 0;


        LinkedList<String> directions = exploreDirection(x,y);

        do{
        String next_direction = directions.get(rand.nextInt(directions.size()));


        switch (next_direction){
            case "N":
                maze[x][y].explore_top();
                x--;
                maze[x][y].explore_bottom();
                break;
            case "S":
                maze[x][y].explore_bottom();
                x++;
                maze[x][y].explore_top();
                break;
            case "E":
                maze[x][y].explore_right();
                y++;
                maze[x][y].explore_left();
                break;
            case "W":
                maze[x][y].explore_left();
                y--;
                maze[x][y].explore_right();
        }

        placesReached++;
        directions.clear();
        directions = exploreDirection(x,y);
        System.out.println(directions);


        }while(!directions.isEmpty());


}
    public MazeObject getObjectAt(int xPos,int yPos){
        return maze[xPos][yPos];
    }

public static void main(String[] args){
        MazeBuilder maze = new MazeBuilder(3,3);
        maze.buildMaze();
        System.out.println("\n"+maze.toString());
}
}
