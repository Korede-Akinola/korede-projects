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



        System.out.println(maze.length);
        if (x+1<maze.length){
            if (maze[x+1][y].isUnexplored()){
                directions.add("E");

            }
        }
        if (y+1<maze[0].length){
            if (maze[x][y+1].isUnexplored()){
                directions.add("S");
            }
        }
        if (x - 1>= 0 ){
            if (maze[x-1][y].isUnexplored()){
                directions.add("W");
            }
        }
        if (y - 1>= 0 ){
            if (maze[x][y-1].isUnexplored()){
                directions.add("N");
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
        String next_direction = directions.get(rand.nextInt(directions.size()));
        System.out.println(next_direction);
        switch (next_direction){
            case "N":
                maze[x][y].explore_top();
                y--;
                maze[x][y - 1].explore_bottom();
                break;
            case "S":
                maze[x][y].explore_bottom();
                y++;
                maze[x][y].explore_top();
                break;
            case "E":
                maze[x][y].explore_right();
                x++;
                maze[x][y].explore_left();
                break;
            case "W":
                maze[x][y].explore_left();
                x--;
                maze[x][y].explore_right();
        }
        System.out.println();
        placesReached++;


}
public String toString(){
        String output = "";
        String yOutput = " ";
        for(int x = 0; x < maze.length; x++){
            for (int y = 0; y < maze[x].length; y++){
                output += " 0 ";

                if (maze[x][y].isUnexplored() || maze[x][y].leftExplored() || maze[x][y].topExplored()){
                    output += " X " ;
                    yOutput += "X     ";

                }else if(maze[x][y].rightExplored()){
                    output += " > ";



                }else if(maze[x][y].bottomExplored()){
                    yOutput += "|     ";
                }

            }
            output += "\n";
            output += yOutput;
            yOutput = " ";
            output += "\n";
        }

        return output;
}
public static void main(String[] args){
        MazeBuilder maze = new MazeBuilder(3,3);
        maze.buildMaze();
        System.out.println(maze.toString());
}
}
