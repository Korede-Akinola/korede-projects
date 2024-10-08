import java.util.LinkedList;
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
    public void buildMaze(){
        System.out.println("Building Maze");
        int placesReached = 0;
        int x = 0, y = 0;
        System.out.println("koQ");
        LinkedList<String> directions = new LinkedList<String>();
        System.out.println("koQ");


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
        System.out.println(directions);


}
public static void main(String[] args){
        MazeBuilder maze = new MazeBuilder(10,10);
        maze.buildMaze();
}
}
