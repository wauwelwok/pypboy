import pypboy
import settings


class Module(pypboy.SubModule):

    label = "CONNECT"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.label = "CONNECT"
 
        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "STAT"
        self.topmenu.title = settings.MODULE_TEXT

        self.footer = pypboy.ui.Footer(["NOTIFICATIONS", "POWER", "CUSTOM"])
        self.add(self.footer)

        self.upperfooter = pypboy.ui.UpperFooter(["RADIATION", "CONNECT >"])
        self.add(self.upperfooter)