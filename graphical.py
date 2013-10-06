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
    self.size = 20, h - 2
    with self.canvas:
      Color(*(0.05, 0.1, 0.05, 1), mode='rgba')
      Line(points=[xp, yp - h/2, xp, yp + h/2], width=10, cap='none')
      Color(*(0.4, 0.2, 0.2, 1), mode='rgba')
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
      Color(*(0.4, 0.2, 0.2, 1), mode='rgba')
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
    self.d_height = 10; self.sl = 10
    self.col = [0, 0, 0, 0]

  def draws(self, xp, yp, *args):
    if args[0] != 10: self.d_height, self.sl = args[0]/2, args[0]/2
    self.xp = xp
    self.bp = yp - 10
    self.tp = yp + 10 
    self.size = 30, 2*self.d_height + 2
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[xp, yp + 10, xp, yp - 10], width=3, cap='none')
      self.center_x = xp; self.center_y = yp
      Color(*(0, 1, 0, 1), mode='rgba')
      Line(circle=[self.xp + 3, self.tp, 1], mode='rgba', width=1)
      Line(circle=[self.xp - 3, self.tp, 1], mode='rgba', width=1)
      Line(circle=[self.xp + 3, self.bp, 1], mode='rgba', width=1)
      Line(circle=[self.xp - 3, self.bp, 1], mode='rgba', width=1)

    self.opena = Animation(d_height = 0, d = 0.1)
    self.opena.bind(on_progress=self.slide)
    self.opena.bind(on_complete=self.draw)
    self.closea = Animation(d_height = 10, d = 0.1)
    self.closea.bind(on_progress=self.slide)
    self.closea.bind(on_complete=self.draw)
    self.col = self.xp, self.tp, self.xp, self.tp - 2*self.d_height

  def slide(self, *args):
    self.canvas.clear()
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[self.xp, self.tp, self.xp, self.tp - self.d_height], width=3, cap='none')
      Line(points=[self.xp, self.bp, self.xp, self.bp + self.d_height], width=3, cap='none')
      Color(*(0, 0, 1, 1), mode='rgba')
      Line(circle=[self.xp + 3, self.tp, 1], mode='rgba', width=1)
      Line(circle=[self.xp - 3, self.tp, 1], mode='rgba', width=1)
      Line(circle=[self.xp + 3, self.bp, 1], mode='rgba', width=1)
      Line(circle=[self.xp - 3, self.bp, 1], mode='rgba', width=1)

  def draw(self, *args):
    with self.canvas:
      Color(*(0, 1, 0, 1), mode='rgba')
      Line(circle=[self.xp + 3, self.tp, 1], mode='rgba', width=1)
      Line(circle=[self.xp - 3, self.tp, 1], mode='rgba', width=1)
      Line(circle=[self.xp + 3, self.bp, 1], mode='rgba', width=1)
      Line(circle=[self.xp - 3, self.bp, 1], mode='rgba', width=1)

  def collision_detect(self, playa):
    if (self.collide_widget(playa) and self.flag):
      self.flag = 0
      self.opena.start(self)
    if not self.collide_widget(playa) and not self.flag:
      self.flag = 1
      self.closea.start(self)
    if (self.xp - 20 < playa.center_x < self.xp + 20) and (self. bp <= playa.center_y <= self.bp + 5):
      playa.pos[1] += 90*playa.dt
    if (self.xp - 20 < playa.center_x < self.xp + 20) and (self. tp >= playa.center_y >= self.tp - 5):
      playa.pos[1] -= 90*playa.dt

  def detect(self, gun):
    i = 0
    i = Vector.segment_intersection(self.col[0:2], self.col[2:4], gun.s, gun.e)
    if i and self.flag:
      gun.canvas.clear()
      gun.rifle(gun.s, i)


