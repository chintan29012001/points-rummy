"""
PRESS M TO MELD
"""
import arcade
import math
import os
from random import *
import threading
import time
from enum import Enum

from Card import card
#from comp import *

class GameState(Enum):
    """ Store game state in enum """

    MENU = 1
    player_vs_comp = 2
    player_vs_player = 3
    GAME_RUNNING = 4
    GAME_OVER = 5



class GameManager(arcade.Window):
    """
    Main application class.
    """
    

    def __init__(self, GAME_CONFIG):
        """ Initializer """

        # Get config data
        self.GAME_CONFIG = GAME_CONFIG
        self.SCREEN_WIDTH = GAME_CONFIG["general_settings"]["screen_width"]
        self.SCREEN_HEIGHT = GAME_CONFIG["general_settings"]["screen_height"]
        self.SCREEN_TITLE = GAME_CONFIG["general_settings"]["screen_title"]
        self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["sprite_scaling"]
        self.GAME_OVER_DELAY = GAME_CONFIG["general_settings"]["game_over_delay"]
        self.BACKGROUND_INGAME = GAME_CONFIG["assets_path"]["images"]["background_ingame"]
        self.BACKGROUND_GAMEOVER = GAME_CONFIG["assets_path"]["images"]["background_gameover"]
        self.draw=0
        self.flg=0
        self.meld=False
        self.meld_list=[]
        self.meld_cards=[]
        self.button_list=None

        # Call the parent class initializer
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Initialize the game state
        self.current_state = GameState.MENU

        # Background image will be stored in this variable
        self.background = None

        # Variables that hold individual sprites
        self.cards = []
        self.back_of_card=None
        self.button_list=None
        # Variables that will hold sprite lists
        self.comp_cards = []
        self.self_cards=[]
        #self.cards2=[]
        self.c1=None
        self.c2=None
        self.p1 = []
        self.shown_deck=[]
        self.hidden_deck=[]
        # Set up the game score
        self.score = 0
        self.stage = 1
        self.score_text = None
        self.turn='p'
        # Set the background color
        arcade.set_background_color(arcade.color.AO)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        self.background_ingame = arcade.load_texture(self.BACKGROUND_INGAME)
        self.background_gameover = arcade.load_texture(self.BACKGROUND_GAMEOVER)

        self.button_list=[]
        self.cards=arcade.SpriteList()
        #self.cards2=arcade.SpriteList()
        self.comp = arcade.SpriteList()
        self.p1 = arcade.SpriteList()
        self.self_cards=arcade.SpriteList()
        self.comp_cards=arcade.SpriteList()
        self.shown_deck = arcade.SpriteList()
        self.hidden_deck = arcade.SpriteList()
        self.c1=arcade.SpriteList()
        self.c2=arcade.SpriteList()
        self.meld_cards=arcade.SpriteList()
        self.back_of_card=arcade.SpriteList()
        # Set up the cards in the deck
        self.create_cards()
        while(len(self.comp_cards)<10):
            x=randint(0,51)
            if(self.cards[x] not in self.comp_cards):
                self.comp_cards.append(self.cards[x])
        xo=0
        while(len(self.self_cards)<10):
            x=randint(0,51)
            m=randint(0,1)
            if(self.cards[x] not in self.comp_cards and abs(xo-x)>=1 and m==1 and self.cards[x] not in self.self_cards ):
                self.self_cards.append(self.cards[x])
                xo=x
            if(self.cards[x] not in self.comp_cards and abs(xo-x)!=13 and m==0 and self.cards[x] not in self.self_cards):
                self.self_cards.append(self.cards[x])
                xo=x
        while(len(self.hidden_deck)!=len(self.cards)-20):
            x=randint(0,51)
            if(self.cards[x] not in self.self_cards and self.cards[x] not in self.comp_cards):
                self.hidden_deck.append(self.cards[x])
        self.shown_deck.append(self.hidden_deck.pop())
        

    
    
    def draw_menu(self):
        """ Draw main menu across the screen. """

        # Draw the background texture
        arcade.draw_texture_rectangle(
            self.SCREEN_WIDTH //2, 
            self.SCREEN_HEIGHT//2,
            self.SCREEN_WIDTH, 
            self.SCREEN_HEIGHT, 
            self.background_gameover)

        # Draw logo
        self.logo_list = arcade.SpriteList()
        self.logo = arcade.Sprite(self.GAME_CONFIG["assets_path"]["images"]["logo"],0.6)
        self.logo.center_x = self.SCREEN_WIDTH*0.1
        self.logo.center_y = self.SCREEN_HEIGHT*0.5
        self.logo_list.append(self.logo)
        self.logo_list.draw()

        # Display "Game Over" text
        # output = "Python Knife Hit"
        # arcade.draw_text(output, self.SCREEN_WIDTH*0.5, self.SCREEN_HEIGHT*0.6, arcade.color.WHITE, 54,  align="center", anchor_x="center")

        # Display restart instruction
        output = "Press The required key:"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.8, self.SCREEN_HEIGHT*0.60, arcade.color.WHITE, 24,  align="center", anchor_x="center")
        output = "1. PLayer vs Computer"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.8, self.SCREEN_HEIGHT*0.50, arcade.color.WHITE, 24,  align="center", anchor_x="center")
        output = "Points Rummy"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.8, self.SCREEN_HEIGHT*0.80, arcade.color.WHITE, 30,  align="center", anchor_x="center")
        output = "2. Quit"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.8, self.SCREEN_HEIGHT*0.30, arcade.color.WHITE, 24,  align="center", anchor_x="center")

    def draw_game_over(self):
        """ Draw game over menu across the screen. """

        # Reset the score and stage number
        self.score = 0
        self.stage = 1

        # Draw the background texture
        arcade.draw_texture_rectangle(
            self.SCREEN_WIDTH // 2, 
            self.SCREEN_HEIGHT // 2,
            self.SCREEN_WIDTH, 
            self.SCREEN_HEIGHT, 
            self.background_gameover)

        # Display "Game Over" text
        output = "Game Over"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.5, self.SCREEN_HEIGHT*0.6, arcade.color.WHITE, 54,  align="center", anchor_x="center")

        # Display restart instruction
        output = "Press <ENTER> To Restart"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.5, self.SCREEN_HEIGHT*0.55, arcade.color.WHITE, 24,  align="center", anchor_x="center")
    
    def draw_game(self):
        """ Draw all the sprites, along with the score. """

        # Draw the background texture
        arcade.draw_texture_rectangle(
            self.SCREEN_WIDTH // 2, 
            self.SCREEN_HEIGHT // 2,
            self.SCREEN_WIDTH, 
            self.SCREEN_HEIGHT, 
            self.background_ingame
            )

        
        output = f"{self.score}"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.1, self.SCREEN_HEIGHT*0.95, (239, 182, 90), 28,align="center", anchor_x="center", anchor_y="center",)
        
        
        self.g=0.1
        #print(len(self.self_cards))
        for i in range(len(self.self_cards)):
            self.self_cards[i].center_y = self.SCREEN_HEIGHT*0.2
            self.self_cards[i].center_x = self.SCREEN_WIDTH*self.g
            self.self_cards[i].draw()
            self.g+=0.08
        self.g=0.1
        for i in range(len(self.comp_cards)):
            m=card('1','R',self.GAME_CONFIG)
            m.center_y = self.SCREEN_HEIGHT*0.8
            m.center_x = self.SCREEN_WIDTH*self.g
            self.g+=0.08
            m.draw()
        self.back_of_card.draw()
        if(len(self.shown_deck)!=0):
            self.shown_deck[-1].center_y=self.SCREEN_HEIGHT*0.5
            self.shown_deck[-1].center_x=self.SCREEN_WIDTH*0.6
            self.shown_deck[-1].draw()
        g=0.1
        for  i in range(len(self.meld_cards)):
            self.meld_cards[i].center_y=self.SCREEN_HEIGHT*0.55
            self.meld_cards[i].center_x=self.SCREEN_WIDTH*g
            self.meld_cards[i].draw()
            g+=0.08

        self.h=0.65
        for j in self.meld_list:
            g=0.8
            for  i in range(len(j)):
                j[i].center_y=self.SCREEN_HEIGHT*self.h
                j[i].center_x=self.SCREEN_WIDTH*g
                j[i].draw()
                g+=0.02
            self.h-=0.1
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        i=0
        if(self.draw==1 and self.turn=='p' and self.meld==False):

            while i <len(self.self_cards):
                if(self.self_cards[i].center_x-self.SCREEN_WIDTH*0.04<=x<=self.self_cards[i].center_x+self.SCREEN_WIDTH*0.04):
                    if(self.self_cards[i].center_y-self.SCREEN_HEIGHT*0.04<=y<=self.self_cards[i].center_y+self.SCREEN_HEIGHT*0.04):
                        self.self_cards[i].center_y=self.SCREEN_HEIGHT*0.5
                        self.self_cards[i].center_x=self.SCREEN_WIDTH*0.6
                        m=card(self.self_cards[i].no,self.self_cards[i].suit,self.GAME_CONFIG)
                        if (not (m.no==self.m.no and m.suit==self.m.suit)):
                            self.shown_deck.append(m)
                            self.self_cards[i].remove_from_sprite_lists()
                            self.draw=0
                            self.flg=0
                            self.turn='c'
                            break
                i+=1
        elif(self.draw==1 and self.turn=='p' and self.meld==True and len(self.meld_cards)<5):
            while i<(len(self.self_cards)):
                if(self.self_cards[i].center_x-self.SCREEN_WIDTH*0.04<=x<=self.self_cards[i].center_x+self.SCREEN_WIDTH*0.04):
                    if(self.self_cards[i].center_y-self.SCREEN_HEIGHT*0.04<=y<=self.self_cards[i].center_y+self.SCREEN_HEIGHT*0.04):
                        m=card(self.self_cards[i].no,self.self_cards[i].suit,self.GAME_CONFIG)
                        self.meld_cards.append(m)
                        self.self_cards[i].remove_from_sprite_lists()
                        self.flg=1
                        break
                i+=1

        elif(self.draw==0 and self.flg==0 and self.turn=='p'):
            if(self.shown_deck[-1].center_x-self.SCREEN_WIDTH*0.04<=x<=self.shown_deck[-1].center_x+self.SCREEN_WIDTH*0.04):
                if(self.shown_deck[-1].center_y-self.SCREEN_HEIGHT*0.04<=y<=self.shown_deck[-1].center_y+self.SCREEN_HEIGHT*0.04):
                    self.shown_deck[-1].center_y=self.SCREEN_HEIGHT*0.2
                    self.shown_deck[-1].center_x=self.SCREEN_WIDTH*self.g
                    self.m=card(self.shown_deck[-1].no,self.shown_deck[-1].suit,self.GAME_CONFIG)
                    self.self_cards.append(self.m)
                    self.shown_deck[-1].remove_from_sprite_lists()
                    self.draw=1
                    self.flg=1
            if(self.back_of_card.center_x-self.SCREEN_WIDTH*0.04<=x<=self.back_of_card.center_x+self.SCREEN_WIDTH*0.04):
                if(self.back_of_card.center_y-self.SCREEN_HEIGHT*0.04<=y<=self.back_of_card.center_y+self.SCREEN_HEIGHT*0.04):
                    if(len(self.hidden_deck)==1):
                        self.trigger_game_over()
                    else:    
                        self.hidden_deck[-1].center_y=self.SCREEN_HEIGHT*0.2
                        self.hidden_deck[-1].center_x=self.SCREEN_WIDTH*self.g
                        self.m=card(self.hidden_deck[-1].no,self.hidden_deck[-1].suit,self.GAME_CONFIG)
                        self.self_cards.append(self.m)
                        self.hidden_deck[-1].remove_from_sprite_lists()
                        self.draw=1
                        self.flg=1

    def meld_comp(self,i,j,k):
        self.meld_cards.append(self.comp_cards[i])
        self.meld_cards.append(self.comp_cards[j])
        self.meld_cards.append(self.comp_cards[k])
        z=arcade.SpriteList()
        for i in range(len(self.meld_cards)):
            m=card(self.meld_cards[i].no,self.meld_cards[i].suit,self.GAME_CONFIG,1)
            z.append(m)
        self.meld_list.append(z)
        while(len(self.meld_cards)>0):
            self.meld_cards[0].remove_from_sprite_lists()


    def on_update(self,delta_time):
        draw_from_shown=False
        if(len(self.hidden_deck)<1 or len(self.self_cards)<3 or len(self.comp_cards)<3):
            self.trigger_game_over()
        if(self.turn=='c'):
            i=0
            while i<len(self.comp_cards)-1:
                j=i+1
                while j <len(self.comp_cards):
                    if(self.comp_cards[i].num==self.comp_cards[j].num):
                        if(self.shown_deck[-1].num==self.comp_cards[i].num):
                            draw_from_shown=True
                            break
                    if(self.comp_cards[i].num+1==self.comp_cards[j].num and self.comp_cards[i].suit==self.comp_cards[j].suit):
                        if((self.shown_deck[-1].num==self.comp_cards[i].num-1 or self.shown_deck[-1].num==self.comp_cards[j].num+1) and self.shown_deck[-1].suit==self.comp_cards[i].suit):
                            draw_from_shown=True
                            break
                    if(self.comp_cards[i].num-1==self.comp_cards[j].num and self.comp_cards[i].suit==self.comp_cards[j].suit):
                        if((self.shown_deck[-1].num==self.comp_cards[j].num-1 or self.shown_deck[-1].num==self.comp_cards[i].num+1) and self.shown_deck[-1].suit==self.comp_cards[i].suit):
                            draw_from_shown=True
                            break
                    if(self.comp_cards[i].num+2==self.comp_cards[j].num and self.comp_cards[i].suit==self.comp_cards[j].suit):
                        if((self.shown_deck[-1].num==self.comp_cards[i].num+1) and self.shown_deck[-1].suit==self.comp_cards[i].suit):
                            draw_from_shown=True
                            break
                    if(self.comp_cards[i].num-2==self.comp_cards[j].num and self.comp_cards[i].suit==self.comp_cards[j].suit):
                        if((self.shown_deck[-1].num==self.comp_cards[i].num-1) and self.shown_deck[-1].suit==self.comp_cards[i].suit):
                            draw_from_shown=True
                            break
                    j+=1
                i+=1
            if(draw_from_shown==True):
                self.g=0.1
                self.shown_deck[-1].center_y=self.SCREEN_HEIGHT*0.8
                self.shown_deck[-1].center_x=self.SCREEN_WIDTH*self.g
                self.m=card(self.shown_deck[-1].no,self.shown_deck[-1].suit,self.GAME_CONFIG,0,1)
                self.g+=0.08
                self.comp_cards.append(self.m)
                self.copy_of_shown=self.shown_deck[-1]
                self.shown_deck[-1].remove_from_sprite_lists()
            else:
                self.hidden_deck[-1].center_y=self.SCREEN_HEIGHT*0.8
                self.hidden_deck[-1].center_x=self.SCREEN_WIDTH*self.g
                self.m=card(self.hidden_deck[-1].no,self.hidden_deck[-1].suit,self.GAME_CONFIG,0,1)
                self.comp_cards.append(self.m)
                self.hidden_deck[-1].remove_from_sprite_lists()


            i=0
            j=0
            k=0
            while(i<len(self.comp_cards)):
                j=i+1
                while(j<len(self.comp_cards)):
                    k=j+1
                    flg=0
                    while(k<len(self.comp_cards)):
                        
                        if(self.comp_cards[i].num==self.comp_cards[j].num):
                            if(self.comp_cards[k].num==self.comp_cards[i].num):
                                self.meld_comp(i,j,k)
                                flg=1                                
                        if(self.comp_cards[i].num+1==self.comp_cards[j].num and self.comp_cards[i].suit==self.comp_cards[j].suit):
                            if((self.comp_cards[k].num==self.comp_cards[i].num-1 or self.comp_cards[k].num==self.comp_cards[j].num+1) and self.shown_deck[-1].suit==self.comp_cards[i].suit):
                                self.meld_comp(i,j,k)
                                flg=1
                        if(self.comp_cards[i].num-1==self.comp_cards[j].num and self.comp_cards[i].suit==self.comp_cards[j].suit):
                            if((self.shown_deck[-1].num==self.comp_cards[j].num-1 or self.shown_deck[-1].num==self.comp_cards[i].num+1) and self.shown_deck[-1].suit==self.comp_cards[i].suit):
                                self.meld_comp(i,j,k)
                                flg=1
                        if(flg==0):
                            k+=1
                    j+=1
                i+=1
            max_card=self.comp_cards[0]
            if(draw_from_shown==True):
                for i in range(len(self.comp_cards)):
                        if(max_card.num<self.comp_cards[i].num and not (max_card.no==self.copy_of_shown.no and max_card.suit==self.copy_of_shown.suit)):
                            max_card=self.comp_cards[i]
                m=card(max_card.no,max_card.suit,self.GAME_CONFIG)
                self.shown_deck.append(m)
                i=0
                while(i <len(self.comp_cards)):
                    if(max_card.no==self.comp_cards[i].no and max_card.suit==self.comp_cards[i].suit):
                        self.comp_cards[i].remove_from_sprite_lists()
                        break
                    i+=1
            else:
                for i in range(len(self.comp_cards)):
                        if(max_card.num<self.comp_cards[i].num):
                            max_card=self.comp_cards[i]
                
                m=card(max_card.no,max_card.suit,self.GAME_CONFIG)
                self.shown_deck.append(m)
                i=0
                while(i<len(self.comp_cards)):
                    if(max_card.num==self.comp_cards[i].num and max_card.suit==self.comp_cards[i].suit):
                        self.comp_cards[i].remove_from_sprite_lists()
                        break
                    i+=1

            if(len(self.comp_cards)<=1):
                self.trigger_game_over()
            self.turn='p'         

            

    def mel(self):
        asc=0
        dsc=0
        eq=0
        f=0
        if(len(self.meld_cards)==3):
            if(self.meld_cards[0].num>self.meld_cards[1].num and self.meld_cards[0].suit==self.meld_cards[1].suit):
                for i in range(len(self.meld_cards)-1):
                    if(self.meld_cards[i].num!=self.meld_cards[i+1].num+1):
                            dsc=1
                if(dsc==1):
                    print("not dsc")
                    output = "Invalid Meld"
                    print(output)
                    while(len(self.meld_cards)>0):
                        m=card(self.meld_cards[0].no,self.meld_cards[0].suit,self.GAME_CONFIG)
                        self.self_cards.append(m)
                        self.meld_cards[0].remove_from_sprite_lists()                        
                else:
                    z=arcade.SpriteList()
                    for i in range(len(self.meld_cards)):
                        m=card(self.meld_cards[i].no,self.meld_cards[i].suit,self.GAME_CONFIG,1)
                        z.append(m)
                    self.meld_list.append(z)
                    while(len(self.meld_cards)>0):
                        self.meld_cards[0].remove_from_sprite_lists()
                        
            elif(self.meld_cards[0].num<self.meld_cards[1].num and self.meld_cards[0].suit==self.meld_cards[1].suit):
                for i in range(len(self.meld_cards)-1):
                    if(self.meld_cards[i].num!=self.meld_cards[i+1].num-1):
                        asc=1
                        break
                if(asc==1):
                    print("not asc")
                    output = "Invalid Meld"
                    print(output)
                    while(len(self.meld_cards)>0):
                        m=card(self.meld_cards[0].no,self.meld_cards[0].suit,self.GAME_CONFIG)
                        self.self_cards.append(m)
                        self.meld_cards[0].remove_from_sprite_lists()
                else:
                    z=arcade.SpriteList()
                    for i in range(len(self.meld_cards)):
                        m=card(self.meld_cards[i].no,self.meld_cards[i].suit,self.GAME_CONFIG,1)
                        z.append(m)
                    self.meld_list.append(z)
                    while(len(self.meld_cards)>0):
                        self.meld_cards[0].remove_from_sprite_lists()
            elif(self.meld_cards[0].num==self.meld_cards[1].num):
                for i in range(len(self.meld_cards)-1):
                    if(self.meld_cards[i].num!=self.meld_cards[i+1].num):
                        eq=1
                        break
                if(eq==1):
                    print("not eq")
                    for i in range(len(self.meld_cards)):
                        print(self.meld_cards[i].num)
                    output = "Invalid Meld"
                    print(output)
                    while(len(self.meld_cards)>0):
                        m=card(self.meld_cards[0].no,self.meld_cards[0].suit,self.GAME_CONFIG,1)
                        self.self_cards.append(m)
                        self.meld_cards[0].remove_from_sprite_lists()
                else:
                    z=arcade.SpriteList()
                    for i in range(len(self.meld_cards)):
                        m=card(self.meld_cards[i].no,self.meld_cards[i].suit,self.GAME_CONFIG,1)
                        z.append(m)
                    self.meld_list.append(z)
                    while(len(self.meld_cards)>0):
                        self.meld_cards[0].remove_from_sprite_lists()
            
            else:
                print("meld not possible")
                while(len(self.meld_cards)>0):
                    m=card(self.meld_cards[0].no,self.meld_cards[0].suit,self.GAME_CONFIG)
                    self.self_cards.append(m)
                    self.meld_cards[0].remove_from_sprite_lists()
            self.meld=False
        else:
            print("meld not possible")
            while(len(self.meld_cards)>0):
                m=card(self.meld_cards[0].no,self.meld_cards[0].suit,self.GAME_CONFIG)
                self.self_cards.append(m)
                self.meld_cards[0].remove_from_sprite_lists()
            self.meld=False

    def create_cards(self):
        """ sets up cards in deck """
        l=['H','S','C','D']
        k=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        shuffle(l)
        shuffle(k)
        self.back_of_card=card('1','R',self.GAME_CONFIG)
        self.back_of_card.center_y = self.SCREEN_HEIGHT*0.5
        self.back_of_card.center_x = self.SCREEN_WIDTH*0.4
        
        for i in range(4):
            for j in range(13):
                self.m=card(k[j],l[i],self.GAME_CONFIG)
                self.cards.append(self.m)

    def trigger_game_over(self):
        """ Trigger game over after certain delay """
        if(len(self.comp_cards)<2):
            output="You Lose"
        elif(len(self.self_cards)<2):
            output="You won"
        else:
            output="It was a tie"    
        time.sleep(30)
        self.current_state = GameState.GAME_OVER

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Redirect to main menu
        if self.current_state == GameState.MENU:
            self.draw_menu()

        # Redirect to in game screen
        elif self.current_state == GameState.GAME_RUNNING:
            self.draw_game()

        # Redirect to game over screen
        else:
            # self.draw_game()
            self.draw_game_over()
    
    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        # Shoot knife
    
        if(key == arcade.key.KEY_1 and(self.current_state == GameState.GAME_OVER or self.current_state == GameState.MENU)):
            self.setup()
            self.current_state = GameState.GAME_RUNNING

        if key == arcade.key.F5:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen) and self.current_state == GameState.GAME_RUNNING

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        if(key == arcade.key.M and self.current_state == GameState.GAME_RUNNING):
            self.meld=True
            self.current_state = GameState.GAME_RUNNING

        if key == arcade.key.ESCAPE:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, self.SCREEN_WIDTH, 0, self.SCREEN_HEIGHT)
        if(key== arcade.key.KEY_2 and(self.current_state == GameState.GAME_OVER or self.current_state == GameState.MENU)):
            quit()

        if(key==arcade.key.ENTER and self.current_state == GameState.GAME_RUNNING):
            self.mel()
                

