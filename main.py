from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import random
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

#Disk Widget Class
class Disk(Widget):
    pass

#Bat Widget Class
class Bat(Widget):
    pass

#Border Widget Class for upper and lower border
class Border(Widget):
    pass

#MenuScreen with 3 Buttons (Functionality is given in the MainApp Class)
class MenuScreen(Screen):
    menu_screen_sound = SoundLoader.load("music/L's theme (Deathnote) (MenuScreen).mp3")
    menu_screen_sound.volume = 0.5
    def on_pre_enter(self):
        self.menu_screen_sound.play()
    def on_pre_leave(self):
        self.menu_screen_sound.stop()

#Screen and its controls for Play with Computer
class GameScreenComputer(Screen):
    pass

#Screen and its controls for Play with Player
class GameScreenPlayer(Screen):

    randnum = random.uniform(0.45, 0.55) #Proper use of this is not functional yet. Its meant to randomly choosing a side to start the game.
    original_x = 0
    original_y = 0
    ball_speed_x = 0.007
    ball_speed_y = 0.007
    main_game_event = None
    timer_event = None
    scorePlayer1 = 0
    scorePlayer2 = 0

    tap = SoundLoader.load("music/tap.mp3")

    def on_enter(self):
        Window.bind(on_key_down=self._keydown)

    def reset(self): #Reset the disk position to default after a point is scored by any player
        disk = self.ids['disk']
        disk.pos_hint = {"x": 0.5, "top": 0.5}
        self.ball_speed_x = 0.007
        self.ball_speed_y = 0.007


    def serve(self): #Starts the game (Called when the START Button is clicked)
        backbtn = self.ids['backbtn'] #Hides the Menu Button
        backbtn.disabled = True
        backbtn.visible = False
        backbtn.opacity = 0
        pause = self.ids['pause']
        pause.disabled = False
        startbtn = self.ids['startbtn'] # Hides the START Button
        startbtn.visible = False
        startbtn.opacity = 0
        startbtn.disabled = True
        disk = self.ids['disk']
        disk.pos_hint = {"x": self.randnum, "top": self.randnum}
        self.original_x = disk.pos_hint["x"]
        self.original_y = disk.pos_hint["top"]
        if (disk.pos_hint['x'] < 1):
            self.main_game_event = Clock.schedule_interval(self.callback, 1.0/120.0) #Kivy Clock function to call a function repeatedly, calls the callback() function described below
            self.timer_event = Clock.schedule_interval(self.timer, 1) #Calls the timer() function described below

    def callback(self, dt):  #Gets called 120 times in 1 second giving 120 FPS, if the disk is on the screen
        disk = self.ids['disk']
        x = disk.pos_hint['x']
        y = disk.pos_hint['top']
        bat_left = self.ids['player_left_bat']
        bat_right = self.ids['player_right_bat']
        if (disk.collide_widget(bat_left) or (disk.collide_widget(bat_right))): #To check if the disk is collided with the bats(both left and right)
            self.ball_speed_x *= -1
            self.tap.play()
        if (y >= 0.95) or (y <= 0.07):
            self.ball_speed_y *= -1
        disk.pos_hint = {"x": x + self.ball_speed_x, "top": y + self.ball_speed_y}
        # Score for left Player
        if(disk.pos_hint['x'] >= 1):
            score_left = self.ids['player_left_score']
            score_left.text = str(int(score_left.text) + 1)
            self.scorePlayer1 = int(score_left.text)
            self.reset()
        # Score for right Player
        if(disk.pos_hint['x'] <= 0):
            score_right = self.ids['player_right_score']
            score_right.text = str(int(score_right.text) + 1)
            self.scorePlayer2 = int(score_right.text)
            self.reset()
    
    def on_touch_move(self, touch): # Kivy Function to for touch operation
        bat_left = self.ids['player_left_bat']
        bat_right = self.ids['player_right_bat']
        widl, lengl = bat_left.size_hint
        widr, lengr = bat_right.size_hint
        # left players(player 1)
        if (touch.x < self.width/3) and (touch.y/self.height <= 0.975 - (lengl/2) and (touch.y/self.height >= 0.025 + (lengl/2))): #0.975 is the top border and 0.025 is the bottom border
            if (bat_left.pos_hint["y"] <= 0.97 - lengl + 0.005) and (bat_left.pos_hint["y"] >= 0.02 + 0.005): #0.005 is just the correction term
                bat_left.pos_hint = {"y": (touch.y/self.height)-lengl/2, "x": 0}
            elif (bat_left.pos_hint["y"] > 0.97 - lengl + 0.005):
                bat_left.pos_hint = {"y": 0.97-lengl+ 0.005, "x": 0}
            else:
                bat_left.pos_hint = {"y" : 0.02+0.005, "x": 0}
        
        # right player(player 2)
        if (touch.x > self.width - (self.width/3)) and (touch.y/self.height <= 0.975 - (lengr/2) and (touch.y/self.height >= 0.025 + (lengr/2))):
            if (bat_right.pos_hint["y"] <= 0.97 - lengr + 0.005) and (bat_right.pos_hint["y"] >= 0.02 + 0.005): #0.005 is just the correction term
                bat_right.pos_hint = {"y": (touch.y/self.height)-lengr/2, "x": 0.98}
            elif (bat_right.pos_hint["y"] > 0.97 - lengr + 0.005):
                bat_right.pos_hint = {"y": 0.97-lengr+ 0.005, "x": 0.98}
            else:
                bat_right.pos_hint = {"y" : 0.02+0.005, "x": 0}

    def timer(self, dt): #The Timer on the Screen, gets called every second
        timer = self.ids['timer']
        time = int(timer.text)
        time -= 1
        timer.text = str(time)
        if (time%10 == 0) and (time != 180): #Increases the speed of the ball in every 10 seconds
            if (self.ball_speed_x > 0):
                self.ball_speed_x += 0.001
            if(self.ball_speed_y > 0):
                self.ball_speed_y += 0.001
            if (self.ball_speed_x < 0):
                self.ball_speed_x -= 0.001
            if (self.ball_speed_y < 0):
                self.ball_speed_y -= 0.001
        bat_left = self.ids['player_left_bat']
        bat_right = self.ids['player_right_bat']
        wedl, lengl = bat_left.size_hint
        wedr, lengr = bat_left.size_hint
        if (time%20 == 0) and (time != 180) and (lengl >= 0.2):
            lengl -= 0.05
            bat_left.size_hint = wedl, lengl
            lengr -= 0.05
            bat_right.size_hint = wedr, lengr

        if (timer.text == "0"):
            self.timer_event.cancel() #Cancels the timer clock event
            self.main_game_event.cancel() #Cancels the main game clock event
            self.showWinner() #Calling a function showWinner() to present the winner's name in the screen
    
    def showWinner(self):
        winner_label = self.ids['winner_label']
        winner_label.visible = True
        winner_label.opacity = 1
        winner_label.disabled = False
        if(int(self.scorePlayer1) > int(self.scorePlayer2)):
            winner_label.text = "Player 1 Wins"
        else:
            winner_label.text = "Player 2 Wins"

    def pause(self): #Pause Functionality of the game
        self.main_game_event.cancel()
        self.timer_event.cancel()
        pause = self.ids['pause']
        pause.disabled = True
        resume = self.ids['resume']
        resume.disabled = False
        backbtn = self.ids['backbtn']
        backbtn.disabled = False
        backbtn.opacity = 1
        backbtn.visible = True 

    def resume(self): #Resume Functionality of game
        self.main_game_event = Clock.schedule_interval(self.callback, 1.0/120.0)
        self.timer_event = Clock.schedule_interval(self.timer, 1)
        resume = self.ids['resume']
        resume.disabled = True
        pause = self.ids['pause']
        pause.disabled = False
        backbtn = self.ids['backbtn']
        backbtn.disabled = True
        backbtn.opacity = 0
        backbtn.visible = False

    def _keydown(self, garbage, garbage2, not_garbage, symbol, garbage4):
        bat_left = self.ids['player_left_bat']
        widl, lengl = bat_left.size_hint
        bat_right = self.ids['player_right_bat']
        widr, lengr = bat_left.size_hint
        left_y = bat_left.pos_hint['y']
        right_y = bat_right.pos_hint['y']
        print(left_y)
        if (symbol == "w" and left_y + lengl < 0.97):
            bat_left.pos_hint = {"x": 0, "y": left_y + 0.04}
        if (symbol == "s" and left_y > 0.04):
            bat_left.pos_hint = {"x": 0, "y": left_y - 0.04}
        if (not_garbage == 82 and right_y + lengr < 0.97):
            bat_right.pos_hint = {"x": 0.98, "y": right_y + 0.04}
        if (not_garbage == 81 and right_y > 0.04):
            bat_right.pos_hint = {"x": 0.98, "y": right_y - 0.04}
        if (symbol == 'p'):
            self.pause()
        if (symbol == 'r'):
            self.resume()


#Loads main.kv using the Builder in Kivy Library
GUI = Builder.load_file("main.kv")

#App Class
class MainApp(App):
    def build(self):
        return GUI

    def changescreen(self, screen_name): #change screen button
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
        if (screen_manager.current == "menu_screen"):
            screen_manager.transition.direction = "right"
        if (screen_manager.current != "menu_screen"):
            screen_manager.transition.direction = "left"

#Function to run the App
MainApp().run()