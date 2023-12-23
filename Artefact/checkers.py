#all the imports needed
import pygame
import os
import math
import statistics as st
import random
import time
import pandas as pd
import copy
import  PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#to make sure they played
did_they_play = True

#writing the layout for the starting window
layout = [[sg.Text("analysis mode"),sg.Radio("yes","analysis"),sg.Radio("no","analysis")]
    ,[sg.Text("Player 1 *",key = "player1"),sg.Radio("human","player1"),sg.Radio("bot","player1"),
          sg.Text("enter player one",text_color="red",visible = False,key = "player1 warning")],
          [sg.Text("Player 2 *",key = "player2"),sg.Radio("human","player2"),sg.Radio("bot","player2"),
          sg.Text("enter player two",visible = False,text_color = "red",key = "player2 warning")],
          [sg.Text("bots pause between moves (sec)"),sg.Input(key = "pause",size=(5,1))],
          [sg.Text("rounds"),sg.Slider(range=(1,500),default_value = 1,size=(20,15), orientation = "horizontal")],
          [sg.Text("custom board ",key = "custom"),sg.Radio("yes","custom"),sg.Radio("no","custom",default=True)],
          [sg.Text("first turn",key = "first"),sg.Radio("red","first",default=True),sg.Radio("white","first")],
          [[sg.Text("file name for analysis and storing (without .csv)")],[sg.Input(key='csv_name',size=(20,15))]],
          [sg.Text("file doesn't exist",text_color = "red",visible = False,key = "file")],
          [sg.Button("Start playing")],
          [sg.Text("* indicates required field")]]

# Create the window
window = sg.Window("checkers settings", layout, margins=(20,50))
# Create an event loop to make sure all correct data is inputted with a while loop
while True:
    #gathers all data from the window
    event, values = window.read()
    print(values)
    player1 = [values[2],values[3]]
    player2 = [values[4],values[5]]
    #makes sure pause time is in correct format
    try:
        float(values["pause"])
    except:
        values["pause"] = 0
    #the requirments to start the game
    if event == "Start playing" and (values[0] == True and (os.path.isfile(values['csv_name']+".csv") == True or values["csv_name"] == "")) or (any(x == True for x in player1) and any(x == True for x in player2) and (values[7] == True or values[8] == True) and (values[9] == True or values[10] == True)):
        #puts data in correct format
        if player1[0] == True:
            player1 = "human"
        else:
            player1 = "bot"
        if player2[0] == True:
            player2 = "human"
        else:
            player2 = "bot"
        if values[9] == True:
            first_turn = "red"
        elif values[10] == True:
            first_turn = "white"
        if values["csv_name"] == "":
            values["csv_name"] = "data"
        if values[0] == True:
            did_they_play = False
        break
        
    #warning to player if data is not entered
    elif event == "Start playing":
        if all(x == False for x in player1):
            window["player1"].update(text_color = "red")
            window["player1 warning"].update(visible = True)
            window[2].update(text_color= "red")
            window[3].update(text_color= "red")
        else:
            window["player1"].update(text_color = "white")
            window["player1 warning"].update(visible = False)
            window[2].update(text_color= "white")
            window[3].update(text_color = "white")
        if all(x == False for x in player2):
            window["player2"].update(text_color = "red")
            window["player2 warning"].update(visible = True)
            window[4].update(text_color = "red")
            window[5].update(text_color = "red")
        else:
            window["player2"].update(text_color = "white")
            window["player2 warning"].update(visible = False)
            window[4].update(text_color = "white")
            window[5].update(text_color = "white")
        if values[0] == True and os.path.isfile(values['csv_name']+".csv") == False:
            window["file"].update(visible = True)
        else:
            window["file"].update(visible = False)
    #closing the window ends the game
    if  event == sg.WIN_CLOSED:
        did_they_play = False
        values[6] = 0
        break
#close the starting window
window.close()
#inistalise pygame
pygame.init()
# all the images that need to be imported for pygame
pygame.display.set_caption("checkers")
board = pygame.image.load('checkerboard.png')
red = pygame.image.load('red checkers.png')
white = pygame.image.load('white checkers.png')
back = pygame.image.load('check.png')
go = pygame.image.load("where you go.png")
crown = pygame.image.load("crown.png")
cross = pygame.image.load("x.png")
white_wins = pygame.image.load("white wins.png")
red_wins = pygame.image.load("red wins.png")
finshed = pygame.image.load("done.png")
#resizing an image
finshed = pygame.transform.scale(finshed, (64, 64))
last_pos = pygame.image.load("where you move.png")
draw = pygame.image.load("draw.png")
#resizing an image
clear = pygame.transform.scale(cross, (64, 64))
#corodinate system for everything, individual square hold the data about what is on them and they are checked and displayed by a reader
#the first item in the list tells the computer whether the piece is red or white. the second tells the computer whether the piece is a quen or not
position = { (1,1):["red","n"],
            (1,3):["red","n"],
            (2,2):["red","n"],
            (4,2):["red","n"],
            (3,3):["red","n"],
            (5,1):["red","n"],
            (6,2):["red","n"],
            (5,3):["red","n"],
            (7,1):["red","n"],
            (8,2):["red","n"],
            (7,3):["red","n"],
            (3,1):["red","n"],
            (8,8):["white","n"],
            (7,7):["white","n"],
            (6,6):["white","n"],
            (8,6):["white","n"],
            (6,8):["white","n"],
            (5,7):["white","n"],
            (4,8):["white","n"],
            (4,6):["white","n"],
            (3,7):["white","n"],
            (2,6):["white","n"],
            (2,8):["white","n"],
            (1,7):["white","n"],
            #EMPTY SQUARES
            (1,5):["empty","n"],
            (2,4):["empty","n"],
            (3,5):["empty","n"],
            (4,4):["empty","n"],
            (5,5):["empty","n"],
            (6,4):["empty","n"],
            (7,5):["empty","n"],
            (8,4):["empty","n"],}
