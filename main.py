import pyttsx3
from random import randint, shuffle, sample
import os
import threading
from time import sleep
from kivymd.toast import toast

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from libs.baseclass import Question
from libs.baseclass.AppDialog import ResultDialog
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.core.audio import SoundLoader


os.environ['RootFolder'] = os.path.dirname(__file__)
os.environ['AssetFolder'] = os.path.join(os.environ['RootFolder'], f'asset{os.sep}')
os.environ['PythonFolder'] = os.path.join(os.environ['RootFolder'], 'libs', f'baseclass{os.sep}')
os.environ['KvFolder'] = os.path.join(os.environ['RootFolder'], 'libs', f'kv{os.sep}')

kv = '''
#: import os os
#: import Window kivy.core.window.Window
ScreenManager:
	Screen:
		MDFloatLayout:
			md_bg_color: 1,1,1,1
			Image:
				source: f"{os.environ['AssetFolder']}logo.png"
            MDSpinner:
                size_hint: .1, .1
                pos_hint: {'center_x': .5}
	Screen:
		id: manager
		name: 'manager'
'''

class PassySpellingApp(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.questionNumber = 1
		self.correct = 0
		self.incorrect = 0
		self.position = 0
		self.quest = None
		self.repeat = True
		self.wrongDb = {}

	def resetData(self):
		self.questionNumber = 1
		self.correct = 0
		self.incorrect = 0
		self.position = 0
		self.quest = None
		self.repeat = True
		self.wrongDb = {}
		self.number = []
		self.questionList = []

		self.root.ids.manager.children[0].ids.question.ids.incorrect.text = f'Incorrect: [b]{self.incorrect}[/b]'
		self.root.ids.manager.children[0].ids.question.ids.total.text = 'Begin SPELLINGBee'
		self.root.ids.manager.children[0].ids.question.ids.correct.text = f'Correct: [b]{self.correct}[/b]'

	def build(self):
		Window.bind(on_keyboard=self.events)
		return Builder.load_string(kv)

	def events(self, window, key, *args):
		if key == 27:
			if self.root.ids.manager.children[0].current == 'questionScreen':
				self.changeScreen('levelScreen', self.root.ids.manager.children[0], 'right')
		return True

	def on_start(self):
		self.number = []
		self.questionList = ('photosynthesis', 'Complementary', 'Verification')
		self.runThread = threading.Thread(target=self.initialiseApp)
		self.runThread.start()

	def chooseNumber(self, length):
		self.correctSound = SoundLoader.load(f"{os.environ['AssetFolder']}correct.mp3")
		self.incorrectSound = SoundLoader.load(f"{os.environ['AssetFolder']}incorrect.mp3")
		while True:
			number = randint(0, 50)
			if len(self.number) == length:
				break
			else:
				if number in self.number:
					continue
				else:
					self.number.append(number)

	def openText(self, level):
		file = open(f"{os.environ['AssetFolder']}{level}.txt", 'r')
		for words in file.readlines():
			if int(words.strip().split('.')[0]) in self.number:
				self.questionList.append(words.strip().split('.')[1])
		file.close()
		if len(self.questionList) != len(self.number):
			self.questionList.append(sample(['Massive', 'Endure', 'Conclude', 'Verify'], k=1)[0])
		shuffle(self.questionList)

	def difficulty(self, level):
		self.questionList = []
		self.level = level
		load = threading.Thread(target=self.chooseNumber, args=[3])
		load2 = threading.Thread(target=self.openText, args=[level])
		load.start()
		load.join()
		load2.start()
		load2.join()

	def initialiseApp(self):
		Factory.register('Question', cls=Question)
		Clock.schedule_once(
            lambda x: exec(f"from libs.baseclass import Manager"))
		self.buildKvFiles()
		Clock.schedule_once(
			lambda x: exec("self.root.ids.manager.add_widget(Factory.Manager())", {'self':self, 'Factory':Factory}))
		Clock.schedule_once(
            lambda x: exec(f"self.changeScreen('manager', self.root, 'left')", {'self': self}))

	def buildKvFiles(self):
		for kvFiles in os.listdir(os.environ['KvFolder']):
			Builder.load_file(os.path.join(os.environ['KvFolder'], kvFiles))

	def changeScreen(self, name, manager, direction):
		manager.transition.direction = direction
		manager.current = name

	def askQuestion(self):
		def ask():
			self.quest = self.questionList[self.position]
			pyttsx3.speak(f'Question {self.questionNumber}')
			pyttsx3.speak(f'Spell {self.quest}')
			self.repeat = True
		try:
			self.questionList[self.position]
		except IndexError:
			self.displayResult()
		else:
			self.runThread = threading.Thread(target=ask)
			self.runThread.start()

	def displayResult(self):
		ResultDialog(main=self, level=self.level, total=str(self.position), correct=str(self.correct), incorrect=str(self.incorrect), corrections=self.wrongDb).open()
		self.resetData()
		
		
	def checkSpelling(self, answer, total, correct, incorrect):
		if self.quest:
			if len(answer.text.strip()) != 0:
				if answer.text.strip().casefold() == self.quest.casefold():
					toast('Correct')
					self.doCorrect(correct)
				else:
					toast('Incorrect')
					self.doWrong(incorrect)
					self.wrongDb[self.quest.casefold().upper()] = answer.text.strip().casefold().upper()
				answer.text = ''
				self.questionNumber += 1
				self.position +=1
				self.makeChanges(total)
				self.repeat = False
				self.askQuestion()
			else:
				toast('Enter A Word')
		else:
			toast('Press the play button')

	def makeChanges(self, totalIns):
		totalIns.text = f"Total: [b]{self.position} of {len(self.questionList)}[/b]"

	def doCorrect(self, correctIns):
		self.correctSound.play()
		self.correct += 1
		correctIns.text = f'Correct: [b]{self.correct}[/b]'
		
	def doWrong(self, incorrectIns):
		self.incorrectSound.play()
		self.incorrect += 1
		incorrectIns.text = f'Incorrect: [b]{self.incorrect}[/b]'

PassySpellingApp().run()