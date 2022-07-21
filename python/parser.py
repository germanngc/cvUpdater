import math
import yaml
from fpdf import FPDF
from yaml.loader import SafeLoader

cvData = []
version = '1.0.0'

# Open the file and load the file
with open('cv.yaml') as f:
	cvData = yaml.load(f, Loader=yaml.FullLoader)

class PDF(FPDF):
	def customvars(self):
		self.Information = cvData.get('Information', [])
		self.cvOwner = self.Information.get('Name', 'Missing')
		self.cvRoleName = self.Information.get('RoleName', 'Missing')

		self.AboutMe = self.Information.get('AboutMe', [])
		self.Birthday = self.AboutMe.get('Birthday', 'Missing')
		self.Location = self.AboutMe.get('Location', 'Missing')
		self.Nacionality = self.AboutMe.get('Nacionality', 'Missing')
		self.PassportExp = str(self.AboutMe.get('PassportExp', 'Missing'))
		self.VisaExp = str(self.AboutMe.get('VisaExp', 'Missing'))

		self.Contact = self.Information.get('Contact', [])
		self.Email = self.Contact.get('Email', 'Missing')
		self.Phone = self.Contact.get('Phone', 'Missing')

		self.Languages = self.Information.get('Languages', [])
		self.Softwares = self.Information.get('Softwares', [])
		self.Skills = self.Information.get('Skills', [])

		self.Title = 'Resume py Parser v' + version + ' by ' + self.cvOwner

	def header(self):
		self.set_font('Arial', 'I', 8)
		self.set_fill_color(76, 181, 255)
		self.set_draw_color(76, 181, 255)
		self.set_text_color(250, 250, 250)
		self.cell(10, 10, '', 1, 0, 'C', 1)
		self.cell(190, 10, self.Title, 1, 0, 'R', 1)
		self.cell(10, 10, '', 1, 0, 'C', 1)

		self.set_draw_color(80, 80, 80)
		self.set_fill_color(115, 115, 115)
		self.rect(0, 10, 210, 1, 'F')

		self.set_fill_color(255, 255, 255)
		self.ln(1)

	def footer(self):
		self.set_y(-15)
		self.set_font('Arial', 'I', 8)
		self.cell(0, 10, 'Page' + str(self.page_no()) + ' / {nb}', 0, 0, 'C')
	
	def leftCol(self):
		self.set_xy(5, 11)
		self.set_font('Arial', 'B', 16)
		self.set_text_color(80, 80, 80)
		self.cell(60, 8, self.cvOwner, 0, 1, 'C', 0)

		self.set_x(5)
		self.set_font('Arial', 'B', 14)
		self.set_text_color(76, 181, 255)
		self.cell(60, 6, self.cvRoleName, 0, 1, 'C', 0)

		# About Me: 
		self.ln(5)
		self.set_x(5)
		self.set_font('Arial', 'B', 12)
		self.set_text_color(80, 80, 80)
		self.cell(60, 6, 'ABOUT ME', 0, 1, 'C', 0)
		self.separatorA(5)

		# About Me: Nacionality
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'Nacionality: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.Nacionality, 0, 1, 'L')

		# About Me: Birtday
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'Birthday: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.Birthday, 0, 1, 'L')

		# About Me: Location
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'Location: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.Location, 0, 1, 'L')

		# About Me: PassportExp
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'Passport Exp: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.PassportExp, 0, 1, 'L')

		# About Me: VisaExp
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'US VISA Exp: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.VisaExp, 0, 1, 'L')

		# Contact: 
		self.ln(5)
		self.set_x(5)
		self.set_font('Arial', 'B', 12)
		self.set_text_color(80, 80, 80)
		self.cell(60, 6, 'CONTACT', 0, 1, 'C', 0)
		self.separatorA(5)

		# Contact: Email
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'Email: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.Email, 0, 1, 'L')

		# Contact: Phone
		self.set_x(5)
		self.set_font('Arial', 'B', 10)
		labelName = 'Phone: '
		labelWidth = math.ceil(self.get_string_width(labelName))
		self.cell(labelWidth, 5, labelName, 0, 0, 'L')
		self.set_font('Arial', '', 10)
		self.cell(60 - labelWidth, 5, self.Phone, 0, 1, 'L')

		# Languages:
		self.ln(5)
		self.set_x(5)
		self.set_font('Arial', 'B', 12)
		self.set_text_color(80, 80, 80)
		self.cell(60, 6, 'LANGUAGES', 0, 1, 'C', 0)
		self.separatorA(5)

		for lngs in self.Languages:
			self.set_x(5)
			self.set_font('Arial', 'B', 10)
			labelName = str(lngs) + ': '
			labelWidth = math.ceil(self.get_string_width(labelName))
			self.cell(labelWidth, 5, labelName, 0, 0, 'L')
			self.set_font('Arial', '', 10)
			self.cell(60 - labelWidth, 5, self.Languages[str(lngs)], 0, 1, 'L')

		# Softwares:
		self.ln(5)
		self.set_x(5)
		self.set_font('Arial', 'B', 12)
		self.set_text_color(80, 80, 80)
		self.cell(60, 6, 'SOFTWARES', 0, 1, 'C', 0)
		self.separatorA(5)

		self.set_x(5)
		self.set_font('Arial', '', 10)
		self.cell(60, 5, " / ".join(self.Softwares), 0, 1, 'L')

		# Skills:
		self.ln(5)
		self.set_x(5)
		self.set_font('Arial', 'B', 12)
		self.set_text_color(80, 80, 80)
		self.cell(60, 6, 'SKILLS', 0, 1, 'C', 0)
		self.separatorA(5)

		self.set_x(5)
		self.set_font('Arial', '', 10)
		self.cell(60, 5, " / ".join(self.Skills), 0, 1, 'L')

	def separatorA(self, x):
		self.set_draw_color(80, 80, 80)
		self.set_fill_color(80, 80, 80)
		self.rect(x, self.get_y() + 1, 25, 1, 'DF')
		self.set_draw_color(76, 181, 255)
		self.set_fill_color(76, 181, 255)
		self.rect((x + 25), self.get_y(), 10, 3, 'DF')
		self.set_draw_color(80, 80, 80)
		self.set_fill_color(80, 80, 80)
		self.rect((x + 35), self.get_y() + 1, 25, 1, 'DF')
		self.set_fill_color(255, 255, 255)
		self.ln(4)

pdf = PDF()
pdf.alias_nb_pages()
pdf.customvars()
pdf.set_margins(0, 0, 0)
pdf.add_page()
pdf.set_font('Times', '', 12)
pdf.leftCol()

#for i in range(1, 10):
# 	pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)

pdf.output('cv.pdf', 'F')