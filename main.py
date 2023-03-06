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
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import random, time
from kivy.clock import Clock


class CustomDropDown(DropDown):
    pass

class TimeEntryScreen(BoxLayout):        
    pass

class ClockScreen(BoxLayout):
    
    time_left = StringProperty()
    time_right = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.demo_time = ('2', '10')
        self.minutes = self.demo_time[0] if len(self.demo_time[0]) == 2 else '0' + self.demo_time[0]
        self.seconds = self.demo_time[1] if len(self.demo_time[1]) == 2 else '0' + self.demo_time[1]

        self.time_left = f'{self.minutes}:{self.seconds}'
        self.time_right = f'{self.minutes}:{self.seconds}'

        self.total_seconds_left = int(self.minutes) * 60 + int(self.seconds)
        self.total_seconds_right = int(self.minutes) * 60 + int(self.seconds)

        self.scheduled_left = False
        self.scheduled_right = False

        self.time_running = False

    def start_switch_time_left(self, widget):
        self.time_running = True

        # minutes, seconds = self.minutes, self.seconds
        # time_left = f'{minutes}:{seconds}'
        if self.scheduled_left:
            Clock.unschedule(self.countdown_left)
            self.scheduled_left = False

        if not self.scheduled_right:
            Clock.schedule_interval(self.countdown_right, 1)
            self.scheduled_right = True


    def countdown_left(self, dt):

        if self.total_seconds_left > 0 and self.time_running:
            print('time running', self.ids.time_left.text)
            self.total_seconds_left -= 1

            minutes, seconds = divmod(self.total_seconds_left, 60)

            self.time_left = f'{minutes}:{seconds}'

        else:
            Clock.unschedule(self.countdown_left)
            self.scheduled_left = False


    def start_switch_time_right(self, widget):
        self.time_running = True

        # minutes, seconds = self.minutes, self.seconds
        # time_left = f'{minutes}:{seconds}'\
        if self.scheduled_right:
            Clock.unschedule(self.countdown_right)
            self.scheduled_right = False

        if not self.scheduled_left:
            Clock.schedule_interval(self.countdown_left, 1)
            self.scheduled_left = True
    
    def countdown_right(self, dt):

        if self.total_seconds_right > 0 and self.time_running:
            print('time running', self.ids.time_right.text)
            self.total_seconds_right -= 1

            minutes, seconds = divmod(self.total_seconds_right, 60)

            self.time_right = f'{minutes}:{seconds}'

        else:
            Clock.unschedule(self.countdown_right)
            self.scheduled_right = False




    def stop_resume(self, widget): 
        if self.time_running: 
            widget.background_normal = './icons/play_icon.png'
            widget.background_down = './icons/play_icon_down.png'
            #stop_right
            # Clock.unschedule(self.countdown_right)
            # self.scheduled_right = False

            #stop left
            # Clock.unschedule(self.countdown_left)
            # self.scheduled_left = False
            
            self.time_running = False
        
        else:
            widget.background_normal = './icons/pause_icon.png'
            widget.background_down = './icons/pause_icon_down.png'
            self.time_running = True
    

class ChessClockApp(App):
    pass


dropdown = CustomDropDown()
mainbutton = Button(text = 'Select Time', font_name = 'fonts/Lcd.ttf', size_hint = (0.2, 0.2), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
mainbutton.bind(on_release = dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))


ChessClockApp().run()
