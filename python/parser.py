import math
import yaml

from datetime import datetime
from fpdf import FPDF
from yaml.loader import SafeLoader

cvData = []
version = '1.0.1'

# Open the file and load the file
with open('cv.yaml') as f:
	cvData = yaml.load(f, Loader=yaml.FullLoader)

class PDF(FPDF):
	def customvars(self):
		self.Information = cvData.get('Information', [])
		self.AboutMe = self.Information.get('AboutMe', [])
		self.Contact = self.Information.get('Contact', [])
		self.Languages = self.Information.get('Languages', [])
		self.Softwares = self.Information.get('Softwares', [])
		self.Skills = self.Information.get('Skills', [])

		self.fullName = self.Information.get('FullName', 'Missing')
		self.roleName = self.Information.get('RoleName', 'Missing')
		self.Title = 'Resume py Parser by Nina Code'

	def header(self):
		self.set_font('OpenSansItalic', '', 8)
		self.set_fill_color(76, 181, 255)
		self.set_draw_color(76, 181, 255)
		self.set_text_color(250, 250, 250)
		self.cell(10, 6, '', 1, 0, 'C', 1)
		self.cell(95, 6, self.Title, 1, 0, 'L', 1)
		self.cell(95, 6, 'Version: ' + version + ', Build: ' + str(datetime.now().strftime("%Y%m%d")), 1, 0, 'R', 1)
		self.cell(10, 6, '', 1, 0, 'C', 1)

		self.set_draw_color(80, 80, 80)
		self.set_fill_color(115, 115, 115)
		self.rect(0, 6, 210, .5, 'F')

		self.set_fill_color(255, 255, 255)
		self.ln(1)

	def footer(self):
		self.set_y(-15)
		self.set_font('OpenSansItalic', '', 8)
		self.cell(0, 10, 'Page' + str(self.page_no()) + ' / {nb}', 0, 0, 'C')
	
	def leftCol(self):
		self.set_xy(5, 11)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(80, 80, 80)
		self.cell(60, 8, self.fullName, 0, 1, 'C', 0)

		self.set_x(5)
		self.set_font('OpenSansBold', '', 14)
		self.set_text_color(76, 181, 255)
		self.cell(60, 6, self.roleName, 0, 1, 'C', 0)

		# About me Block
		self.leftColBlock(self.AboutMe, 'ABOUT ME', 'table')

		# Contacts Block
		self.leftColBlock(self.Contact, 'CONTACT', 'table')

		# Languages Block
		self.leftColBlock(self.Languages, 'LANGUAGES', 'table')

		# Softwares Block
		self.leftColBlock(self.Softwares, 'SOFTWARES', 'inline')

		# Skills Block
		self.leftColBlock(self.Skills, 'SKILLS', 'inline')

	def leftColBlock(self, data, blockName = 'Missing', layout = 'table'):
		self.ln(5)
		self.set_x(5)
		self.set_font('OpenSansBold', '', 12)
		self.set_text_color(80, 80, 80)
		self.cell(60, 6, blockName, 0, 1, 'C', 0)
		self.separatorA(5)
		self.ln(1)

		if (layout == 'table'):
			for item in data:
				self.set_x(5)
				self.set_font('OpenSansBold', '', 10)
				labelName = str(item) + ': '
				labelWidth = math.ceil(self.get_string_width(labelName))
				self.cell(labelWidth, 5, labelName, 0, 0, 'L')
				self.set_font('OpenSans', '', 10)
				self.cell(60 - labelWidth, 5, str(data[item]), 0, 1, 'L')
		else:
			self.set_x(5)
			self.set_font('OpenSans', '', 10)
			self.cell(60, 5, " / ".join(data), 0, 1, 'L')


	def separatorA(self, x):
		self.set_draw_color(80, 80, 80)
		self.set_fill_color(80, 80, 80)
		self.rect(x, self.get_y() + 0.5, 25, 0.5, 'DF')
		self.set_draw_color(76, 181, 255)
		self.set_fill_color(76, 181, 255)
		self.rect((x + 25), self.get_y(), 10, 1.5, 'DF')
		self.set_draw_color(80, 80, 80)
		self.set_fill_color(80, 80, 80)
		self.rect((x + 35), self.get_y() + 0.5, 25, 0.5, 'DF')
		self.set_fill_color(255, 255, 255)
		self.ln(4)

pdf = PDF()
pdf.alias_nb_pages()
pdf.customvars()
pdf.set_margins(0, 0, 0)
pdf.add_font('OpenSans', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Regular.ttf', uni=True)
pdf.add_font('OpenSansBold', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Bold.ttf', uni=True)
pdf.add_font('OpenSansItalic', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Italic.ttf', uni=True)
pdf.add_page()
# pdf.set_font('OpenSans', '', 12)
pdf.leftCol()

#for i in range(1, 10):
# 	pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)

Information = cvData.get('Information', [])
cvOwnerOutput = Information.get('Name', 'Missing')
cvOwnerOutput = 'output/' + cvOwnerOutput.replace(' ', '-') + '-Resume.pdf'

pdf.output(cvOwnerOutput, 'F')
print('Your resume is ready under: ' + cvOwnerOutput)