import java.util.Random;
import java.util.Scanner;
public class Rps {
    public static void main(String[] args) {
        int wins,loses,draws,gamesPlayed;
        wins = loses = draws = gamesPlayed = 0;
        Random random = new Random();
        Scanner sc = new Scanner(System.in);
        boolean stillPlaying = true;
        int playerInput;
        int botInput;
        String[] options = {"Rock","Paper","Scissors"};
        while (stillPlaying) {
            botInput = random.nextInt(3) + 1;
            System.out.printf("Enter 1. Rock, 2. paper or 3. scissors > ");
            playerInput = sc.nextInt();
            System.out.printf("You chose %s \nThe bot chose %s\n",options[playerInput-1],options[botInput-1]);
            if (playerInput == botInput) {
                System.out.println("You drew!");
                draws++;
            } else if (playerInput > botInput || (playerInput == 1 && botInput == 3)) {
                System.out.println("You won!");
                wins++;
            } else {
                System.out.println("You lost!");
                loses++;
            }
            gamesPlayed++;
            System.out.printf("GP:%d W:%d D:%d L:%d  \n", gamesPlayed, wins,draws,loses);
            System.out.print("Do you want to play again? (Y/N) > ");
            String answer;
            answer = sc.next().toUpperCase();
            if (answer.equals("Y")) {
                stillPlaying = true;
            }else {
                stillPlaying = false;
            }


        }

    }
}
