from googletrans import Translator

class Search(Translator):
	def __init__(self, text_from, language_to):
		super(Search, self).__init__()
		self.text_from = text_from
		self.language_to = language_to

	def __repr__(self):
		return "<text_from: {}, text_to: {}, language_to>".format(
			self.text_from, self.language_to)

	def translate_txt(self):
		if self.language_to == "Português Brasileiro":
			return self.translate(self.fix_text_from_paper(), dest='pt')
		elif self.language_to == "Inglês":
			return self.translate(self.fix_text_from_paper(), dest='en')
		return self.translate(self.fix_text_from_paper(), dest='es')

	def fix_text_from_paper(self):
		return self.text_from.replace("\n", ' ')
		