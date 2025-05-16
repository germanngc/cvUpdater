#!/usr/bin/env python3

from datetime import date
from datetime import datetime
from dateutil.parser import parse
import math
import yaml

from fpdf import FPDF
from yaml.loader import SafeLoader

import sys
import os
import time

from utils.charts import radar_chart

cvData = []
version = '2.0.0'
inputCv = 'cv.yaml'

if len(sys.argv) > 1:
	inputCv = sys.argv[1]

# Open the file and load the file
with open(inputCv) as f:
	cvData = yaml.load(f, Loader=yaml.FullLoader)

class PDF(FPDF):
	template_color = {
		"background": [35, 116, 225],
		"foreground": [250, 250, 250],
		"lines": [80, 80, 80],
		"reset": [255, 255, 255],
		"text": [80, 80, 80]
	}
	
	mainHeadY = 11

	def getJobAge(self, start, end):
		num_years = end.year - start.year
		num_months = end.month - start.month
		
		if end.day < start.day:
			num_months -= 1

		if num_months < 0:
			num_years -= 1
			num_months += 12

		yearPloural = 'Year' if num_years == 1 else 'Years'
		monthPloural = 'Month' if num_months == 1 else 'Months'

		if num_years > 0:
			return str(num_years) + ' ' + yearPloural + ', ' + str(num_months) + ' ' + monthPloural
		else:
			return str(num_months) + ' ' + monthPloural

	def setMarker(self):
		xMarker = 70 if self.page_no() == 1 else 5


	def customvars(self):
		self.Information = cvData.get('Information', [])
		self.AboutMe = self.Information.get('AboutMe', [])
		self.Contact = self.Information.get('Contact', [])
		self.Social = self.Information.get('Social', [])
		self.Languages = self.Information.get('Languages', [])
		self.Technologies = self.Information.get('Technologies', [])
		self.Skills = self.Information.get('Skills', [])

		self.Email = self.Information.get('Email', 'Missing')
		self.FullName = self.Information.get('FullName', 'Missing')
		self.Location = self.Information.get('Location', 'Missing')
		self.Phone = self.Information.get('Phone', 'Missing')
		self.RoleName = self.Information.get('RoleName', 'Missing')
		self.Summary = self.Information.get('Summary', 'Missing')
		self.Title = 'Resume py Parser by Nina Code'

		self.Job = cvData.get('Job', [])
		self.Certification = cvData.get('Certification', []) or []
		self.Recognition = cvData.get('Recognition', []) or []
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
		self.cell(0, 10, 'Page ' + str(self.page_no()) + ' / {nb}', 0, 1, 'C')
		self.set_y(-10)
		self.cell(0, 10, 'Iconos by Freepik, Ilham Fitrotul Hayat and Those Icons - Flaticon', 0, 1, 'C', 0, 'https://www.flaticon.es')

	def mainHead(self):
		self.set_xy(5, 11)
		self.set_x(5)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])
		self.cell(200, 8, self.FullName, 0, 1, 'L', 0)

		self.set_x(5)
		self.set_font('OpenSans', '', 14)
		self.set_text_color(self.template_color['background'][0], self.template_color['background'][1], self.template_color['background'][2])
		self.cell(200, 6, self.RoleName, 0, 1, 'L', 0)
		self.ln()

		self.set_x(5)
		self.set_font('OpenSansLight', '', 12)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])

		getX = self.get_x()
		getY = self.get_y()
		cellSizePhone = math.ceil(self.get_string_width(self.Phone)) + 2
		cellSizeEmail = math.ceil(self.get_string_width(self.Email)) + 2
		cellSizeLocation = math.ceil(self.get_string_width(self.Location)) + 2
		cellSizeSep = math.ceil((cellSizePhone + cellSizeEmail + cellSizeLocation + 16) / 2)

		self.cell(cellSizeSep, 6, '', 0, 0, 'L', 0)
		self.set_x(cellSizeSep)

		getX = self.get_x()

		self.image('./icons/phone.png', getX, getY + 1, 4, 4, 'PNG')
		self.set_x(getX + 4)
		self.cell(cellSizePhone, 6, self.Phone, 0, 0, 'L', 0, 'tel:' + self.Phone)
		getX = self.get_x() + 2
		self.set_x(getX)

		self.image('./icons/at.png', getX, getY + 1, 4, 4, 'PNG')
		self.set_x(getX + 4)
		self.cell(cellSizeEmail, 6, self.Email, 0, 0, 'L', 0, 'mailto:' + self.Email)
		getX = self.get_x() + 2
		self.set_x(getX)

		self.image('./icons/location.png', getX, getY + 1, 4, 4, 'PNG')
		self.set_x(getX + 4)
		self.cell(cellSizeLocation, 6, self.Location, 0, 0, 'L', 0)
		self.ln()

		# self.set_x(5)
		# self.set_font('OpenSansBold', '', 16)
		# self.cell(200, 6, "Summary", 0, 1, 'L', 0)

		# self.set_x(5)
		# self.set_font('OpenSansLight', '', 10)
		# self.multi_cell(200, 6, self.Summary, 0, 'L', 0)
		# self.ln()

		self.ln()
		self.mainHeadY = self.get_y()

	def leftCol(self):
		# self.set_xy(5, 11)
		self.set_xy(5, self.mainHeadY)

		# About me Block
		self.leftColBlock(self.AboutMe, 'ABOUT ME', 'table')

		# Contacts Block
		# self.leftColBlock(self.Contact, 'CONTACT', 'table')

		# Languages Block
		self.leftColBlock(self.Languages, 'LANGUAGES', 'table')

		# Social Block
		self.leftColBlock(self.Social, 'SOCIAL', 'table', False, True)

		# Technologies Block
		self.leftColBlock(self.Technologies, 'TECH STACK', 'inline', True)

		# Skills Block
		# self.leftColBlock(self.Skills, 'SKILLS', 'inline')

	def leftColBlock(self, data, blockName = 'Missing', layout = 'table', bread_crumbs = False, link = False):
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
				labelName = str(item)
				linkToSet = ""

				if link == False:
					labelName = labelName + ': '
					labelWidth = math.ceil(self.get_string_width(labelName))
					self.cell(labelWidth, 5, labelName, 0, 0 if link == False else 1, 'L', False, linkToSet)
					self.set_font('OpenSans', '', 10)
					self.multi_cell(60 - labelWidth, 5, str(data[item]), 0, 'L')
				else:
					self.set_font('OpenSans', '', 10)
					self.write(5, str(data[item]), str(data[item]))
					self.ln()
		else:
			self.set_x(5)
			self.set_font('OpenSans', '', 10 if bread_crumbs == True else 7)
			self.multi_cell(60, 5, " / ".join(data), 0, 'J')

		self.ln(5)

	def rightCol(self):
		xMarker = 70 if self.page_no() == 1 else 5
		reversedXMarker = 5 if self.page_no() == 1 else 70

		self.set_xy(xMarker, self.mainHeadY)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])

		if (self.get_y() + 8 + 8) > 255:
			self.add_page()
			self.set_x(xMarker)

		xMarker = 70 if self.page_no() == 1 else 5
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.cell(140 + (reversedXMarker + 5), 8, "Summary", 0, 1, 'L', 0)

		xMarker = 70 if self.page_no() == 1 else 5
		self.set_x(xMarker)
		self.set_font('OpenSansLight', '', 10)
		self.multi_cell(140 + (reversedXMarker - 5), 6, str(self.Summary), 0, 'J')
		self.ln()

		xMarker = 70 if self.page_no() == 1 else 5
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.cell(140 + (reversedXMarker + 5), 8, 'Skills', 0, 1, 'L', 0)
		self.ln(2)

		for item in self.Skills:
			xMarker = 70 if self.page_no() == 1 else 5
			self.set_x(xMarker)
			self.set_font('OpenSansBold', '', 10)
			self.cell(140 + (reversedXMarker + 5), 6, str(item['name'] + ': '), 0, 1, 'L', 1)
			xMarker = 70 if self.page_no() == 1 else 5
			self.set_x(xMarker)
			self.set_font('OpenSansLight', '', 10)
			self.multi_cell(140 + (reversedXMarker - 5), 6, str(item['skill']), 0, 'L')
			self.ln(1)

		self.ln(7)

		xMarker = 70 if self.page_no() == 1 else 5
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.cell(140 + (reversedXMarker + 5), 8, 'Education', 0, 1, 'L', 0)
		self.ln(2)

		for item in self.Education:
			institution = item.get('Institution', 'Unknown')
			location = item.get('Location', 'Unknown')
			name = item.get('Name', 'Unknown')
			year = item.get('Year', 'Unknown')
			reversedXMarker = 5 if self.page_no() == 1 else 70

			xMarker = 70 if self.page_no() == 1 else 5
			self.set_x(xMarker)
			self.set_font('OpenSansBold', '', 10)
			self.cell(130 + (reversedXMarker - 5), 4, str(name), 0, 1, 'L')
			self.ln(1)

			xMarker = 70 if self.page_no() == 1 else 5
			self.set_x(xMarker)
			self.set_font('OpenSans', '', 10)
			self.cell(130 + (reversedXMarker - 5), 4, str(institution + ' / ' + location + ' / ') + str(year), 0, 1, 'L')
			self.ln(1)

		self.ln(7)

		self.add_page()

		xMarker = 70 if self.page_no() == 1 else 5
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.cell(140 + (reversedXMarker + 5), 8, 'Employment History', 0, 1, 'L', 0)
		self.ln(8)

		for item in self.Job:
			activities = item.get('Activities', [])
			technologies = item.get('Technologies', [])
			company = item.get('Company', 'Unknown')
			description = item.get('Description', 'Unknown')
			end = item.get('End', date.today())
			end_string = item.get('End', 'Current')
			location = item.get('Location', 'Unknown')
			start = item.get('Start', date.today())
			title = item.get('Title', 'Unknown')
			type = item.get('Type', 'Full time')

			end = date.today() if end == 'Current' else end
			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70

			try:
				parse(end.strftime("%B/%Y"), False)
			except ValueError:
				end = date.today()
			except TypeError:
				end = date.today()

			try:
				parse(end_string.strftime("%b %Y"), False)
				end_string = end_string.strftime("%b %Y")
			except ValueError:
				end_string = 'Current'
			except TypeError:
				end_string = 'Current'
			except AttributeError:
				end_string = 'Current'

			try:
				parse(start.strftime("%b %Y"), False)
			except ValueError:
				start = date.today()
			except TypeError:
				start = date.today()

			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70
			self.set_x(xMarker)
			self.set_font('OpenSansBold', '', 10)
			self.cell(52 + ((reversedXMarker - 5) / 3), 4, str(title), 0, 0, 'L')
			# self.cell(35 + ((reversedXMarker - 5) / 3), 4, str(type), 0, 0, 'C')
			self.cell(35 + ((reversedXMarker - 5) / 3), 4, str(''), 0, 0, 'C')
			self.cell(52 + ((reversedXMarker - 5) / 3), 4, str(company), 0, 1, 'R')
			self.ln(2)
			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70
			self.set_x(xMarker)
			self.set_font('OpenSans', '', 10)
			# self.cell(100 + (reversedXMarker - 5), 6, str(location + '   /   From ' + start.strftime("%B/%Y") + ' to ' + end_string), 'B', 0, 'L')
			self.cell(100 + (reversedXMarker - 5), 6, str(start.strftime("%b %Y") + ' -- ' + end_string), 'B', 0, 'L')
			self.cell(40, 6, self.getJobAge(start, end), 'B', 1, 'R')
			self.ln(2)

			if self.get_y() > 255:
				self.add_page()

			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70
			self.set_x(xMarker)
			self.set_font('OpenSansLight', '', 10)
			self.multi_cell(140 + (reversedXMarker - 5), 6, str(description), 0, 'J')
			
			if self.get_y() > 255:
				self.add_page()
			
			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70
			self.set_x(xMarker)
			self.set_font('OpenSans', '', 10)
			self.ln(2)

			if self.get_y() > 255:
				self.add_page()

			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70
			self.set_x(xMarker)
			self.cell(15, 6, str('Activities and Responsabilities: '), 0, 0, 'L')
			self.ln()

			for item in activities:
				if self.get_y() > 255:
					self.add_page()

				xMarker = 70 if self.page_no() == 1 else 5
				reversedXMarker = 5 if self.page_no() == 1 else 70
				self.set_x(xMarker + 5)
				self.set_font('OpenSansLight', '', 10)
				self.multi_cell(115 + (reversedXMarker - 5), 6, str("• " + item), 0, 'J')

			self.ln(2)

			if self.get_y() > 255:
				self.add_page()

			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70
			self.set_x(xMarker)
			self.set_font('OpenSans', '', 10)
			self.cell(18, 6, str('Technologies: '), 0, 0, 'L')
			self.set_font('OpenSansLight', '', 10)
			self.multi_cell(117 + (reversedXMarker - 5), 6, ", ".join(technologies) + ".", 0, 'J')

			self.ln(13)

			if self.get_y() > 255:
				self.add_page()

		xMarker = 70 if self.page_no() == 1 else 5
		reversedXMarker = 5 if self.page_no() == 1 else 70

		# self.add_page()
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])

		if (self.get_y() + 8 + 8) > 255:
			self.add_page()
			self.set_x(xMarker)

		self.cell(130 + (reversedXMarker - 5), 8, 'Certifications', 0, 1, 'L', 0)
		self.ln(8)

		getY = self.get_y()

		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 10)
		self.cell(55 + ((reversedXMarker - 5) / 2), 6, str('Certification'), 'B', 0, 'L')
		self.cell(55 + ((reversedXMarker - 5) / 2), 6, str('Insititution'), 'B', 0, 'L')
		self.cell(20, 6, str('Year'), 'B', 1, 'L')
		self.ln(2)
		self.set_font('OpenSans', '', 10)

		anchorY = self.get_y()

		if anchorY > 255:
			self.add_page()
			anchorY = 11

		for item in self.Certification:
			institution = item.get('Institution', 'Unknown')
			name = item.get('Name', 'Unknown')
			year = item.get('Year', 'Unknown')

			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70

			self.set_xy(xMarker, anchorY)
			self.multi_cell(55 + ((reversedXMarker - 5) / 2), 4, str(name), 0, 'L')
			#highY = highY if highY > self.get_y() else self.get_y()
			#highY = highY if highY > 255 else -15

			self.set_xy(xMarker + 55 + ((reversedXMarker - 5) / 2), anchorY)
			self.multi_cell(55 + ((reversedXMarker - 5) / 2), 4, str(institution), 0, 'L')
			# highY = highY if highY > self.get_y() else self.get_y()
			# highY = highY if highY > 255 else -15

			self.set_xy(xMarker + 55 + 55 + ((reversedXMarker - 5) / 2) + ((reversedXMarker - 5) / 2), anchorY)
			self.multi_cell(20, 4, str(year), 0, 'L')
			# highY = highY if highY > self.get_y() else self.get_y()

			anchorY = self.get_y()

			if anchorY > 255:
				self.add_page()
				anchorY = 11

			# self.set_xy(xMarker, highY)
			self.ln(1)

		xMarker = 70 if self.page_no() == 1 else 5
		reversedXMarker = 5 if self.page_no() == 1 else 70

		self.ln(8)
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])

		if (self.get_y() + 8 + 8) > 255:
			self.add_page()
			self.set_x(xMarker)

		self.cell(130 + (reversedXMarker - 5), 8, 'Recognitions', 0, 1, 'L', 0)
		self.ln(8)

		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 10)
		self.cell(55 + ((reversedXMarker - 5) / 2), 6, str('Name'), 'B', 0, 'L')
		self.cell(55 + ((reversedXMarker - 5) / 2), 6, str('Insititution'), 'B', 0, 'L')
		self.cell(20, 6, str('Year'), 'B', 1, 'L')
		self.ln(2)
		self.set_font('OpenSans', '', 10)

		for item in self.Recognition:
			institution = item.get('Institution', 'Unknown')
			name = item.get('Name', 'Unknown')
			year = item.get('Year', 'Unknown')

			getY = self.get_y()
			highY = getY
			xMarker = 70 if self.page_no() == 1 else 5
			reversedXMarker = 5 if self.page_no() == 1 else 70

			self.set_xy(xMarker, getY)
			self.multi_cell(55 + ((reversedXMarker - 5) / 2), 4, str(name), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()

			self.set_xy(xMarker + 55 + ((reversedXMarker - 5) / 2), getY)
			self.multi_cell(55 + ((reversedXMarker - 5) / 2), 4, str(institution), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()

			self.set_xy(xMarker + 55 + 55 + ((reversedXMarker - 5) / 2) + ((reversedXMarker - 5) / 2), getY)
			self.multi_cell(20, 4, str(year), 0, 'L')
			highY = highY if highY > self.get_y() else self.get_y()

			if highY > 255:
				self.add_page()
				highY = 11

			self.set_xy(xMarker, highY)
			self.ln(1)

		xMarker = 70 if self.page_no() == 1 else 5
		reversedXMarker = 5 if self.page_no() == 1 else 70

		self.ln(8)
		self.set_x(xMarker)
		self.set_font('OpenSansBold', '', 16)
		self.set_text_color(self.template_color['text'][0], self.template_color['text'][1], self.template_color['text'][2])

		if (self.get_y() + 8 + 8) > 255:
			self.add_page()
			self.set_x(xMarker)

		# self.cell(130 + (reversedXMarker - 5), 8, 'Education', 0, 1, 'L', 0)
		# self.ln(8)
		# self.set_font('OpenSans', '', 10)

		# for item in self.Education:
		# 	institution = item.get('Institution', 'Unknown')
		# 	location = item.get('Location', 'Unknown')
		# 	name = item.get('Name', 'Unknown')
		# 	year = item.get('Year', 'Unknown')
		# 	xMarker = 70 if self.page_no() == 1 else 5
		# 	reversedXMarker = 5 if self.page_no() == 1 else 70

		# 	self.set_x(xMarker)
		# 	self.set_font('OpenSansBold', '', 10)
		# 	self.cell(130 + (reversedXMarker - 5), 4, str(name), 0, 1, 'L')

		# 	self.set_x(xMarker)
		# 	self.set_font('OpenSans', '', 10)
		# 	self.cell(130 + (reversedXMarker - 5), 4, str(institution + ' / ' + location + ' / ') + str(year), 0, 1, 'L')
		# 	self.ln(1)

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
pdf.add_font('OpenSansLight', '', r'fonts/Open_Sans/static/OpenSans_Condensed/OpenSans_Condensed-Light.ttf', uni=True)
pdf.add_page()
# pdf.set_font('OpenSans', '', 12)
pdf.mainHead()
pdf.leftCol()
pdf.rightCol()

#for i in range(1, 10):
# 	pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)

Information = cvData.get('Information', [])
cvOwnerOutput = Information.get('Name', 'Missing')
cvOwnerOutput = 'output/' + cvOwnerOutput.replace(' ', '-') + '-Resume.pdf'

pdf.output(cvOwnerOutput, 'F')
print('Your resume is ready under: ' + cvOwnerOutput)
