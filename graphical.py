#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.clock import Clock


class Vertical(Widget):
  '''
  A vertical wall, width 10 and definable placement as well as length.
  '''
  def draws(self, xp, yp, h):
    self.l = [xp - 10, yp - h/2, xp - 10, yp + h/2]
    self.r = [xp + 10, yp - h/2, xp + 10, yp + h/2]
    self.size = 20, h - 4
    with self.canvas:
      Color(*(0.05, 0.1, 0.05, 1), mode='rgba')
      Line(points=[xp, yp - h/2, xp, yp + h/2], width=10, cap='none')
      Color(*(0.2, 0.2, 0.2, 1), mode='rgba')
      Line(points=[xp, yp - h/2, xp, yp + h/2], width=3, cap='none')
      Color(*(0.1, 0.1, 1, 1), mode='rgba')
      Line(points=[xp + 11, yp - h/2, xp + 11, yp + h/2], width=1, cap='none', dash_length = 20, dash_offset = 20)
      Line(points=[xp - 11, yp - h/2, xp - 11, yp + h/2], width=1, cap='none', dash_length = 20, dash_offset = 20)
      self.center_x = xp; self.center_y = yp
    self.col_check = 1

  def collision_detect(self, playa):
    if self.collide_widget(playa):
      if playa.velocity_x < 0:
        playa.pos[0] += 90*playa.dt
      elif playa.velocity_x > 0:
        playa.pos[0] -= 90*playa.dt

  def detect1(self, gun):
    i = Vector.line_intersection(self.l[0:2], self.l[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (i[0] == self.l[0]) and (self.l[1] <= i[1] <= self.l[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.rifle(gun.s, i)

  def detect2(self, gun):
    i = Vector.line_intersection(self.r[0:2], self.r[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (i[0] == self.r[0]) and (self.r[1] <= i[1] <= self.r[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.rifle(gun.s, i)

class Horizontal(Widget):
  '''
  A horizontal wall, width 10 and definable placement as well as length.
  '''
  def draws(self, xp, yp, w):
    self.b = [xp - w/2, yp - 10, xp + w/2, yp - 10]
    self.t = [xp - w/2, yp + 10, xp + w/2, yp + 10]
    self.size = w - 2, 20
    with self.canvas:
      Color(*(0.05, 0.1, 0.05, 1), mode='rgba')
      Line(points=[xp - w/2, yp, xp + w/2, yp], width=10, cap='none')
      Color(*(0.2, 0.2, 0.2, 1), mode='rgba')
      Line(points=[xp - w/2, yp, xp + w/2, yp], width=3, cap='none')
      Color(*(0.1, 0.1, 1, 1), mode='rgba')
      Line(points=[xp - w/2, yp + 11, xp + w/2, yp + 11], width=1, cap='none', dash_length = 20, dash_offset = 20)
      Line(points=[xp - w/2, yp - 11, xp + w/2, yp - 11], width=1, cap='none', dash_length = 20, dash_offset = 20)
      self.center_x = xp; self.center_y = yp
    self.col_check = 1
      
  def collision_detect(self, playa):
    if self.collide_widget(playa):
      if playa.velocity_y < 0:
        playa.pos[1] += 90*playa.dt
      elif playa.velocity_y > 0:
        playa.pos[1] -= 90*playa.dt

  def detect1(self, gun):
    i = Vector.line_intersection(self.b[0:2], self.b[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (self.b[0] <= i[0] <= self.b[2]) and (i[1] == self.b[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.rifle(gun.s, i)

  def detect2(self, gun):
    i = Vector.line_intersection(self.t[0:2], self.t[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (self.t[0] <= i[0] <= self.t[2]) and (i[1] == self.t[1]):
      if (a) and (b):
        gun.canvas.clear()
        gun.rifle(gun.s, i)

class Vdoors(Widget):
  '''
  This is a set of doors that automagically open when the player is near them.
  They also have some glowing lights. This is sci-fi after all.
  '''
  def __init__(self, **kwargs):
    super(Vdoors, self).__init__(**kwargs)
    self.flag = 1
    self.p = 9
    self.col_check = 1

  def draws(self, xp, yp, s):
    ty = yp + 10; by = ty - s
    self.xp = xp; self.yp = yp
    self.size = 30, 10
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[xp, by, xp, ty], width=3, cap='none')
      self.center_x = xp; self.center_y = yp

  def draws2(self, xp, yp, s):
    by = yp - 10; ty = by + s
    self.size = 40, 20
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[xp, ty, xp, by], width=3, cap='none')
      self.center_x = xp; self.center_y = yp

  def collision_detect(self, playa):
    if (self.collide_widget(playa) and self.flag):
      self.flag = 0
      self.col_check = 0
      self.p = 10
      Clock.schedule_once(self.opencall, 0)
      print 'opening'
    if not self.collide_widget(playa) and not self.flag:
      self.flag = 1
      self.col_check = 0
      self.p = 0
      Clock.schedule_once(self.closecall, 0)
      print 'closing'

  def opencall(self, *args):
    opena = Animation(d = 0.25, s = .25/10.)
    opena.bind(on_progress=self.slideo)
    opena.bind(on_complete=self.no_col)
    opena.start(self)

  def closecall(self, *args):
    closea = Animation(d = 0.25, s = .25/10.)
    closea.bind(on_progress=self.slidec)
    closea.bind(on_complete=self.no_col)
    closea.start(self)

  def no_col(self, *args):
    self.col_check = 1

  def slideo(self, *args):
    self.canvas.clear()
    self.draws(self.xp, self.yp, self.p)
    self.draws2(self.xp, self.yp, self.p)
    self.p -= 1

  def slidec(self, *args):
    self.canvas.clear()
    self.draws(self.xp, self.yp, self.p)
    self.draws2(self.xp, self.yp, self.p)
    self.p += 1


#class Hdoors(Widget):