# transfers all the keys of the dictionary into keys for easy use 
pos_in_lists = list(position)
#functons that finds out where the mouse is if it is on the board
def board_pos(x,y):
    if x <= 512 and y <= 512:
        cords = [x,y]
        #to find which box it is in as each square is 64 pixels wide
        #the value is rounded up as the top corner is 1,1
        if cords[0] != 0: cords[0] = math.ceil(x/64)
        else: cords[0] = 1
        if cords[1] != 0: cords[1] = math.ceil(y/64)
        else: cords[1] = 1
        return cords
#making sure they played
if did_they_play == True:
    #setting up the pygame window
    wd = pygame.display.set_mode((600,600))
    wd.fill((220,220,220))
    #displaying the board
    wd.blit(board,(0,0))
    #mode is used in the custom board settings to let the computer now what to change to
    mode = ""
    #values[5] is whether custom board is on or off
    if values[7] == True:
        check = False
        # the  code to allow you to change the board
        while check == False:
            wd.fill((220,220,220))
            wd.blit(board,(0,0))
            #for loop to display the board
            for element in pos_in_lists:
                #making sure that if a person places a white piece at the promotion row that it still promotess an doesn't render that square usless
                if (element[1] == 1 and position[element][0] == "white") or (element[1] == 8 and position[element][0] == "red"):
                    position[element][1] = "y"
                #displaying the piece
                if position[element][0] == "red":
                    wd.blit(red,(((element[0]-1)*64)+5,((element[1]-1)*64)+5))
                elif position[element][0] == "white":
                    wd.blit(white,(((element[0]-1)*64)+5,((element[1]-1)*64)+5))
                #displaying crown if piece is a queen
                if position[element][1] == "y" :
                    wd.blit(crown,(((element[0]-1)*64)+16,((element[1]-1)*64)+16))
            #checking if you clicked
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # getting mouse cororinates
                    mx,my = pygame.mouse.get_pos()
                    # finding if the cords are in the board
                    if mx < 512 and my < 512 and mode != "":
                        where_i_clicked = board_pos(mx,my)
                        #figuring out where mode the person clicked which mode they clicked
                        #if they clicked clear it will reomve all pieces,red turns it to a red piece,white a white piece etc. 
                        if mode == "clear":
                            if tuple(where_i_clicked) in pos_in_lists:
                                position[tuple(where_i_clicked)] = ["empty","n"]
                        elif mode == "red":
                            if tuple(where_i_clicked) in pos_in_lists:
                                position[tuple(where_i_clicked)] = ["red","n"]
                        elif mode == "red queen":
                            if tuple(where_i_clicked) in pos_in_lists:
                                position[tuple(where_i_clicked)] = ["red","y"]
                        elif mode == "white":
                            if tuple(where_i_clicked) in pos_in_lists:
                                position[tuple(where_i_clicked)] = ["white","n"]
                        elif mode == "white queen":
                            if tuple(where_i_clicked) in pos_in_lists:
                                position[tuple(where_i_clicked)] = ["white","y"]
                    #checking if you clicked on the mode selctor an changing to the correc selector
                    elif mx >= 0 and mx < 64 and my > 522 and my < 586:
                        check = True
                    elif mx >= 64 and mx < 128 and my >= 522 and my <= 586:
                        mode = "clear"
                    elif mx >= 128 and mx < 192 and my >= 522 and my <= 586:
                        mode = "red"
                    elif mx >= 192 and mx < 256 and my >= 522 and my <= 586:
                        mode = "red queen"
                    elif mx >= 256 and mx < 320 and my >= 522 and my <= 586:
                        mode = "white"
                    elif mx >= 320 and mx < 384 and my >= 522 and my <= 586:
                        mode = "white queen"
                    else:
                        mode = ""
            #putting a backgroun on selecte mode to make it clearer which one you are using
            if mode == "clear":
                wd.blit(last_pos,(64,522))
            elif mode == "red":
                wd.blit(last_pos,(128,522))
            elif mode == "red queen":
                wd.blit(last_pos,(192,522))
            elif mode == "white":
                wd.blit(last_pos,(256,522))
            elif mode == "white queen":
                wd.blit(last_pos,(320,522))
            wd.blit(finshed,(0,522))
            wd.blit(clear,(64,527))
            wd.blit(red,(133,527))
            wd.blit(red,(197,527))
            wd.blit(crown,(208,537))
            wd.blit(white,(261,527))
            wd.blit(white,(325,527))
            wd.blit(crown,(336,537))
            pygame.display.update()
