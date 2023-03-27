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

class CustomDropDown(DropDown):
    pass

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

        self.original_total_seconds_left = 0
        self.original_total_seconds_right = 0

        self.time_button_ids = [self.ids.one_minutes_left, self.ids.three_minutes_left,
                           self.ids.five_minutes_left, self.ids.ten_minutes_left]

        self.selected_left = 0
        self.selected_right = 0

    
    def pick_left(self, widget):
        
        # for i in self.time_button_ids:
        #     if i == widget:
        self.selected_left = self.time_button_ids[self.time_button_ids.index(widget)]

        for i in self.time_button_ids:
            if i.disabled == True:
                i.disabled == False

        widget.disabled = True

        time_str = widget.text

        minutes_left = int(time_str[0:2])
        seconds_left = int(time_str[3:])

        #One way:
        # time_left = f'{self.minutes_left:02}:{self.seconds_left:02}'

        #Another way:
        original_total_seconds_left = (minutes_left * 60) + seconds_left
        total_seconds_left = (minutes_left * 60) + seconds_left

        minutes, seconds = divmod(total_seconds_left, 60)

        time_left = f'{minutes:02}:{seconds:02}'
        
        self.original_total_seconds_left = original_total_seconds_left
        self.time_left = time_left
        
        print(minutes, seconds, time_left)

        # return (time_left, original_total_seconds_left)


    def pick_right(self, widget):

        time_str = widget.text

        minutes_right = int(time_str[0:2])
        seconds_right = int(time_str[3:])

        #One way:
        # time_right = f'{self.minutes_right:02}:{self.seconds_right:02}'

        #Another way:
        original_total_seconds_right = (minutes_right * 60) + seconds_right
        total_seconds_right = (minutes_right * 60) + seconds_right

        minutes, seconds = divmod(total_seconds_right, 60)

        time_right = f'{minutes:02}:{seconds:02}'

        self.original_total_seconds_right = original_total_seconds_right
        self.time_right = time_right

        print(minutes, seconds, time_right)

        # return (time_right, original_total_seconds_right)


class ClockScreen(BoxLayout, Screen):
    
    time_left = StringProperty()
    time_right = StringProperty()
    stop_resume_text = StringProperty()
    paused = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.manager.transition.direction = 'right'

        self.TimeEntryClass = TimeEntryScreen()

        self.time_left = self.TimeEntryClass.time_left
        self.time_right = self.TimeEntryClass.time_right

        self.original_total_seconds_left = self.TimeEntryClass.original_total_seconds_left
        self.original_total_seconds_right = self.TimeEntryClass.original_total_seconds_right

        self.total_seconds_left = self.original_total_seconds_left
        self.total_seconds_right = self.original_total_seconds_right

        self.original_time_left = self.time_left
        self.original_time_right = self.time_right
        
        # self.demo_time = ('2', '10')
        # self.minutes = self.demo_time[0] if len(self.demo_time[0]) == 2 else '0' + self.demo_time[0]
        # self.seconds = self.demo_time[1] if len(self.demo_time[1]) == 2 else '0' + self.demo_time[1]

        # self.original_time_left = f'{self.minutes}:{self.seconds}'
        # self.original_time_right = f'{self.minutes}:{self.seconds}'

        # self.time_left = f'{self.minutes}:{self.seconds}'
        # self.time_right = f'{self.minutes}:{self.seconds}'

        # self.original_total_seconds_left = int(self.minutes) * 60 + int(self.seconds)
        # self.original_total_seconds_right = int(self.minutes) * 60 + int(self.seconds)

        # self.total_seconds_left = int(self.minutes) * 60 + int(self.seconds)
        # self.total_seconds_right = int(self.minutes) * 60 + int(self.seconds)

        self.scheduled_left = False
        self.scheduled_right = False
        self.was_running = None

        self.time_running = False
        self.running_right = False
        self.running_left = False
        self.paused = False



        self.stop_resume_text = 'STOP'


    def start_switch_time_left(self, widget):
        # minutes, seconds = self.minutes, self.seconds
        # time_left = f'{minutes}:{seconds}'
        # print('Left btn before', f'Time_running: {self.time_running}, Self.paused: {self.paused}')

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
        # minutes, seconds = self.minutes, self.seconds
        # time_left = f'{minutes}:{seconds}'\
        # print('Right btn before', f'Time_running: {self.time_running}, Self.paused: {self.paused}')
        

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
        self.time_left = self.original_time_left
        self.time_right = self.original_time_right
        self.total_seconds_left = self.original_total_seconds_left
        self.total_seconds_right = self.original_total_seconds_right
        self.was_running = None
        self.paused = False
        self.stop_resume_text = 'STOP'


class WindowManager(ScreenManager):

    pass

class ChessClockApp(App):
    pass


ChessClockApp().run()
