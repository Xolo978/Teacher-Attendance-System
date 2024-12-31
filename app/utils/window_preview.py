from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivy.core.window import Window
from .constants import WindowSizes, WINDOW_COLORS
from kivy.utils import get_color_from_hex

class DevicePreview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.setup_toolbar()
        Window.clearcolor = get_color_from_hex(WINDOW_COLORS["background"])
        Window.minimum_width = 300
        Window.minimum_height = 500
        
    def setup_toolbar(self):
        self.toolbar = MDTopAppBar(
            title="Device Preview",
            md_bg_color=get_color_from_hex(WINDOW_COLORS["toolbar"]),
            right_action_items=[
                ["cellphone", lambda x: self.set_size(WindowSizes.PHONE_PORTRAIT)],
                ["tablet", lambda x: self.set_size(WindowSizes.TABLET_PORTRAIT)],
                ["rotate-3d", lambda x: self.toggle_orientation()]
            ]
        )
        self.add_widget(self.toolbar)

    def set_size(self, size):
        Window.size = size
        
    def toggle_orientation(self):
        width, height = Window.size
        Window.size = (height, width)