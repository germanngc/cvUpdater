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
	template_color = {
		"background": [35, 116, 225],
		"foreground": [250, 250, 250],
		"lines": [80, 80, 80],
		"reset": [255, 255, 255],
		"text": [80, 80, 80]
	}

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

		self.Job = cvData.get('Job', [])
		self.Certification = cvData.get('Certification', [])
		self.Recognition = cvData.get('Recognition', [])
		self.Education = cvData.get('Education', [])

	def header(self):
		self.set_font('OpenSansItalic', '', 8)
		self.set_fill_color(self.template_color['background'][0], self.template_color['background'][1], self.template_color['background'][2])
		self.set_draw_color(self.template_color['background'][0], self.template_color['background'][1], self.template_color['background'][2])
		self.set_text_color(self.template_color['foreground'][0], self.template_color['foreground'][1], self.template_color['foreground'][2])
		self.cell(5, 6, '', 1, 0, 'C', 1)
		self.cell(103, 6, self.Title, 1, 0, 'L', 1)
		self.cell(103, 6, 'Version: ' + version + ', Build: ' + str(datetime.now().strftime("%Y%m%d")), 1, 0, 'R', 1)
		self.cell(5, 6, '', 1, 0, 'C', 1)

		self.set_draw_color(self.template_color['lines'][0], self.template_color['lines'][1], self.template_color['lines'][2])
		self.set_fill_color(self.template_color['lines'][0], self.template_color['lines'][1], self.template_color['lines'][2])

		self.rect(0, 6, 216, .5, 'F')

		self.set_fill_color(self.template_color['reset'][0], self.template_color['reset'][1], self.template_color['reset'][2])
		self.set_y(15)

	def footer(self):
		self.set_y(-15)
		self.set_font('OpenSansItalic', '', 8)
		self.cell(0, 10, 'Page' + str(self.page_no()) + ' / {nb}', 0, 0, 'C')

	def rightCol(self):
		self.set_xy(80, 11)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
		self.cell(130, 8, 'Work Experience', 0, 1, 'L', 0)
		self.ln(12)

		for item in self.Job:
			activities = item.get('Activities', [])
			company = item.get('Company', 'Unknown')
			description = item.get('Description', 'Unknown')
			end = item.get('End', 'Unknown')
			location = item.get('Location', 'Unknown')
			start = item.get('Start', 'Unknown')
			title = item.get('Title', 'Unknown')

			self.set_x(80)
			self.set_font('OpenSansBold', '', 10)
			self.cell(65, 5, str(title), 0, 0, 'L')
			self.cell(65, 5, str(company), 0, 1, 'R')
			self.set_x(80)
			self.set_font('OpenSans', '', 10)
			self.cell(130, 5, str(location + ' / From ' + start + ' to ' + end), 'B', 1, 'L')
			self.ln(2)
			self.set_x(80)
			self.set_font('OpenSans', '', 10)
			self.multi_cell(130, 5, str(description), 0, 'J')
			self.ln(2)
			self.set_x(80)
			self.set_font('OpenSansBold', '', 10)
			self.cell(18, 5, str('Activities: '), 0, 0, 'L')
			self.set_font('OpenSans', '', 10)
			self.multi_cell(111, 5, " / ".join(activities), 0, 'J')
			self.ln(8)

		self.set_x(80)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
		self.cell(130, 8, 'Certifications', 0, 1, 'L', 0)
		self.ln(6)

		self.set_x(80)
		self.set_font('OpenSansBold', '', 10)
		self.cell(55, 5, str('Certification'), 'B', 0, 'L')
		self.cell(55, 5, str('Insititution'), 'B', 0, 'L')
		self.cell(20, 5, str('Year'), 'B', 1, 'L')
		self.set_font('OpenSans', '', 10)

		for item in self.Certification:
			institution = item.get('Institution', 'Unknown')
			name = item.get('Name', 'Unknown')
			year = item.get('Year', 'Unknown')

			getY = self.get_y()
			highY = getY

			self.set_xy(80, getY)
			self.multi_cell(55, 5, str(name), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()
			self.set_xy(80 + 55, getY)
			self.multi_cell(55, 5, str(institution), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()
			self.set_xy(80 + 55 + 55, getY)
			highY = highY if highY > self.get_y() else self.get_y()
			self.multi_cell(20, 5, str(year), 0, 'L')
			self.set_xy(80, highY)
			self.ln(1)

		self.ln(12)
		self.set_x(80)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
		self.cell(130, 8, 'Recognitions', 0, 1, 'L', 0)
		self.ln(6)

		self.set_x(80)
		self.set_font('OpenSansBold', '', 10)
		self.cell(55, 5, str('Name'), 'B', 0, 'L')
		self.cell(55, 5, str('Insititution'), 'B', 0, 'L')
		self.cell(20, 5, str('Year'), 'B', 1, 'L')
		self.set_font('OpenSans', '', 10)

		for item in self.Recognition:
			institution = item.get('Institution', 'Unknown')
			name = item.get('Name', 'Unknown')
			year = item.get('Year', 'Unknown')

			getY = self.get_y()
			highY = getY

			self.set_xy(80, getY)
			self.multi_cell(55, 5, str(name), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()
			self.set_xy(80 + 55, getY)
			self.multi_cell(55, 5, str(institution), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()
			self.set_xy(80 + 55 + 55, getY)
			highY = highY if highY > self.get_y() else self.get_y()
			self.multi_cell(20, 5, str(year), 0, 'L')
			self.set_xy(80, highY)
			self.ln(1)

		self.ln(12)
		self.set_x(80)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
		self.cell(130, 8, 'Education', 0, 1, 'L', 0)
		self.ln(6)

		self.set_x(80)
		self.set_font('OpenSansBold', '', 10)
		self.cell(55, 5, str('Name'), 'B', 0, 'L')
		self.cell(55, 5, str('Insititution'), 'B', 0, 'L')
		self.cell(20, 5, str('Year'), 'B', 1, 'L')
		self.set_font('OpenSans', '', 10)

		for item in self.Recognition:
			institution = item.get('Institution', 'Unknown')
			name = item.get('Name', 'Unknown')
			year = item.get('Year', 'Unknown')

			getY = self.get_y()
			highY = getY

			self.set_xy(80, getY)
			self.multi_cell(55, 5, str(name), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()
			self.set_xy(80 + 55, getY)
			self.multi_cell(55, 5, str(institution), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()
			self.set_xy(80 + 55 + 55, getY)
			highY = highY if highY > self.get_y() else self.get_y()
			self.multi_cell(20, 5, str(year), 0, 'L')
			self.set_xy(80, highY)
			self.ln(1)
	
	def leftCol(self):
		self.set_xy(5, 11)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
		self.cell(60, 8, self.fullName, 0, 1, 'C', 0)

		self.set_x(5)
		self.set_font('OpenSansBold', '', 14)
		self.set_text_color(self.template_color['background'][0], self.template_color['background'][1], self.template_color['background'][2])
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
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
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
		self.set_draw_color(self.template_color['lines'][0], self.template_color['lines'][1], self.template_color['lines'][2])
		self.set_fill_color(self.template_color['lines'][0], self.template_color['lines'][1], self.template_color['lines'][2])
		self.rect(x, self.get_y() + 0.5, 25, 0.5, 'DF')
		self.set_draw_color(self.template_color['background'][0], self.template_color['background'][1], self.template_color['background'][2])
		self.set_fill_color(self.template_color['background'][0], self.template_color['background'][1], self.template_color['background'][2])
		self.rect((x + 25), self.get_y(), 10, 1.5, 'DF')
		self.set_draw_color(self.template_color['lines'][0], self.template_color['lines'][1], self.template_color['lines'][2])
		self.set_fill_color(self.template_color['lines'][0], self.template_color['lines'][1], self.template_color['lines'][2])
		self.rect((x + 35), self.get_y() + 0.5, 25, 0.5, 'DF')
		self.set_fill_color(self.template_color['reset'][0], self.template_color['reset'][1], self.template_color['reset'][2])
		self.set_fill_color(255, 255, 255)
		self.ln(4)

pdf = PDF('P', 'mm', 'Letter')
pdf.alias_nb_pages()
pdf.customvars()
pdf.set_margins(0, 0, 0)
pdf.add_font('OpenSans', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Regular.ttf', uni=True)
pdf.add_font('OpenSansBold', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Bold.ttf', uni=True)
pdf.add_font('OpenSansItalic', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Italic.ttf', uni=True)
pdf.add_page()
# pdf.set_font('OpenSans', '', 12)
pdf.leftCol()
pdf.rightCol()

#for i in range(1, 10):
# 	pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)

Information = cvData.get('Information', [])
cvOwnerOutput = Information.get('Name', 'Missing')
cvOwnerOutput = 'output/' + cvOwnerOutput.replace(' ', '-') + '-Resume.pdf'

pdf.output(cvOwnerOutput, 'F')
print('Your resume is ready under: ' + cvOwnerOutput)