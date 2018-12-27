# -*- coding: utf-8 -*-
"""
    Hangman Game
"""
import random

""" Game Class:
    The Game Class represents an active game
        Game takes a list of strings as its input
            it represents the available words used for games
        if NOT provided the beneath is used:
                imports list from words.txt
"""
class Game:
    try:
        f = open(".\words.txt", "r")
        default_list = f.read().split(" ")
    
    except:
        print("Couldn't find words.txt... exiting")
    
    else:
        f.close()
    
    #init
    def __init__(self, list_of_words=None):
        # set the word list as the user's input
        if type(list_of_words) != type(None):
            self.word_list = list_of_words
        # set the default list as the word list
        else:
            self.word_list = self.default_list
            
        self.new_game()
        #end init
        
    #start a new game
    def new_game(self):
        #reset the game state at start
        self.reset_game() 
        
        # ask the user if they want to start a game
        confirm = self.user.get_user_confirm("Would you like to play a game of hangman?")

        # if the user inputs "yes"        
        if confirm == "y" or confirm == "Y":
            # get a name for the user
            name = input("What should I call you?: ")
            self.user = Player(name)
            
            #It's a key of some sort...
            print("Ready {}".format(self.user.get_name()))

            # randomly generate a word
            self.set_word()
            
            # set flag that the game is running
            self.is_running = True
            
            # start the game loop
            self.start_game_loop()
            
        # else exit with splash
        else:
            print("No problems, I'll catch you next time.")
        #end new_game
    
    #reset the game
    def reset_game(self):
        # initial values
        self.invalid_try = 0
        self.max_try = 3
        self.current_word = {}
        self.guess_list = {}
        self.user = Player()
        self.is_running = False
        #end reset_game
    
    #set the word for the current game
    #   will randomly selects a word from the list of words
    #   if given a string input, it'll set that string as the word
    def set_word(self, word_to_guess=None):
        if type(word_to_guess) != type(None):
            # set the word to the input
            self.current_word = self.generate_word_map(word_to_guess)
        else:
            # randomly select a word from the list
            random_select = random.randint(0, len(self.word_list) - 1)
            self.current_word = self.generate_word_map(self.word_list[random_select])
        #end set_word
        
    #start the game loop
    def start_game_loop(self):
        # while the game is running
        while self.is_running == True:
            self.show_current_game()
            
            # get the current guess
            current_try = self.user.get_guess()
            
            #update user turn
            self.update_turn(current_try)
            
            #check for a win condition
            if self.check_win(self.current_word[1]) == True:
                #change the response based on a coin flip
                if self.coin_flip(1, 101):
                    print("Great job!!! You won!")
                else:
                    print("You did it! You're awesomesauce!")
                
                #set the is_running flag to False to break the game loop
                self.is_running = False
                
            #check for a lose condition
            elif self.invalid_try >= 3:
                print("Sorry, you ran out of tries, the word was {}".format(self.current_word[0]))
                self.is_running = False
            #end start_game_loop
            
    #update the next turn
    def update_turn(self, guess):
        #reference the dict
        found_list = self.current_word[1]
        
        #set up some defaults
        historic_count = 0
        no_match_found = False
        
        #check the guess is valid first
        try:
            if found_list[guess] == 0:
                for letter in self.current_word[0]:
                    #if the guess occurs in the word and the letter is not yet found
                    if letter == guess and found_list[letter] == 0:
                        #update the letter as being found
                        found_list[letter] = 1
                        
                        #update the history of how many was found
                        historic_count = 1
                        
                    #if the guess occurs in the word and the letter is already found
                    elif letter == guess and found_list[letter] == 1:
                        #increment the history count
                        historic_count += 1 
        
        #if the guess throws an except against our dict, we can assume no match found
        except:
            no_match_found = True
            
        #if we found matches, pretty print that to the user
        if historic_count > 0:
            #step 1: sprinkle the icing
            if historic_count > 1:
                print("You found {} letter \'{}\' s".format(historic_count, guess))
            else:
                print("You found 1 letter \'{}\'".format(guess))
        
        #if no matches were found at all
        elif historic_count == 0 and no_match_found == True:
            self.invalid_try += 1
            print("No match for that letter found. Try again!")
            
        #else, we already found that letter
        else:
            print("You already found that letter!")
        #end update_turn
    
    #flip a coin - fufufu
    def coin_flip(self, start, end):
        #create a number in a range
        coin = random.randint(start, end)
    
        #odds are true, evens are false
        if coin % 2 == 0:
            return False
        else:
            return True
        #end coin_flip
            
    #check for the win condition - all letters are found
    def check_win(self, found_map):
        #if the map contains no unfound elements
        if 0 in found_map.values():
            return False
        else:
            return True
        #end check_win
        
    #print the current game state        
    def show_current_game(self):
        found_list = self.current_word[1]
        state = ""
        for ch in self.current_word[0]:
            if found_list[ch] > 0:
                state += str(ch) + " "
            else:
                state += "_ "
        
        print("Letters guessed: {}".format(state))
        print("Tries left: {}".format(self.max_try - self.invalid_try))
        #end show_current_game
        
    #generate a word map
    #   a dict that contains each letter of the word
    #       which is linked to a 0 / 1 to represent if it was "not found" or "found"
    def generate_word_map(self, word):
        #This list is our return
        result = [word, {}]
        found_list = result[1]
        
        #for each char in the word
        for char in word:
            #if the char is not a key
            if char not in found_list.keys():
                #add it
                found_list[char] = 0
        return result
    
"""Player Class:
    A Player Class represents an active player in a game
        it handles interactions between the player and the game
    Player takes a string as its input to represent the player name
        if NOT provided the player is given the name "Player One"
"""
class Player:
    #init
    def __init__(self, name="Player One"):
        #if the name is an empty string set it to "Player One"
        if name == " " or name == "":
            name = "Player One"
            
        self.set_name(name)
        #end init
    
    #get the Player's name
    def get_name(self):
        return self.player_name
        #end get_name
    
    #set the Player's name    
    def set_name(self, name):
        self.player_name = name
        #end set_name
        
    #get single input confirmation from user (y/n)
    #can provide a string as a prompt to provide when asking for response
    def get_user_confirm(self, prompt=None):
        if type(prompt) != type(None):
            splash_text = prompt            
        else:
            splash_text = "Yes or No?"
            
        resp = self.clip_input_to_first_char(input("{} (y/n): ".format(splash_text)))                    
        return resp
        #end get_user_confirm
    
    #get the user's guess - user input will be clipped to first letter character
    def get_guess(self):
        #change the response based on a coin flip
        if self.coin_flip(1, 101):
            prompt = "Hey {}, what is your next guess?: "
        else:
            prompt = "What's the next letter there {}?: "
                    
        guess = self.clip_input_to_first_char(input(prompt.format(self.get_name())))
        return guess
        #end get_guess
       
    #clip the input from the user to its first character
    def clip_input_to_first_char(self, txt):
        if len(txt) > 1:
            return txt[0]
        else:
            return txt
        #end clip_input_to_first_char
    
    #flip a coin - fufufu
    def coin_flip(self, start, end):
        #create a number in a range
        coin = random.randint(start, end)
    
        #odds are true, evens are false
        if coin % 2 == 0:
            return False
        else:
            return True
        #end coin_flip
        
g = Game()

        