#game function
def play(p1,p2,filename,pauses,turner,posin):
    #varibles set up
    pos = posin
    pos_in_list = list(pos)
    running = True
    turn = "red"
    possible_moves = []
    possible_capture = []
    last_move = []
    move = []
    # data to be stored on the csv
    data = {"winner": [],
                "red_pawns":[],
                "queen":[],
                "white_pawns":[]
    
            }
    winner = ""
    queen = ""
    
    #stop the main playing loop to ch
    failsafe = False 
    capture_chain = ["n",[0,0]]
    who_playing = {"red":p1,
                   "white":p2}
    
    draw_check = True
    original_turn = turner
    turn_checker = [[0,0],[0,0]]
    where_i_clicked = [0,0]
    wd.fill((220,220,220))
    wd.blit(board,(0,0))
    #main game loop    
    while running:
        failsafe = False
        #the draw system check if either player cannot move
        if draw_check == True:
            if turn_checker[0][0] == 0:
                turn = "red"
            elif turn_checker[1][0] == 0:
                turn =  "white"
                
        wd.fill((220,220,220))
        wd.blit(board,(0,0))
        #highlight last made move for you to see easier
        if len(last_move) > 0:
                wd.blit(last_pos,((last_move[0][0]-1)*64,(last_move[0][1]-1)*64))
                wd.blit(last_pos,((last_move[1][0]-1)*64,(last_move[1][1]-1)*64))
        #loops through every position to tell if it can move it checks all around it
        #if a move can be made and then highlights its back, if you click on it a blue circle will appear where the
        #move can be made. Possible moves and capture are stored in lists, from its the pieces staring position to its ending position.
        for element in pos_in_list:
            if pos[element][0] == "red":
                if turn == "red":
                    try:
                        if pos[element[0]+1,element[1]+1][0] == "empty":
                            if who_playing[turn] == "human":
                                 wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                            if [list(element),[element[0]+1,element[1]+1]] not in possible_moves and capture_chain[0] == "n":
                                 possible_moves.append([list(element),[element[0]+1,element[1]+1]])
                            if where_i_clicked == list(element) and who_playing[turn] == "human":
                                 wd.blit(go,(((element[0])*64)+2,((element[1])*64)+2))
                    except KeyError:
                        pass
                    try:
                        if pos[element[0]-1,element[1]+1][0] == "empty" and capture_chain[0] == "n":
                            if who_playing[turn] == "human":
                                 wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                            if [list(element),[element[0]-1,element[1]+1]] not in possible_moves:
                                 possible_moves.append([list(element),[element[0]-1,element[1]+1]])
                            if where_i_clicked == list(element) and who_playing[turn] == "human":
                                 wd.blit(go,(((element[0]-2)*64)+2,((element[1])*64)+2))
                    except KeyError:
                        pass
                    try:
                         if pos[element[0]+1,element[1]+1][0] == "white" and pos[element[0]+2,element[1]+2][0] == "empty":
                                if who_playing[turn] == "human":
                                    wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                if [list(element),[element[0]+2,element[1]+2]] not in possible_capture:
                                    if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                        possible_capture.append([list(element),[element[0]+2,element[1]+2]])
                                    elif capture_chain[0] == "n":
                                        possible_capture.append([list(element),[element[0]+2,element[1]+2]])
                                if where_i_clicked == list(element) and who_playing[turn] == "human":
                                    if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                         wd.blit(go,(((element[0]+1)*64)+2,((element[1]+1)*64)+2))
                                    elif capture_chain[0] == "n":
                                        wd.blit(go,(((element[0]+1)*64)+2,((element[1]+1)*64)+2))
                    except KeyError:
                        pass
                    try:
                            if pos[element[0]-1,element[1]+1][0] == "white" and pos[element[0]-2,element[1]+2][0] == "empty":
                                    if who_playing[turn] == "human":
                                         wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                    if [list(element),[element[0]-2,element[1]+2]] not in possible_capture:
                                         if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                             possible_capture.append([list(element),[element[0]-2,element[1]+2]])
                                         elif capture_chain[0] == "n":
                                            possible_capture.append([list(element),[element[0]-2,element[1]+2]])
                                    if where_i_clicked == list(element) and who_playing[turn] == "human":
                                         if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                             wd.blit(go,(((element[0]-3)*64)+2,((element[1]+1)*64)+2))
                                         elif capture_chain[0] == "n":
                                            wd.blit(go,(((element[0]-3)*64)+2,((element[1]+1)*64)+2))
                    except KeyError:
                            pass
                    if pos[element][1] == "y":
                        try:
                            if pos[element[0]-1,element[1]-1][0] == "empty":
                                if who_playing[turn] == "human":
                                     wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                if [list(element),[element[0]-1,element[1]-1]] not in possible_moves and capture_chain[0] == "n":
                                     possible_moves.append([list(element),[element[0]-1,element[1]-1]])
                                if where_i_clicked == list(element) and who_playing[turn] == "human":
                                    wd.blit(go,(((element[0]-2)*64)+2,((element[1]-2)*64)+2))
                        except KeyError:
                            pass
                        try:
                            if pos[element[0]+1,element[1]-1][0] == "empty":
                                if who_playing[turn] == "human":
                                     wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                if [list(element),[element[0]+1,element[1]-1]] not in possible_moves and capture_chain[0] == "n":
                                     possible_moves.append([list(element),[element[0]+1,element[1]-1]])
                                if where_i_clicked == list(element) and who_playing[turn] == "human":
                                     wd.blit(go,(((element[0])*64)+2,((element[1]-2)*64)+2))
                        except KeyError:
                            pass
                        try:
                             if pos[element[0]-1,element[1]-1][0] == "white" and pos[element[0]-2,element[1]-2][0] == "empty":
                                 if who_playing[turn] == "human":
                                        wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                 if [list(element),[element[0]-2,element[1]-2]] not in possible_capture:
                                        if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                            possible_capture.append([list(element),[element[0]-2,element[1]-2]])
                                        elif capture_chain[0] == "n":
                                            possible_capture.append([list(element),[element[0]-2,element[1]-2]])
                                 if where_i_clicked == list(element) and who_playing[turn] == "human":
                                        if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                             wd.blit(go,(((element[0]-3)*64)+2,((element[1]-3)*64)+2))
                                        elif capture_chain[0] == "n":
                                            wd.blit(go,(((element[0]-3)*64)+2,((element[1]-3)*64)+2))
                        except KeyError:
                            pass
                        try:
                             if pos[element[0]+1,element[1]-1][0] == "white" and pos[element[0]+2,element[1]-2][0] == "empty":
                                    if who_playing[turn] == "human":
                                        wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                    if [list(element),[element[0]+2,element[1]-2]] not in possible_capture:
                                        if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                            possible_capture.append([list(element),[element[0]+2,element[1]-2]])
                                        elif capture_chain[0] == "n":
                                            possible_capture.append([list(element),[element[0]+2,element[1]-2]])
                                    if where_i_clicked == list(element) and who_playing[turn] == "human":
                                        if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                             wd.blit(go,(((element[0]+1)*64)+2,((element[1]-3)*64)+2))
                                        elif capture_chain[0] == "n":
                                            wd.blit(go,(((element[0]+1)*64)+2,((element[1]-3)*64)+2))
                        except KeyError:
                            pass
                wd.blit(red,(((element[0]-1)*64)+5,((element[1]-1)*64)+5))
                if pos[element][1] == "y" :
                    wd.blit(crown,(((element[0]-1)*64)+16,((element[1]-1)*64)+16))
            elif pos[element][0] == "white":
                if turn == "white":
                    try:
                        if pos[element[0]-1,element[1]-1][0] == "empty" and capture_chain[0] == "n":
                             if who_playing[turn] == "human":
                                 wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                             if [list(element),[element[0]-1,element[1]-1]] not in possible_moves and capture_chain[0] == "n":
                                 possible_moves.append([list(element),[element[0]-1,element[1]-1]])
                             if where_i_clicked == list(element) and who_playing[turn] == "human":
                                     wd.blit(go,(((element[0]-2)*64)+2,((element[1]-2)*64)+2))
                    except KeyError:
                        pass
                    try:
                        if pos[element[0]+1,element[1]-1][0] == "empty" and capture_chain[0] == "n":
                             if who_playing[turn] == "human":
                                 wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                             if [list(element),[element[0]+1,element[1]-1]] not in possible_moves:
                                 possible_moves.append([list(element),[element[0]+1,element[1]-1]])
                             if where_i_clicked == list(element) and who_playing[turn] == "human":
                                     wd.blit(go,(((element[0])*64)+2,((element[1]-2)*64)+2))
                    except KeyError:
                        pass
                    try:
                         if pos[element[0]-1,element[1]-1][0] == "red" and pos[element[0]-2,element[1]-2][0] == "empty":
                                if who_playing[turn] == "human":
                                    wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                if [list(element),[element[0]-2,element[1]-2]] not in possible_capture:
                                    if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                        possible_capture.append([list(element),[element[0]-2,element[1]-2]])
                                    elif capture_chain[0] == "n":
                                        possible_capture.append([list(element),[element[0]-2,element[1]-2]])
                                if where_i_clicked == list(element) and who_playing[turn] == "human":
                                    if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                         wd.blit(go,(((element[0]-3)*64)+2,((element[1]-3)*64)+2))
                                    elif capture_chain[0] == "n":
                                        wd.blit(go,(((element[0]-3)*64)+2,((element[1]-3)*64)+2))
                    except KeyError:
                        pass
                    try:
                         if pos[element[0]+1,element[1]-1][0] == "red" and pos[element[0]+2,element[1]-2][0] == "empty":
                                if who_playing[turn] == "human":
                                    wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                if [list(element),[element[0]+2,element[1]-2]] not in possible_capture:
                                    if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                        possible_capture.append([list(element),[element[0]+2,element[1]-2]])
                                    elif capture_chain[0] == "n":
                                        possible_capture.append([list(element),[element[0]+2,element[1]-2]])
                                if where_i_clicked == list(element) and who_playing[turn] == "human":
                                    if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                         wd.blit(go,(((element[0]+1)*64)+2,((element[1]-3)*64)+2))
                                    elif capture_chain[0] == "n":
                                         wd.blit(go,(((element[0]+1)*64)+2,((element[1]-3)*64)+2))
                    except KeyError:
                        pass
                    if pos[element][1] == "y":
                        try:
                            if pos[element[0]+1,element[1]+1][0] == "empty" and capture_chain[0] == "n":
                                 if who_playing[turn] == "human":
                                     wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                 if [list(element),[element[0]+1,element[1]+1]] not in possible_moves:
                                     possible_moves.append([list(element),[element[0]+1,element[1]+1]])
                                 if where_i_clicked == list(element) and who_playing[turn] == "human":
                                     wd.blit(go,(((element[0])*64)+2,((element[1])*64)+2))
                        except KeyError:
                            pass
                        try:
                            if pos[element[0]-1,element[1]+1][0] == "empty" and capture_chain[0] == "n":
                                 if who_playing[turn] == "human":
                                     wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                 if [list(element),[element[0]-1,element[1]+1]] not in possible_moves:
                                     possible_moves.append([list(element),[element[0]-1,element[1]+1]])
                                 if where_i_clicked == list(element) and who_playing[turn] == "human":
                                     wd.blit(go,(((element[0]-2)*64)+2,((element[1])*64)+2))
                        except KeyError:
                            pass
                        try:
                             if pos[element[0]+1,element[1]+1][0] == "red" and pos[element[0]+2,element[1]+2][0] == "empty":
                                    if who_playing[turn] == "human":
                                        wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                    if [list(element),[element[0]+2,element[1]+2]] not in possible_capture:
                                        if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                            possible_capture.append([list(element),[element[0]+2,element[1]+2]])
                                        elif capture_chain[0] == "n":
                                            possible_capture.append([list(element),[element[0]+2,element[1]+2]])
                                    if where_i_clicked == list(element) and who_playing[turn] == "human":
                                        if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                             wd.blit(go,(((element[0]+1)*64)+2,((element[1]+1)*64)+2))
                                        elif capture_chain[0] == "n":
                                            wd.blit(go,(((element[0]+1)*64)+2,((element[1]+1)*64)+2))
                        except KeyError:
                            pass
                        try:
                                if pos[element[0]-1,element[1]+1][0] == "red" and pos[element[0]-2,element[1]+2][0] == "empty":
                                         if who_playing[turn] == "human":
                                             wd.blit(back,(((element[0]-1)*64)+2,((element[1]-1)*64)+2))
                                         if [list(element),[element[0]-2,element[1]+2]] not in possible_capture:
                                            if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                                 possible_capture.append([list(element),[element[0]-2,element[1]+2]])
                                            elif capture_chain[0] == "n":
                                                possible_capture.append([list(element),[element[0]-2,element[1]+2]])
                                         if where_i_clicked == list(element) and who_playing[turn] == "human":
                                             if capture_chain[0] == "y" and capture_chain[1] == list(element):
                                                 wd.blit(go,(((element[0]-3)*64)+2,((element[1]+1)*64)+2))
                                             elif capture_chain[0] == "n":
                                                wd.blit(go,(((element[0]-3)*64)+2,((element[1]+1)*64)+2))
                        except KeyError:
                                pass

                wd.blit(white,(((element[0]-1)*64)+5,((element[1]-1)*64)+5))
                if pos[element][1] == "y":
                    wd.blit(crown,(((element[0]-1)*64)+16,((element[1]-1)*64)+16))
        #draw check system it checks if red can move then if white can move and sees if the game is over or it is a draw
        if draw_check == True:
            if turn_checker == [[1,0],[1,0]]:
                draw_check = False
                failsafe = True
                turn = original_turn
                turn_checker = [[0,0],[0,0]]
            elif turn_checker[0][0] == 0:
                 turn_checker[0][0] = 1
                 if len(possible_capture) == 0 and len(possible_moves) == 0:
                     turn_checker[0][1] = 1
            elif turn_checker[0][0] == 1:
                turn_checker[1][0] = 1
                if len(possible_capture) == 0 and len(possible_moves) == 0:
        
                    if turn_checker[0][1] == 1:
                        winner = "draw"
                    elif turn_checker[0][1] == 0:
                        winner = "red"
                else:
                    if  turn_checker[0][1] == 1:
                        winner = "white"
            possible_moves = []
            possible_capture = []
        #after a capture it checks if the same piece can capture again and if not it will change turns 
        if capture_chain[0] == "y" and len(possible_capture) == 0:
            capture_chain = ["n",[0,0]]
            failsafe = True
            draw_check = True
            if turn == "red":
                turn = "white"
            else:
                turn = "red"
            original_turn = turn
        if failsafe == False and draw_check == False:
            #bots turn system it will choose a random capture if possible
            #then play a random move
            if who_playing[turn] == "bot":
                #pause to make seeing bot moves more visible
                time.sleep(pauses)
                    
                if len(possible_capture) == 0:
                        move = random.choice(possible_moves)
                        #the bot move system clones the first move position data to the second move positions data
                        # and then deletes the first postions data
                        last_move = move
                        possible_moves = []
                        possible_capture = []
                        pos[tuple(move[1])] = pos[tuple(move[0])]
                        pos[tuple(move[0])] = ["empty","n"]
                        draw_check = True
                        if (turn == "red" and move[1][1] == 8) or (turn == "white" and move[1][1] == 1):
                            pos[tuple(move[1])][1] = "y"
                            if queen == "":
                                queen = turn
                                
                        move = []
                        if turn == "red":
                            turn = "white"
                        else:
                            turn = "red"
                        original_turn = turn
                else:
                    move = random.choice(possible_capture)
                    #he capture system does the same thing as the move sytem but it also delets the captured pieces data.
                    #after every move or capture the possible move and captures are reset to allow the new positions possible
                    #moves and captures to be assesed.
                    last_move = move
                    possible_moves = []
                    possible_capture = []
                    pos[tuple(move[1])] = pos[tuple(move[0])]
                    pos[tuple(move[0])] = ["empty","n"]
                    y = [(int((move[0][0]+move[1][0])/2)),(int((move[0][1]+move[1][1])/2))]
                    pos[tuple(y)] = ["empty","n"]
                    capture_chain[0] = "y"
                    capture_chain[1] = move[1]
                    if (turn == "red" and move[1][1] == 8) or (turn == "white" and move[1][1] == 1):
                        pos[tuple(move[1])][1] = "y"
                        if queen == "":
                            queen = turn
                            
                    move = []
        if capture_chain[0] == "y" and who_playing[turn] == "human":
            wd.blit(cross,(512,512))
        #gatering input data
        for event in pygame.event.get():
            #gathers if you clicked the screen and gets cords on screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                # feature so you are not forced to multi-capture and you can press a button at the bootom of the screen
                if mx>512 and mx<512+46 and my>512 and my<512+44 and capture_chain[0] == "y":
                    capture_chain = ["n",[0,0]]
                    possible_moves = []
                    possible_capture= []
                    move = []
                    if turn == "red":
                        turn = "white"
                    else:
                        turn = "red"
                #checks if you clicked the checkers board
                if mx < 512 and my < 512:
                    # turns the click in to a useful square
                    where_i_clicked = board_pos(mx,my)
                    #the code below tracks where you clicked and stores it, it waits till you click another square
                    #store the other value in to the same list and checks if the list it created is in the possible
                    #capture or possible move lists. capture system is the same way the bot does it.
                    if failsafe == False and draw_check == False:
                        if who_playing[turn] == "human":
                            if any(where_i_clicked == x[0] for x in possible_moves+possible_capture) and len(move) == 0:
                                    move.append(where_i_clicked)
                            elif len(move) == 1:
                                move.append(where_i_clicked)
                                if any(move == x for x in possible_moves):
                                    possible_moves = []
                                    possible_capture= []
                                    pos[tuple(move[1])] = pos[tuple(move[0])]
                                    pos[tuple(move[0])] = ["empty","n"]
                                    if (turn == "red" and move[1][1] == 8) or (turn == "white" and move[1][1] == 1):
                                        pos[tuple(move[1])][1] = "y"

                                        if queen == "":
                                            queen = turn
                                            
                                    last_move = move
                                    move = []
                                    draw_check = True
                                    
                                    if turn == "red":
                                        turn = "white"
                                    else:
                                        turn = "red"
                                    original_turn = turn
                                elif any(move == x for x in possible_capture):
                                    possible_moves = []
                                    possible_capture = []
                                    pos[tuple(move[1])] = pos[tuple(move[0])]
                                    pos[tuple(move[0])] = ["empty","n"]
                                    y = [(int((move[0][0]+move[1][0])/2)),(int((move[0][1]+move[1][1])/2))]
                                    pos[tuple(y)] = ["empty","n"]
                                    capture_chain[0] = "y"
                                    capture_chain[1] = move[1]
                                    last_move = move
                                    
                                    if (turn == "red" and move[1][1] == 8) or (turn == "white" and move[1][1] == 1):
                                        pos[tuple(move[1])][1] = "y"
                                        if queen == "":
                                            queen = turn
                                    move = []
                                else:
                                    move = []
                                
                    
        
        #updates the images
        pygame.display.update()
        #breaks the main loop if a winner is found
        if winner == "red":
            draw_check = False
            break
            
        elif winner == "white":
            draw_check = False
            break
        if winner == "draw":
            draw_check = False
            #if both players cannot move this check who has more pieces then kings to
            #see who won or drew
            final_red = 0
            final_white = 0
            red_queen = 0
            white_queen = 0
            for element in pos_in_list:
                if pos[element][0] == "red":
                    final_red +=1
                    if pos[element][1] == "y":
                        red_queen+=1
                elif pos[element][0] == "white":
                    final_white +=1
                    if pos[element][1] == "y":
                        white_queen+=1
            if final_red > final_white:
                winner = "red"
            elif final_red < final_white:
                winner = "white"
            elif final_red == final_white:
                if white_queen > red_queen:
                    winner = "white"
                elif red_queen > white_queen:
                    winner = "red"
                elif red_queen == white_queen:
                    winner  = "draw"
            break
    
    wd.fill((220,220,220))
    wd.blit(board,(0,0))
    #displays final postion of everything
    for element in pos_in_list:
            if list(element) in last_move:
                wd.blit(last_pos,((element[0]-1)*64,(element[1]-1)*64))
            if pos[element][0] == "red":
                wd.blit(red,(((element[0]-1)*64)+5,((element[1]-1)*64)+5))
            elif pos[element][0] == "white":
                wd.blit(white,(((element[0]-1)*64)+5,((element[1]-1)*64)+5))
            if pos[element][1] == "y" :
                wd.blit(crown,(((element[0]-1)*64)+16,((element[1]-1)*64)+16))
    
    final_red = 0
    final_white = 0
    red_queen = 0
    white_queen = 0
    #gathers how many pieces are left
    for element in pos_in_list:
        if pos[element][0] == "red":
            final_red +=1
            if pos[element][1] == "y":
                red_queen+=1
        elif pos[element][0] == "white":
            final_white +=1
            if pos[element][1] == "y":
                white_queen+=1
    #prints ending screens
    if winner == "red":
        wd.blit(red_wins,(0,0))
    elif winner == "white":
        wd.blit(white_wins,(0,0))
    else:
        wd.blit(draw,(0,0))
    pygame.display.update()
    #code for gathering 4 pieces of data
    if queen == "":
        queen = "nobody made a king"
    data["winner"].append(winner)
    data["queen"].append(queen)
    data["red_pawns"].append(final_red)
    data["white_pawns"].append(final_white)
    df = pd.DataFrame(data)
    #it create a csv file if it doesn't exist or adds data to it
    if filename == "":
        if os.path.isfile("data.csv") == True:
            df.to_csv("data.csv", mode='a', index=False, header=False)
        else:
            df.to_csv(filename+".csv", mode='a', index=False, header=data.keys())
    elif os.path.isfile(filename+".csv") == False:
        df.to_csv(filename+".csv", mode='a', index=False, header=data.keys())
    else:
        df.to_csv(filename+".csv", mode='a', index=False, header=False)
