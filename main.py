from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import random, time
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore


class TimeEntryScreen(BoxLayout, Screen): 

    # dropdown = CustomDropDown()
    # mainbutton = Button(text = 'Select Time', font_name = 'fonts/Lcd.ttf', size_hint = (0.2, 0.2), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
    # mainbutton.bind(on_release = dropdown.open)
    # dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
    
    # Screen.manager.transition.direction = 'left'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time_left = ''
        self.time_right = ''

        self.minutes_right = 0
        self.minutes_left = 0
        self.seconds_right = 0
        self.seconds_left = 0

        self.original_total_seconds_left = 0
        self.original_total_seconds_right = 0

        self.selected_left = ''
        self.selected_right = ''
        
        self.btn_list_left = []
        self.btn_list_right = []

        self.storage = JsonStore('storage.json')
        self.storage.put('Time left', time_left=self.time_left, total_seconds_left=self.original_total_seconds_left)
        self.storage.put('Time right', time_right=self.time_right, total_seconds_right=self.original_total_seconds_right)

        # self.storage.get('Time right')['total_seconds_right'] == None
        # self.storage.get('Time right')['total_seconds_right'] == None

    
    def pick_left(self, clicked_btn, btn2, btn3, btn4):
        
        not_clicked = [btn2, btn3, btn4]

        for i in not_clicked:
            if i.disabled == True:
                i.disabled = False

        clicked_btn.disabled = True
        time_str = clicked_btn.text        
        self.selected_left = clicked_btn

        not_clicked.insert(0, clicked_btn)

        self.btn_list_left = not_clicked
        
        self.minutes_left = int(time_str[0:2])
        self.seconds_left = int(time_str[3:])

        self.original_total_seconds_left = (self.minutes_left * 60) + self.seconds_left
        total_seconds_left = (self.minutes_left * 60) + self.seconds_left

        minutes, seconds = divmod(total_seconds_left, 60)

        self.time_left = f'{minutes:02}:{seconds:02}'
        
        
        # print(minutes, seconds, self.time_left)
        # print(not_clicked == self.btn_list_left)

        return (self.time_left, self.original_total_seconds_left)


    def pick_right(self, clicked_btn, btn2, btn3, btn4):

        not_clicked = [btn2, btn3, btn4]

        for i in not_clicked:
            if i.disabled == True:
                i.disabled = False

        clicked_btn.disabled = True

        time_str = clicked_btn.text
        self.selected_right = clicked_btn
     
        not_clicked.insert(0, clicked_btn)

        self.btn_list_right = not_clicked

        self.minutes_right = int(time_str[0:2])
        self.seconds_right = int(time_str[3:])

        self.original_total_seconds_right = (self.minutes_right * 60) + self.seconds_right
        total_seconds_right = (self.minutes_right * 60) + self.seconds_right

        minutes, seconds = divmod(total_seconds_right, 60)

        self.time_right = f'{minutes:02}:{seconds:02}'


        # print(minutes, seconds, self.time_left)
        # print(not_clicked == self.btn_list_right)

        return (self.time_right, self.original_total_seconds_right)


    def pressed_play(self):
        print(self.time_left, self.original_total_seconds_left)
        print(self.time_right, self.original_total_seconds_right)

        # self.storage.put('Time left')['time_left'] = self.time_left
        # self.storage.put('Time left')['total_seconds_left'] = self.original_total_seconds_left

        self.storage.put('Time left', time_left=self.time_left, total_seconds_left=self.original_total_seconds_left)
        self.storage.put('Time right', time_right=self.time_right, total_seconds_right=self.original_total_seconds_right)

        print(self.storage.get('Time left'))
        print(self.storage.get('Time right'))

