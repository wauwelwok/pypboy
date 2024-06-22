
from pypboy import BaseModule
from pypboy.modules.inv import attachment
from pypboy.modules.inv import apparel
from pypboy.modules.inv import aid

import settings

class Module(BaseModule):


    def __init__(self, *args, **kwargs):
        self.submodules = [
            attachment.Module(self),
            apparel.Module(self),
            aid.Module(self)
        ]
        super(Module, self).__init__(*args, **kwargs)

    def handle_resume(self):
        settings.hide_top_menu = False
        settings.hide_submenu = False
        settings.hide_main_menu = False
        settings.hide_footer = False
        settings.hide_upper_footer = False
        # self.active.handle_action("resume")