#counter checks how many rouns were played   
counter = 1
#dictionary needs to  be deepcopied to make sure one of them isn't changed an retains the starting position
p_copy = copy.deepcopy(position)

while counter <= values[6] and did_they_play == True:
    
    
    play(player1,player2,values["csv_name"],float(values["pause"]),first_turn,position)
    position = copy.deepcopy(p_copy)
    counter+=1
#closes the window
pygame.quit()
#analysis
if did_they_play == True or values[0] == True:
    #reading the csv
    csv = pd.read_csv(values["csv_name"]+".csv")
    #gathering all the data into list for use
    winner = csv.winner.to_list()
    red_pawns = csv.red_pawns.to_list()
    white_pawns = csv.white_pawns.to_list()
    queens  = csv.queen.to_list()
    # creating dictionarys so i can diplay data as a graph
    winner_counter = {}
    first_queen = {}
    red_counter = {}
    white_counter = {}
    #special case for who queened first as it compares two incoming data sets
    queen = {"Yes":0,
             "No":0, "Nobody made a king": 0}
    #tallies up the data sets
    for element in winner:
        if element in list(winner_counter.keys()):
            winner_counter[element] +=1
        else:
            winner_counter[element] = 1
    for element in queens:
        if element in list(first_queen.keys()):
            first_queen[element] +=1
        else:
            first_queen[element] = 1


    red_mean = [0,0]
    red_mode = []
    white_mean = [0,0]
    white_mode = []
    #gathers mean and mode
    for i in range(len(red_pawns)):
        if red_pawns[i] == 0 or winner[i] == "white":
            pass
        elif red_pawns[i] in list(red_counter.keys()):
            red_counter[red_pawns[i]] +=1
            red_mean[0] += red_pawns[i]
            red_mean[1] +=1
        else:
            red_counter[red_pawns[i]] = 1
            red_mean[0] += red_pawns[i]
            red_mean[1] +=1
    try:
        red_mean[0] /= red_mean[1]
    except ZeroDivisionError:
        red_mean[0] = 0
    for element in list(red_counter.keys()):
        if red_counter[element] == max(red_counter.values()):
            red_mode.append(str(element))
    red_mean[0] = round(red_mean[0],2)
    for i in range(len(white_pawns)):
        if white_pawns[i] == 0 or winner[i] == "red":
            pass
        elif white_pawns[i] in list(white_counter.keys()):
            white_counter[white_pawns[i]] +=1
            white_mean[0] += white_pawns[i]
            white_mean[1] += 1
        else:
            white_counter[white_pawns[i]] = 1
            white_mean[0] += white_pawns[i]
            white_mean[1] += 1
    for element in list(white_counter.keys()):
        if white_counter[element] == max(white_counter.values()):
            white_mode.append(str(element))
    try:
        white_mean[0] /= white_mean[1]
    except ZeroDivisionError:
        white_mean[0] = 0
    white_mean[0] = round(white_mean[0],2)
    for i in range(len(queens)):
        if queens[i] != "*":
            if queens[i] == "nobody made a king":
                queen["Nobody made a king"]+=1
            elif queens[i] == winner[i]:
                queen["Yes"]+=1
            else:
                queen["No"] +=1
    temp = []
    for element in queen.keys():
        if queen[element] == 0:
            temp.append(element)
    for element in temp:
        del queen[element]
    red_zero = False
    white_zero = False
    red_ticker = white_ticker = 1
    while red_zero == False and white_zero == False:
        if red_ticker not in red_counter.keys():
            red_counter[red_ticker] = 0
            red_ticker+=1
        else:
            red_zero = True
        if white_ticker not in white_counter.keys():
            white_counter[red_ticker] = 0
            white_ticker+=1
        else:
            white_zero = True
            
    #used for creating barcharts to be displayed on tabs
    def create_bar(x, y,z,mean):
        plt.figure()
        plt.bar(x, y)
        plt.title(z, fontsize= 14)
        plt.axvline(mean, color='black', linewidth=2)
        return plt.gcf()
    #used for creating pie charts to be displayed on tabs
    def create_pie(x, y,z):
        plt.figure()
        plt.pie(y, labels = x, autopct='%1.1f%%', shadow=True, startangle=80)
        plt.title(z, fontsize=14)
        return plt.gcf()
    #function to draw graphs onto pysimple gui
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    #define layout for each tabs
    layout1 = [[sg.Text('(Black line is the mean)')],
               [sg.Text("no. of games red won: "+str(red_mean[1]))
                ,sg.Text("mean:"+str(red_mean[0])),
               sg.Text("mode: "+ ', '.join(red_mode)),
                ],
              [sg.Canvas(size=(500, 500), key='red pawn')],
              [sg.Exit()]]
    layout2 = [[sg.Text('(Black line is the mean)')],
               [sg.Text("no. of games white won: "+str(white_mean[1]))
                   ,sg.Text("mean:"+(str(white_mean[0]))),
                sg.Text("mode: "+ ", ".join(white_mode))],
              [sg.Canvas(size=(500, 500), key='white pawn')],
              [sg.Exit()]]
    layout3= [[sg.Text("no. of games: "+str(len(winner)))],
              [sg.Canvas(size=(500, 500), key='first king')],
              [sg.Exit()]]
    layout4= [[sg.Text("no. of games: "+str(len(winner)))],
              [sg.Canvas(size=(500, 500), key='winner')],
              [sg.Exit()]]
    layout5 = [[sg.Text("no. of games: "+str(len(winner)))],
              [sg.Canvas(size=(500, 500), key='creater')],
              [sg.Exit()]]
    #Define Layout combining tabs Tabs         
    tabgrp = [[sg.TabGroup([[sg.Tab('who won', layout4, title_color='Red',border_width =10,
                                     element_justification= 'center'),
                        sg.Tab('red pawns left', layout1,title_color='Blue',  element_justification= 'center'),
                             sg.Tab('white pawns left', layout2,title_color='Blue',  element_justification= 'center'),
                             sg.Tab('first to king', layout5,title_color='Blue', element_justification= 'center'),
                        sg.Tab('first to king win', layout3,title_color='Black',
                               
                               element_justification= 'center')]], tab_location='centertop',border_width=5)
               
               ]]  
            
    #Define Window
    window =sg.Window("data analysis",tabgrp,finalize=True, element_justification='center')
    #using functions above to draw graphs onto the tabs
    draw_figure(window['red pawn'].TKCanvas, create_bar(red_counter.keys(), red_counter.values(),"How many pieces did red win with",red_mean[0]))
    draw_figure(window['white pawn'].TKCanvas, create_bar(white_counter.keys(), white_counter.values(),"How many pieces did white win wtih",white_mean[0]))
    draw_figure(window['first king'].TKCanvas, create_pie(queen.keys(), queen.values(),"Did the first person to create a king win"))
    draw_figure(window['winner'].TKCanvas, create_pie(winner_counter.keys(), winner_counter.values(),"Who won"))
    draw_figure(window['creater'].TKCanvas, create_pie(first_queen.keys(), first_queen.values(),"First player to create a king"))
    #Read  values entered by user
    event,values=window.read()
    #access all the values and if selected add them to a list
    window.close()
    