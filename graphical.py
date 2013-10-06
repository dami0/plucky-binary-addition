#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty


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
      self.center_x = xp; self.center_y = yp

  def collision_detect(self, playa):
    if self.collide_widget(playa):
      if playa.velocity_x < 0:
        playa.pos[0] += 90*playa.dt
      elif playa.velocity_x > 0:
        playa.pos[0] -= 90*playa.dt

  def detect(self, gun):
    i = 0
    if gun.s[0] < self.l[0]:
      i = Vector.segment_intersection(self.l[0:2], self.l[2:4], gun.s, gun.e)
    if gun.s[0] > self.r[0]:
      i = Vector.segment_intersection(self.r[0:2], self.r[2:4], gun.s, gun.e)
    if i: gun.canvas.clear()
    if i: gun.rifle(gun.s, i)

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
      self.center_x = xp; self.center_y = yp
      
  def collision_detect(self, playa):
    if self.collide_widget(playa):
      if playa.velocity_y < 0:
        playa.pos[1] += 90*playa.dt
      elif playa.velocity_y > 0:
        playa.pos[1] -= 90*playa.dt

  def detect(self, gun):
    i = 0
    if gun.s[1] < self.b[1]:
      i = Vector.segment_intersection(self.b[0:2], self.b[2:4], gun.s, gun.e)
    if gun.s[1] > self.t[1]:
      i = Vector.segment_intersection(self.t[0:2], self.t[2:4], gun.s, gun.e)
    if i: gun.canvas.clear()
    if i: gun.rifle(gun.s, i)


class Vdoors(Widget):
  '''
  This is a set of doors that automagically open when the player is near them.
  They also have some glowing lights. This is sci-fi after all.
  '''
  def __init__(self, **kwargs):
    super(Vdoors, self).__init__(**kwargs)
    self.flag = 1
    self.d_height = 10
    self.l1, self.l2 = [0, 0, 0, 0], [0, 0, 0, 0]
    self.l3, self.l4 = [0, 0, 0, 0], [0, 0, 0, 0]

  def draws(self, xp, yp, *args):
    self.xp = xp
    self.bp = yp - 10
    self.tp = yp + 10 
    self.size = 40, 30
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[xp, yp + 10, xp, yp - 10], width=3, cap='none')
      self.center_x = xp; self.center_y = yp
    self.opena = Animation(d_height = 0, d = 0.25, s = .25/20.)
    self.opena.bind(on_progress=self.slide)
    self.closea = Animation(d_height = 10, d = 0.25, s = .25/20.)
    self.closea.bind(on_progress=self.slide)

  def slide(self, *args):
    self.canvas.clear()
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[self.xp, self.tp, self.xp, self.tp - self.d_height], width=3, cap='none')
      Line(points=[self.xp, self.bp, self.xp, self.bp + self.d_height], width=3, cap='none')
    self.l1 = self.xp - 1.5, self.tp, self.xp - 1.5, self.tp - self.d_height
    self.l2 = self.xp + 1.5, self.tp, self.xp + 1.5, self.tp - self.d_height
    self.l3 = self.xp + 1.5, self.bp, self.xp + 1.5, self.bp + self.d_height
    self.l2 = self.xp - 1.5, self.bp, self.xp - 1.5, self.bp + self.d_height

  def collision_detect(self, playa):
    if (self.collide_widget(playa) and self.flag):
      self.flag = 0
      self.opena.start(self)
      print 'opening'
    if not self.collide_widget(playa) and not self.flag:
      self.flag = 1
      self.closea.start(self)
      print 'closing'
    if (self.xp -15 < playa.center_x < self.xp + 15) and playa.center_y <= self.bp + 5:
      playa.pos[1] += 90*playa.dt
    if (self.xp -15 < playa.center_x < self.xp + 15) and playa.center_y >= self.tp - 5:
      playa.pos[1] -= 90*playa.dt

  def detect(self, gun):
    i = 0
    if gun.s[0] < self.l1[0]:
      i = Vector.segment_intersection(self.l1[0:2], self.l1[2:4], gun.s, gun.e)
    if gun.s[0] > self.l1[0]:
      i = Vector.segment_intersection(self.l2[0:2], self.l2[2:4], gun.s, gun.e)
    if gun.s[0] < self.l1[0]:
      i = Vector.segment_intersection(self.l3[0:2], self.l3[2:4], gun.s, gun.e)
    if gun.s[0] > self.l1[0]:
      i = Vector.segment_intersection(self.l4[0:2], self.l4[2:4], gun.s, gun.e)
    if i: gun.canvas.clear()
    if i: gun.rifle(gun.s, i)


class Hdoors(Widget):
  '''
  This is a set of doors that automagically open when the player is near them.
  They also have some glowing lights. This is sci-fi after all.
  '''
  def __init__(self, **kwargs):
    super(Vdoors, self).__init__(**kwargs)
    self.flag = 1
    self.d_width = 10

  def draws(self, xp, yp, *args):
    self.yp = yp
    self.lp = xp - 10
    self.rp = xp + 10
    self.size = 40, 30
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[xp + 10, yp, xp - 10, yp], width=3, cap='none')
      self.center_x = xp; self.center_y = yp
    self.opena = Animation(d_width = 0, d = 0.25, s = .01)
    self.opena.bind(on_progress=self.slide)
    self.closea = Animation(d_width = 10, d = 0.25, s = .01)
    self.closea.bind(on_progress=self.slide)
    

  def slide(self, *args):
    self.canvas.clear()
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[self.lp, self.yp, self.lp + self.d_width, self.yp], width=3, cap='none')
      Line(points=[self.rp, self.yp, self.rp - self.d_width, self.yp], width=3, cap='none')
    self.l1 = self.lp, self.yp + 1.5, self.lp + self.d_width, self.yp + 1.5
    self.l2 = self.rp, self.yp + 1.5, self.rp - self.d_width, self.yp + 1.5
    self.l3 = self.rp, self.yp - 1.5, self.lp + self.d_width, self.yp - 1.5
    self.l2 = self.lp, self.yp - 1.5, self.rp - self.d_width, self.yp - 1.5



  def collision_detect(self, playa):
    if (self.collide_widget(playa) and self.flag):
      self.flag = 0
      self.opena.start(self)
      print 'opening'
    if not self.collide_widget(playa) and not self.flag:
      self.flag = 1
      self.closea.start(self)
      print 'closing'
    if (self.yp - 10 < playa.center_y < self.yp + 10) and playa.center_x <= self.lp:
      playa.pos[0] += 90*playa.dt
    if (self.yp - 10 < playa.center_y < self.yp + 10) and playa.center_x >= self.lp:
      playa.pos[0] -= 90*playa.dt      

  def detect(self, gun):
    i = 0
    if gun.s[1] > self.l1[1]:
      i1 = Vector.segment_intersection(self.l1[0:2], self.l1[2:4], gun.s, gun.e)
    if gun.s[1] > self.l2[1]:
      i2 = Vector.segment_intersection(self.l2[0:2], self.l2[2:4], gun.s, gun.e)
    if gun.s[1] < self.l3[1]:
      i3 = Vector.segment_intersection(self.l3[0:2], self.l3[2:4], gun.s, gun.e)
    if gun.s[1] < self.l4[1]:
      i4 = Vector.segment_intersection(self.l4[0:2], self.l4[2:4], gun.s, gun.e)
    if i: gun.canvas.clear()
    if i: gun.rifle(gun.s, i)
