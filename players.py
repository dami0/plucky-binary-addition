#!/usr/bin/env python2

import kivy
kivy.require('1.8.0-dev')

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Player(Widget):
  '''
  This is the player class. It defines movement/position parameters and
  player status variables like health, stamina and quite a few other things
  that describe what's currently going on with them.
  '''
  velocity_x = NumericProperty(0)
  velocity_y = NumericProperty(0)
  velocity = ReferenceListProperty(velocity_x, velocity_y)
  move_speed = 90 #move speed of player blob

  #movement for the update script
  def move(self, dt):
    self.dt = dt
    self.pos = Vector(*self.velocity)*dt + self.pos

  def draws(self):
    self.size = 15, 15
    with self.canvas:
      Color(0.3, 0.4, 0.1)
      Line(ellipse)
      
#    Color:
#      rgb: 0.3, 0.2, 0.1
#    Ellipse:
#      size: 7, 6
#      pos: self.center_x - 3.5, self.center_y - 3
