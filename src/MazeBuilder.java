import java.util.LinkedList;
import java.util.Random;
public class MazeBuilder {
    private MazeObject[][] maze;
    public MazeBuilder(int width, int height) {
        maze = new MazeObject[height][width];
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                maze[y][x] = new MazeObject(y,x);
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


        if (y - 1>= 0 ){
            if (maze[x][y-1].isUnexplored()){
                directions.add("W");
            }
        }

        return directions;
    }
    private LinkedList<int[]> explorePath(int x,int y,LinkedList<int[]> place){
        Random rand = new Random();
        place.addLast(new int[]{x,y});
        LinkedList<String> directions = exploreDirection(x,y);
        System.out.println(directions);
        do{
            String next_direction = directions.get(rand.nextInt(directions.size()));

            System.out.println(next_direction + " " + x + " " + y);
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

            directions.clear();
            directions = exploreDirection(x,y);
            place.addLast(new int[]{x,y});
            System.out.println(directions);


        }while(!directions.isEmpty());
        return place;
    }
    public void buildMaze(){

        System.out.println("Building Maze");
        int x = 3, y = 3;
        LinkedList<int[]> placesTravelled = new LinkedList<int[]>();
        placesTravelled = explorePath(0,0,placesTravelled);
        int i = 0;
        while (i <placesTravelled.size()){
            int[] curentPos = placesTravelled.remove(i);
            if (!exploreDirection(curentPos[0],curentPos[1]).isEmpty()){

                i = 0;
                explorePath(curentPos[0],curentPos[1],placesTravelled);
            }

        }

        /*LinkedList<String> directions = exploreDirection(x,y);
        System.out.println(directions);
        do{
        String next_direction = directions.get(rand.nextInt(directions.size()));

        System.out.println(next_direction + " " + x + " " + y);
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

        directions.clear();
        directions = exploreDirection(x,y);
        System.out.println(directions);


        }while(!directions.isEmpty());*/


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
