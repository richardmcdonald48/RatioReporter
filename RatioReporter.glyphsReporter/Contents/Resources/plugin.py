# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from __future__ import division, print_function, unicode_literals
import objc, math
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSLineCapStyleRound

class RatioReporter(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Ratios',
			'de': 'Verhältnisse',
			'fr': 'proportions',
			'es': 'proporciones',
			'pt': 'proporçiões',
			})

	@objc.python_method
	def conditionsAreMetForDrawing(self):
		"""
		Don't activate if text or pan (hand) tool are active.
		"""
		currentController = self.controller.view().window().windowController()
		if currentController:
			tool = currentController.toolDrawDelegate()
			textToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolText") )
			handToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolHand") )
			if not textToolIsActive and not handToolIsActive: 
				return True
		return False

	@objc.python_method
	def foreground(self, thisLayer):
		selection = [item for item in thisLayer.selection if type(item)==GSNode]
		if len(selection) > 1 and self.getScale() > 0.15 and self.conditionsAreMetForDrawing():
			firstPos = selection[0].position
			lastPos = selection[-1].position

			#specify x and y
			x = int(abs(firstPos.x - lastPos.x))
			y = int(abs(firstPos.y - lastPos.y))

			#calculate greatest common denomenator
			denom = (math.gcd(x, y))

			#divide x and y by greatest common denomenator
			xRatio = int(x/denom)
			yRatio = int(y/denom)

			#format output
			ratio = f"{xRatio}:{yRatio}"
			
			highlightColor = NSColor.blueColor().colorWithAlphaComponent_(0.6)
			highlightColor.set()
			line = NSBezierPath.alloc().init()
			line.moveToPoint_(firstPos)
			line.lineToPoint_(lastPos)
			line.setLineWidth_( 5.0 * self.getScale() ** -0.9 )
			line.setLineCapStyle_(NSLineCapStyleRound)
			line.stroke()
			
			textColor = NSColor.textColor().blendedColorWithFraction_ofColor_(0.3, highlightColor)
			middle = scalePoint(addPoints(firstPos, lastPos), 0.5)
			self.drawTextAtPoint(ratio, middle, fontSize=16, fontColor=textColor, align="bottomcenter")

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
