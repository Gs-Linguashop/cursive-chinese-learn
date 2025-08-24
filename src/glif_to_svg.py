import sys
import argparse
from defcon import Font
from fontTools.pens.svgPathPen import SVGPathPen
from xml.etree.ElementTree import Element, SubElement, tostring

def load_ufo_glyphs(ufo_path):
	font = Font(ufo_path)
	return font

def glyph_to_svg_path(glyph, y_shift=0):
	pen = SVGPathPen(glyph.font)
	glyph.draw(pen)
	path_data = pen.getCommands()
	if y_shift != 0:
		# Apply vertical shift to all path commands
		import re
		def shift(match):
			x, y = float(match.group(1)), float(match.group(2)) + y_shift
			return f"{x} {y}"
		path_data = re.sub(r'([-\d\.]+)\s+([-\d\.]+)', shift, path_data)
	return path_data

def string_to_svg(font, text):
	svg = Element('svg', xmlns="http://www.w3.org/2000/svg")
	x_cursor = 0
	ascender = font.info.ascender if font.info.ascender is not None else 1000
	for char in text:
		codepoint = ord(char)
		glyph_name = None
		for glyph in font:
			if codepoint in glyph.unicodes:
				glyph_name = glyph.name
				break
		if not glyph_name:
			continue
		glyph = font[glyph_name]
		path_data = glyph_to_svg_path(glyph)
		# Reflect y: scaleY(-1) and translateY(-descender)
		path = SubElement(svg, 'path', d=path_data)
		path.set('transform', f'translate({x_cursor}, {ascender}) scale(1,-1)')
		x_cursor += glyph.width
	svg.set('width', str(x_cursor))
	svg.set('height', '1000')
	return tostring(svg, encoding='unicode')

def main():
	parser = argparse.ArgumentParser(description="Convert UFO glyphs to SVG for a string.")
	parser.add_argument('ufo_path', help='Path to UFO font folder')
	parser.add_argument('text', help='Unicode string to render')
	parser.add_argument('output_svg', help='Output SVG file')
	args = parser.parse_args()

	font = load_ufo_glyphs(args.ufo_path)
	svg_content = string_to_svg(font, args.text)
	with open(args.output_svg, 'w', encoding='utf-8') as f:
		f.write(svg_content)

if __name__ == '__main__':
	main()
	# python3 src/glif_to_svg.py src/JingdianCaoshuHeiti.ufo "草书" output.svg
