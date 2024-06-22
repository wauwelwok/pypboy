import pypboy
import settings


class Module(pypboy.SubModule):

    label = "AID"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.label = "AID"
        self.images = []

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "INV"
        self.topmenu.title = settings.MODULE_TEXT

        # self.footer = pypboy.ui.Footer(settings.STATUS_FOOTER)
        self.footer = pypboy.ui.Footer(["PB-NORMAL", "ITEMS ATTACHED", "INVENTORY"])
        self.add(self.footer)

        self.upperfooter = pypboy.ui.UpperFooter(["MODE", "FAV", "SORT"])
        self.add(self.upperfooter)