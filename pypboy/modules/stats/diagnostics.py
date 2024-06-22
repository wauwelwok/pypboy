import pypboy
import settings


class Module(pypboy.SubModule):

    label = "DIAGNOSTICS"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.label = "DIAGNOSTICS"
        self.images = []

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "STAT"
        self.topmenu.title = settings.MODULE_TEXT

        # self.footer = pypboy.ui.Footer(settings.STATUS_FOOTER)
        self.footer = pypboy.ui.Footer(["NOTIFICATIONS", "POWER", "CUSTOM"])
        self.add(self.footer)

        self.upperfooter = pypboy.ui.UpperFooter(["RADIATION", "CONNECT >"])
        self.add(self.upperfooter)