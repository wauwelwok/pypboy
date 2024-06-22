
from pypboy import BaseModule
from pypboy.modules.stats import status
from pypboy.modules.stats import connect
from pypboy.modules.stats import diagnostics

import settings

class Module(BaseModule):


    def __init__(self, *args, **kwargs):
        self.submodules = [
            status.Module(self),
            connect.Module(self),
            diagnostics.Module(self)
        ]
        super(Module, self).__init__(*args, **kwargs)

    def handle_resume(self):
        settings.hide_top_menu = False
        settings.hide_submenu = False
        settings.hide_main_menu = False
        settings.hide_footer = False
        settings.hide_upper_footer = False
        # self.active.handle_action("resume")