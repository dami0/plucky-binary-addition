#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.vector import Vector


class Vertical(Widget):
  '''
  This is for the level design. A vertical wall, width 10 and definable
  placement as well as length.
  '''
  def Vert(self, xp, yp, w_height):
    self.l = [xp - 10, yp - w_height/2, xp - 10, yp + w_height/2]
    self.r = [xp + 10, yp - w_height/2, xp + 10, yp + w_height/2]
    self.size = 20, w_height
    with self.canvas:
      Color(*(0, 1, 1, .5), mode='rgba')
      Line(points=[xp, yp - w_height/2, xp, yp + w_height/2], width=10, cap='none')
      self.center_x = xp; self.center_y = yp

  def collision_detect(self, playa):
    if self.collide_widget(playa):
      if playa.velocity_x < 0:
        playa.pos[0] += 90*playa.dt
      elif playa.velocity_x > 0:
        playa.pos[0] -= 90*playa.dt

  def l_detect(self, gun):
    i = Vector.line_intersection(self.l[0:2], self.l[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (i[0] == self.l[0]) and (self.l[1] <= i[1] <= self.l[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.Rifle(gun.s, i)

  def r_detect(self, gun):
    i = Vector.line_intersection(self.r[0:2], self.r[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (i[0] == self.r[0]) and (self.r[1] <= i[1] <= self.r[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.Rifle(gun.s, i)

class Horizontal(Widget):
  '''This is for the level design. A horizontal wall, width 10 and definable
     placement as well as length.'''
  def Hort(self, xp, yp, w_width):
    self.b = [xp - w_width/2, yp - 10, xp + w_width/2, yp - 10]
    self.t = [xp - w_width/2, yp + 10, xp + w_width/2, yp + 10]
    self.size = w_width, 20
    with self.canvas:
      Color(*(0, 1, 1, .5), mode='rgba')
      Line(points=[xp - w_width/2, yp, xp + w_width/2, yp], width=10, cap='none')
      self.center_x = xp; self.center_y = yp
      
  def collision_detect(self, playa):
    if self.collide_widget(playa):
      if playa.velocity_y < 0:
        playa.pos[1] += 90*playa.dt
      elif playa.velocity_y > 0:
        playa.pos[1] -= 90*playa.dt

  def b_detect(self, gun):
    i = Vector.line_intersection(self.b[0:2], self.b[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (self.b[0] <= i[0] <= self.b[2]) and (i[1] == self.b[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.Rifle(gun.s, i)

  def t_detect(self, gun):
    i = Vector.line_intersection(self.t[0:2], self.t[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (self.t[0] <= i[0] <= self.t[2]) and (i[1] == self.t[1]):
      if (a) and (b):
        gun.canvas.clear()
        gun.Rifle(gun.s, i)
