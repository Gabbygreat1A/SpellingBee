from kivymd.theming import ThemableBehavior
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivymd.uix.label import MDLabel


class AppDialog(ThemableBehavior, ModalView):
    pass

class CustomLabel(MDLabel):
    pass

class ResultDialog(AppDialog):
    level = StringProperty()
    total = StringProperty()
    correct = StringProperty()
    incorrect = StringProperty()
    corrections = DictProperty()
    main = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if len(self.corrections) == 0:
            self.ids.performance.add_widget(CustomLabel(text=f"There Are No Corrections"))
        else:
            for number, pair in enumerate(self.corrections.items(), 1):
                self.ids.performance.add_widget(CustomLabel(text=f"{number}.) [b]{pair[0]}[/b] But You Spelt [b]{pair[1]}[/b]"))

    def on_dismiss(self):
        self.main.changeScreen('levelScreen', self.main.root.ids.manager.children[0], 'right')
        self.main.resetData()