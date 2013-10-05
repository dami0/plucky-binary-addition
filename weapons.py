#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, Line

class Laser(Widget):
  '''
  This is the LaserGun class. It defines the major characteristics of laser
  weaponry before player/class, skill and equipped modifications modifiers.
  It also contains the base bullet graphics, which in this case travel
  instantly. In reality it's the speed of light, but can you be bothered
  to code in a speed of 30,000,000 metres a second? Didn't think so.
  '''
  def rifle(self, s, e):
    #the code for a red line, because c'mon, it's a lazor!
    self.s = s
    self.e = e
    with self.canvas:
      Color(*(1, 0.1, 0.25, 0.8), mode='rgba')
      Line(points=[s[0], s[1], e[0], e[1]], width=1)
    decay = Animation(opacity=0, d=0.8)
    decay.start(self) #animate it so it dissapears over time
