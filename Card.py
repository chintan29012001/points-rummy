import arcade
import math

class card(arcade.Sprite):
    """ card class """

    def __init__(self,no,suit,GAME_CONFIG,meld=0,comp=0):
        """ Initialize knife """
        """x- shown deck x coordinate y-shown deck y coordinate"""
        self.SCREEN_WIDTH = GAME_CONFIG["general_settings"]["screen_width"]
        self.SCREEN_HEIGHT = GAME_CONFIG["general_settings"]["screen_height"]
        self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["sprite_scaling"]
        # self.SPRITE_POSITION=[x,y]
        if(meld==1):
            self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["meld_sprite_scaling"]

        self.no=no
        if(no=='A'):
            self.num=1
        elif(no=='J'):
            self.num=11
        elif(no=='Q'):
            self.num=12
        elif(no=='K'):
            self.num=13
        else:
            self.num=int(no)
        self.suit=suit
        self.card_image = GAME_CONFIG["assets_path"]["images"]["card"]["card"+str(no)+str(suit)]
        if(comp==1):
            self.card_image = GAME_CONFIG["assets_path"]["images"]["card"]["card"+"1R"]

        self.card_drawn = GAME_CONFIG["assets_path"]["sounds"]["card_drawn"]
        self.card_discarded = GAME_CONFIG["assets_path"]["sounds"]["card_discarded"]
        super().__init__(self.card_image, self.SPRITE_SCALING/2)

    def shown_deck_discard(self):
        """ 
        Initialize the "stuck in target" state 
        Copy the target's rotation speed and set the rotation radius and center
        """
        self.center_y = self.shown_deck_y
        self.center_x = self.shown_deck_x
        arcade.play_sound(self.card_discarded)
        
    
    def shown_deck_draw(self,x,y):
        """x,y - coordinates of card to be place in my deck""" 
        self.center_y = y
        self.center_x = x
        arcade.play_sound(self.card_drawn)

    def move(self,startx,starty,x,y,lastx,lasty):
        if(startx<=x<=lastx):
            self.center_x = x
        if(starty<=y<=lasty): 
            self.center_y = y


    def setup(self):
        self.card_drawn = arcade.load_sound(self.card_drawn)
        self.card_drawn = arcade.load_sound(self.card_discarded)

    

