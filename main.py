import os
import sys
import PySimpleGUI as sg
import xml.etree.ElementTree as ET

n_const = 0.0090090090090
o_const = 0.0152

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

def getCoordinates(og, om, os, ng, nm, ns, multi):
	n = ((float(ns) / 60) + float(nm)) / 60 + float(ng)
	o = ((float(os) / 60) + float(om)) / 60 + float(og)
	p1n = n - int(multi) / 2 * n_const
	p1o = o - int(multi) / 2 * o_const
	p2n = p1n
	p2o = p1o + int(multi) * o_const
	p3n = p2n + int(multi) * n_const
	p3o = p2o
	p4n = p3n
	p4o = p1o
	
	p1ng = int(p1n)
	p1nm = int((p1n - p1ng) * 60)
	p1ns = ((p1n - p1ng) * 60) - p1nm
	p1og = int(p1o)
	p1om = int((p1o - p1og) * 60)
	p1os = ((p1o - p1og) * 60) - p1om
	
	p3ng = int(p3n)
	p3nm = int((p3n - p3ng) * 60)
	p3ns = ((p3n - p3ng) * 60) - p3nm
	p3og = int(p3o)
	p3om = int((p3o - p3og) * 60)
	p3os = ((p3o - p3og) * 60) - p3om
	coord = str(p1o) + ',' + str(p1n) + ',0 ' + str(p2o) + ',' + str(p2n) + ',0 ' + str(p3o) + ',' + str(p3n) + ',0  ' + str(p4o) + ',' + str(p4n) + ',0  ' + str(p1o) + ',' + str(p1n) + ',0 '
	tl = 'O: ' + str(p1og) + ' G ' + str(p1om) + ' M ' + str("{:.2f}".format(p1os) + ' S ') + ', N: ' + str(p1ng) + ' G ' + str(p1nm) + ' M ' + str("{:.2f}".format(p1ns) + ' S')
	br = 'O: ' + str(p3og) + ' G ' + str(p3om) + ' M ' + str("{:.2f}".format(p3os) + ' S ') + ', N: ' + str(p3ng) + ' G ' + str(p3nm) + ' M ' + str("{:.2f}".format(p3ns) + ' S')
	return [coord, tl, br]

try:
	import pyi_splash
	pyi_splash.update_text('UI Loaded ...')
	pyi_splash.close()
except:
	pass

sg.set_options(icon = resource_path("logo.ico"))

layout = [	[sg.Text('N Grad, Minute, Sekunde')],
			[sg.Input('', key = '-BG-'), sg.Input('', key = '-BM-'), sg.Input('', key = '-BS-')],
			[sg.Text('O Grad, Minute, Sekunde')],
			[sg.Input('', key = '-LG-'), sg.Input('', key = '-LM-'), sg.Input('', key = '-LS-')],
			[sg.Text('Kantenlänge Ausschnitt in km'), sg.Combo([2,4,8,16,32], default_value = 2, key = '-SIZE-')],
			[sg.Button('Erzeugen', key = '-CREATE-'), sg.Button('Exit', key = '-EXIT-')],
]

window = sg.Window('Cutout from Google Earth', layout, finalize = True, location = (50, 50))

while True:
	event, values = window.read()
	#print(event, values)
	if event == sg.WIN_CLOSED or event=="-EXIT-":
		break
	elif event == '-CREATE-':
		folder = sg.popup_get_folder('', title = 'Speichern unter', default_path = os.path.expanduser('~') + os.sep + 'Desktop')
		if folder != None:
			root = ET.Element('kml')
			root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
			root.attrib["xmlns:gx"] = "http://www.google.com/kml/ext/2.2"
			root.attrib["xmlns:kml"] = "http://www.opengis.net/kml/2.2"
			root.attrib["xmlns:atom"] = "http://www.w3.org/2005/Atom"
			doc = ET.SubElement(root, 'Document')
			ET.SubElement(doc, 'name').text = 'cutout.kml'

			style = ET.SubElement(doc, 'Style', id = "inline")
			lineStyle = ET.SubElement(style, 'LineStyle')
			ET.SubElement(lineStyle, 'color').text = 'ff0000ff'
			ET.SubElement(lineStyle, 'width').text = '2'
			polyStyle = ET.SubElement(style, 'PolyStyle')
			ET.SubElement(polyStyle, 'fill').text = '0'

			styleMap = ET.SubElement(doc, 'StyleMap', id = "inline0")
			pair = ET.SubElement(styleMap, 'Pair')
			ET.SubElement(pair, 'key').text = 'normal'
			ET.SubElement(pair, 'styleUrl').text = '#inline1'
			pair = ET.SubElement(styleMap, 'Pair')
			ET.SubElement(pair, 'key').text = 'highlight'
			ET.SubElement(pair, 'styleUrl').text = '#inline'

			style1 = ET.SubElement(doc, 'Style', id = "inline1")
			lineStyle1 = ET.SubElement(style1, 'LineStyle')
			ET.SubElement(lineStyle1, 'color').text = 'ff0000ff'
			ET.SubElement(lineStyle1, 'width').text = '2'
			polyStyle1 = ET.SubElement(style1, 'PolyStyle')
			ET.SubElement(polyStyle1, 'fill').text = '0'

			placemark = ET.SubElement(doc, 'Placemark')
			ET.SubElement(placemark, 'name').text = 'map_cutout'
			ET.SubElement(lineStyle, 'styleUrl').text = '#inline0'
			lineString = ET.SubElement(placemark, 'LineString')
			ET.SubElement(lineString, 'tessellate').text = '0'
			ret = getCoordinates(values['-LG-'], values['-LM-'], values['-LS-'], values['-BG-'], values['-BM-'], values['-BS-'], values['-SIZE-'])
			ET.SubElement(lineString, 'coordinates').text = ret[0]
			ET.SubElement(lineString, 'corner_tl').text = ret[1]
			ET.SubElement(lineString, 'corner_br').text = ret[2]

			tree = ET.ElementTree(root)
			ET.indent(tree)
			tree.write(folder + os.sep + 'cutout.kml')
			#ET.dump(tree)
		#print(values['-N-'], values['-O-'], values['-SIZE-'], folder)
window.close()