class ClockScreen(BoxLayout, Screen):
    
    time_left = StringProperty()
    time_right = StringProperty()
    stop_resume_text = StringProperty()
    paused = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.manager.transition.direction = 'right'

        self.TimeEntryClass = TimeEntryScreen()

        # self.selected_left = self.TimeEntryClass.selected_left.text
        # self.selected_right = self.TimeEntryClass.selected_right.text
        self.storage = JsonStore('storage.json')
        

        #TIME LEFT MAKING
        # self.text_minutes_left = int(self.selected_left[0:2])
        # self.text_seconds_left = int(self.selected_left[3:])

        # self.original_total_seconds_left = (self.minutes_left * 60) + self.seconds_left
        # self.total_seconds_left = (self.text_minutes_left * 60) + self.text_seconds_left

        # self.minutes_left, self.seconds_left = divmod(self.total_seconds_left, 60)

        # self.time_left = f'{self.minutes:02}:{self.seconds:02}'
        # self.time_left = '10:23'
        self.time_left = self.storage.get('Time left')['time_left']
        self.time_right = self.storage.get('Time right')['time_right']

        self.original_time_right = self.time_left
        self.original_time_left = self.time_right

        self.total_seconds_left = self.storage.get('Time left')['total_seconds_left']
        self.total_seconds_right = self.storage.get('Time right')['total_seconds_right']

        #--------------------------------------------------------------------------------------#
                
        #TIME RIGHT MAKING:
        # self.text_minutes_right = int(self.selected_right[0:2])
        # self.text_seconds_right = int(self.selected_right[3:])

        # self.original_total_seconds_right = (self.minutes_right * 60) + self.seconds_right
        # self.total_seconds_right = (self.text_minutes_right * 60) + self.text_seconds_right

        # self.minutes, self.seconds = divmod(self.total_seconds_right, 60)

        # self.time_right = f'{self.minutes:02}:{self.seconds:02}'
        # self.time_right = '10:23'
        # self.original_time_right = self.time_right

        #--------------------------------------------------------------------------------------#

        #OTHER VARIABLES#

        self.scheduled_left = False
        self.scheduled_right = False
        self.was_running = None

        self.time_running = False
        self.running_right = False
        self.running_left = False
        self.paused = False



        self.stop_resume_text = 'STOP'


    def start_switch_time_left(self, widget):

        if not self.paused:
            self.time_running = True
            if self.scheduled_left:
                Clock.unschedule(self.count_left)
                self.scheduled_left = False
                print('unscheduling left')

            if not self.scheduled_right:
                self.count_right = Clock.schedule_interval(self.countdown_right, 1)
                self.scheduled_right = True
                print('scheduling right')
        


    def countdown_left(self, dt):
        if self.total_seconds_left > 0:
            print('time running', self.ids.time_left.text)
            
            self.total_seconds_left -= 1
            minutes, seconds = divmod(self.total_seconds_left, 60)

            self.time_left = f'{minutes:02}:{seconds:02}'

        else:
            Clock.unschedule(self.countdown_left)
            self.scheduled_left = False


    def start_switch_time_right(self, widget):

        if not self.paused:
            self.time_running = True
            if self.scheduled_right:
                Clock.unschedule(self.countdown_right)
                self.scheduled_right = False
                print('unscheduling right')

            if not self.scheduled_left:
                self.count_left = Clock.schedule_interval(self.countdown_left, 1)
                self.scheduled_left = True
                print('scheduling left')

    
    def countdown_right(self, dt):
        if self.total_seconds_right > 0 and self.time_running:
            print('time running', self.ids.time_right.text)
                
     
            self.total_seconds_right -= 1

            minutes, seconds = divmod(self.total_seconds_right, 60)

        
            self.time_right = f'{minutes:02}:{seconds:02}'

        else:
            Clock.unschedule(self.countdown_right)
            self.scheduled_right = False




    def stop_resume(self, widget): 
        self.was_running = self.count_left if self.scheduled_left == True else self.count_right
        if self.time_running: 
            
            # widget.background_normal = './icons/play_icon.png'
            # widget.background_down = './icons/play_icon_down.png'
            #stop_right
            # Clock.unschedule(self.countdown_right)
            # self.scheduled_right = False

            #stop left
            # Clock.unschedule(self.countdown_left)
            # self.scheduled_left = False
            self.time_running = False
            self.paused = True
            
            Clock.unschedule(self.was_running)
            # Clock.unschedule(self.count_right)

            self.stop_resume_text = 'RESUME'
            print('stopping',f'self.was_running: {self.was_running}' ,f'Time_running: {self.time_running}', f'Self.paused: {self.paused}')

        else:
            # widget.background_normal = './icons/pause_icon.png'
            # widget.background_down = './icons/pause_icon_down.png'
            # print('starting', f'Time_running: {self.time_running}', f'Self.paused: {self.paused}')

            self.was_running()

            self.time_running = True
            self.paused = False
            self.stop_resume_text = 'STOP'

            print('resuming',f'self.was_running: {self.was_running}' ,f'Time_running: {self.time_running}', f'Self.paused: {self.paused}')
    
    def reset(self, widget):

        # if self.paused:
        # self.time_left = self.original_time_left
        # self.time_right = self.original_time_right
        # self.total_seconds_left = self.original_total_seconds_left
        # self.total_seconds_right = self.original_total_seconds_right
        # self.was_running = None
        # self.paused = False
        # self.stop_resume_text = 'STOP'
        # print(self.TimeEntryClass.time_right, type(self.TimeEntryClass.time_right), list(self.TimeEntryClass.time_right))
        print(self.storage.get('Time left'))
        print(self.storage.get('Time right'))


class WindowManager(ScreenManager):
    pass

class ChessClockApp(App):
    pass


ChessClockApp().run()
