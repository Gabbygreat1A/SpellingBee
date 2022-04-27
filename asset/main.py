from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

kv = '''
MDBoxLayout:
	MDRaisedButton:
		text: 'Correct'
		on_press: app.playCorrect()
	MDRaisedButton:
		text: 'Incorrect'
		on_press: app.playInCorrect()
'''

class Test(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.correctSound = SoundLoader.load('correct.mp3')
		self.incorrectSound = SoundLoader.load('incorrect.mp3')
		
	def playCorrect(self):
		self.correctSound.play()
	
	def playInCorrect(self):
		self.incorrectSound.play()
		
	def build(self):
		return Builder.load_string(kv)
		
Test().run()