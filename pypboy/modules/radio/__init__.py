
from pypboy import BaseModule
from pypboy.modules.radio import radio


import settings

class Module(BaseModule):


    def __init__(self, *args, **kwargs):
        self.submodules = [
            radio.Module(self),
        ]
        super(Module, self).__init__(*args, **kwargs)

    def handle_resume(self):
        settings.hide_top_menu = False
        settings.hide_submenu = True
        settings.hide_main_menu = False
        settings.hide_footer = False
        settings.hide_upper_footer = True