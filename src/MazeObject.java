public class MazeObject {
    private boolean isStart;
    private int[] objectCords = new int[2];
    private boolean top_empty;
    private boolean bottom_empty;
    private boolean left_empty;
    private boolean right_empty;
    private boolean explored;
    private boolean isEnd;
    public MazeObject(int x, int y) {
        objectCords[0] = x;
        objectCords[1] = y;
        top_empty = false;
        bottom_empty = false;
        left_empty = false;
        right_empty = false;
        explored = true;
    }
    public void explore_top(){
        top_empty = true;
        explored = false;
    }
    public void explore_bottom(){
        bottom_empty = true;
        explored = false;
    }
    public void explore_left(){
        left_empty = true;
        explored = false;
    }
    public void explore_right(){
        right_empty = true;
        explored = false;
    }
    public boolean isUnexplored(){
        return explored;
    }
    public boolean topExplored(){
        return top_empty;
    }
    public boolean leftExplored(){
        return left_empty;
    }
    public boolean rightExplored(){
        return right_empty;
    }
    public boolean bottomExplored(){
        return bottom_empty;
    }
    public String toString(){
        String result  = "Cords: ";
        result += objectCords[0] + " " + objectCords[1] + "\n";
        result += "Top: " + top_empty + "\n";
        result += "Bottom: " + bottom_empty + "\n";
        result += "Left: " + left_empty + "\n";
        result += "Right: " + right_empty + "\n";

        return result;
    }
    public boolean getIstart(){
        return isStart;
    }
    public void makeStart(){
        isStart = true;
    }
    public void makeEnd(){
        isEnd = true;
    }
    public boolean isEnd(){
        return isEnd;
    }
}