class Hdoors(Widget):
  '''
  This is a set of doors that automagically open when the player is near them.
  They also have some glowing lights. This is sci-fi after all.
  '''
  def __init__(self, **kwargs):
    super(Hdoors, self).__init__(**kwargs)
    self.flag = 1
    self.d_width = 10; self.sl = 10
    self.col = [0, 0, 0, 0]

  def draws(self, xp, yp, *args):
    if len(args) > 0: self.d_width, self.sl = args[0]/2, args[0]/2
    self.yp = yp
    self.lp = xp - self.d_width
    self.rp = xp + self.d_width
    self.size = 2*self.d_width + 2, 30
    self.canvas.clear()
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[xp + self.d_width, yp, xp - self.d_width, yp], width=3, cap='none')
      self.center_x = xp; self.center_y = yp
      Color(*(0, 1, 0, 1), mode='rgba')
      Line(circle=[self.lp, self.yp + 3, 1], mode='rgba', width=1)
      Line(circle=[self.lp, self.yp - 3, 1], mode='rgba', width=1)
      Line(circle=[self.rp, self.yp + 3, 1], mode='rgba', width=1)
      Line(circle=[self.rp, self.yp - 3, 1], mode='rgba', width=1)
    
    self.opena = Animation(d_width = 0, d = 0.1)
    self.opena.bind(on_progress=self.slide)
    self.opena.bind(on_complete=self.draw)
    self.closea = Animation(d_width = self.sl, d = 0.1)
    self.closea.bind(on_progress=self.slide)
    self.closea.bind(on_complete=self.draw)
    self.col = self.lp, self.yp + 1.5, self.lp + 2*self.d_width, self.yp + 1.5

  def draw(self, *args):
    with self.canvas:
      Color(*(0, 1, 0, 1), mode='rgba')
      Line(circle=[self.lp, self.yp + 3, 1], mode='rgba', width=1)
      Line(circle=[self.lp, self.yp - 3, 1], mode='rgba', width=1)
      Line(circle=[self.rp, self.yp + 3, 1], mode='rgba', width=1)
      Line(circle=[self.rp, self.yp - 3, 1], mode='rgba', width=1)

  def slide(self, *args):
    self.canvas.clear()
    with self.canvas:
      Color(*(1, 0.3, 0.2, 1), mode='rgba')
      Line(points=[self.lp, self.yp, self.lp + self.d_width, self.yp], width=3, cap='none')
      Line(points=[self.rp, self.yp, self.rp - self.d_width, self.yp], width=3, cap='none')
      Color(*(0, 0, 1, 1), mode='rgba')
      Line(circle=[self.lp, self.yp + 3, 1], mode='rgba', width=1)
      Line(circle=[self.lp, self.yp - 3, 1], mode='rgba', width=1)
      Line(circle=[self.rp, self.yp + 3, 1], mode='rgba', width=1)
      Line(circle=[self.rp, self.yp - 3, 1], mode='rgba', width=1)

  def collision_detect(self, playa):
    if (self.collide_widget(playa) and self.flag):
      self.flag = 0
      self.opena.start(self)
    if not self.collide_widget(playa) and not self.flag:
      self.flag = 1
      self.closea.start(self)
    if (self.yp - 10 < playa.center_y < self.yp + 10) and (self.lp <= playa.center_x <= self.lp + 5):
      playa.pos[0] += 90*playa.dt
    if (self.yp - 10 < playa.center_y < self.yp + 10) and (self.lp >= playa.center_x >= self.lp - 5):
      playa.pos[0] -= 90*playa.dt      

  def detect(self, gun):
    i = 0
    i = Vector.segment_intersection(self.col[0:2], self.col[2:4], gun.s, gun.e)
    if i and self.flag:
      gun.canvas.clear()
      gun.rifle(gun.s, i)

class Alight(Widget):
  '''
  Status light, illuminates brightly but not far.
  '''
  def draws(self, xp, yp, arg):
    if arg == 0:
      self.a = [1., 0., 0.]
    if arg == 1:
      self.a = [0., 1., 0.]
    if arg == 2:
      self.a = [0., 0., 1.]
    if arg == 3:
      self.a = [1., 1., 0.]
    self.center = xp, yp
    self.light(xp, yp)

  def light(self, x, y):
    with self.canvas:
      Color(*(self.a + [1.]), mode='rgba')
      Line(circle=[x, y, 1], width=1.5, cap='none')
    i = 3.
    while i < 20.:
      with self.canvas:
        Color(*(self.a + [(0.15**(i/30.))**4]), mode='rgba')
        print self.a + [i]
        Line(circle=[x, y, 2*(i - 1)], width=1.7, cap='none')
        i += 0.5

  def collision_detect(*args): pass

  def detect(*args): pass
