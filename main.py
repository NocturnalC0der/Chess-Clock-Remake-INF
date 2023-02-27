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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.demo_time = ('2', '30')
        self.minutes = self.demo_time[0] if len(self.demo_time[0]) == 2 else '0' + self.demo_time[0]
        self.seconds = self.demo_time[1] if len(self.demo_time[1]) == 2 else '0' + self.demo_time[1]

        self.time = self.minutes + ':' + self.seconds

        self.time_running = False

    def start_switch_time_left(self, widget):
        self.time_running = True
        total_seconds = int(self.minutes) * 60 + int(self.seconds)

        while total_seconds > 0 and self.time_running:
            total_seconds -= 1

            minutes, seconds = divmod(total_seconds, 60)

            widget.text = f'{minutes:02d}:{seconds:02d}'

            time.sleep(1)


    def start_switch_time_right(self, widget):
        self.time_running = True
        total_seconds = int(self.minutes) * 60 + int(self.seconds)

        while total_seconds > 0 and self.time_running:
            total_seconds -= 1

            minutes, seconds = divmod(total_seconds, 60)

            widget.text = f'{minutes:02d}:{seconds:02d}'

            time.sleep(1)




    def stop_resume(self, widget): 
        if self.time_running: 
            widget.background_normal = './icons/play_icon.png'
            widget.background_down = './icons/play_icon_down.png'
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
