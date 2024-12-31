import os
from typing import List, Optional
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from utils.window_preview import DevicePreview
from utils.constants import WindowSizes
from screens.login.login import LoginScreen
from utils.reload import start_hot_reload

class TeacherAttendanceApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hot_reload_observer = None
        
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        

        self.preview = DevicePreview()
        
        
        self.manager = ScreenManager()
        self.load_all_kv_files()
        self.load_screens()
        
      
        self.preview.add_widget(self.manager)
        
     
        directories_to_watch = ['app/screens', 'app/utils']
        self.hot_reload_observer = start_hot_reload(self, directories_to_watch)
        
        return self.preview

    def load_all_kv_files(self):
        for root, dirs, files in os.walk('app'):
            for file in files:
                if file.endswith('.kv'):
                    path = os.path.join(root, file)
                    Builder.load_file(path)
    
    def load_screens(self):
        self.manager.add_widget(LoginScreen(name="login"))
    
    def rebuild(self):
        self.root.clear_widgets()
        self.load_screens()
    
    def on_stop(self):
        if self.hot_reload_observer:
            self.hot_reload_observer.stop()
            self.hot_reload_observer.join()

if __name__ == "__main__":
    Window.size = WindowSizes.PHONE_PORTRAIT
    TeacherAttendanceApp().run()