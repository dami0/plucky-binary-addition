#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.animation import Animation


class WarPlayer(Widget):
  '''This is the player class. It defines movement/position parameters and
     player status variables like health, stamina and quite a few other things
     that describe what's currently going on with them.'''
  velocity_x = NumericProperty(0)
  velocity_y = NumericProperty(0)
  velocity = ReferenceListProperty(velocity_x, velocity_y)
  move_speed = 90 #move speed of player blob
  
  #movement for the update script
  def move(self, dt):
    self.dt = dt
    self.pos = Vector(*self.velocity)*dt + self.pos


class LaserGun(Widget):
  '''This is the LaserGun class. It defines the major characteristics of laser
     weaponry before player/class, skill and equipped modifications modifiers.
     It also contains the base bullet graphics, which in this case travel
     instantly. In reality it's the speed of light, but can you be bothered
     to code in a speed of 30,000,000 metres a second? Didn't think so.'''
  def Bullet(self, s, e):
    #the code for a red line, because c'mon, it's a lazor!
    self.s = s
    self.e = e
    with self.canvas:
      Color(*(1, 0.1, 0.25, 0.8), mode='rgba')
      Line(points=[s[0], s[1], e[0], e[1]], width=1)
    decay = Animation(opacity=0, d=0.8)
    decay.start(self) #animate it so it dissapears over time


class Vertical_Wall(Widget):
  '''This is for the level design. A vertical wall, width 10 and definable
     placement as well as length.'''
  def Vert(self, xp, yp, w_height):
    self.l = [xp - 10, yp - w_height/2, xp - 10, yp + w_height/2]
    self.r = [xp + 10, yp - w_height/2, xp + 10, yp + w_height/2]
    self.size = 18, w_height
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
        gun.Bullet(gun.s, i)

  def r_detect(self, gun):
    i = Vector.line_intersection(self.r[0:2], self.r[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (i[0] == self.r[0]) and (self.r[1] <= i[1] <= self.r[3]):
      if (a) and (b):
        gun.canvas.clear()
        gun.Bullet(gun.s, i)

class Horizontal_Wall(Widget):
  '''This is for the level design. A horizontal wall, width 10 and definable
     placement as well as length.'''
  def Hort(self, xp, yp, w_width):
    self.b = [xp - w_width/2, yp - 10, xp + w_width/2, yp - 10]
    self.t = [xp - w_width/2, yp + 10, xp + w_width/2, yp + 10]
    self.size = w_width, 18
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
        gun.Bullet(gun.s, i)

  def t_detect(self, gun):
    i = Vector.line_intersection(self.t[0:2], self.t[2:4], gun.s, gun.e)
    a = gun.s[0] <= i[0] <= gun.e[0] or gun.e[0] <= i[0] <= gun.s[0]
    b = gun.s[1] <= i[1] <= gun.e[1] or gun.e[1] <= i[1] <= gun.s[1]
    if (self.t[0] <= i[0] <= self.t[2]) and (i[1] == self.t[1]):
      if (a) and (b):
        gun.canvas.clear()
        gun.Bullet(gun.s, i)


class WarBackground(Widget): #the root widget, the window maker
  player = ObjectProperty(None) #assign all the stuff to draw, player char.
  w_vert = []                   #level layout
  w_hort = []
  kcds = dict(zip(['w', 's', 'a', 'd'], [0, 1, 2, 3])) #configurable keybindings
  already_pressed = len(kcds)*[0] #so I can have multiple key presses
  c = []

  def __init__(self, **kwargs): #standard adds for keyboard and things
    super(WarBackground, self).__init__(**kwargs)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def levelgen(self):
    self.i = 0
    self.player.center_x = 1250; self.player.center_y = 30
    while self.i < 2:
      self.w_vert.append(Vertical_Wall())
      self.w_hort.append(Horizontal_Wall())
      self.add_widget(self.w_vert[self.i])
      self.add_widget(self.w_hort[self.i])
      self.i += 1
    self.w_vert[0].Vert(1270, 65, 130)
    self.w_hort[0].Hort(1120, 10, 320)
    self.w_hort[1].Hort(1240, 120, 80)
    self.w_vert[1].Vert(1210, 200, 320)

  def _keyboard_closed(self):
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #what to do if keys are pressed, extensions of keybindings
    if keycode[1] == 'w' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_y += self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 's' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_y -= self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 'a' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_x -= self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 'd' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_x += self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
      
    return True

  def _on_keyboard_up(self, keyboard, keycode):
    #what to do on key release
    if keycode[1] == 'w' and self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_y -= self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 's' and self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_y += self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 'a' and self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_x += self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 'd' and self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_x -= self.player.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()

    return True

  def on_touch_down(self, touch): #shoot lazors on click! whooooooooo!
    index = len(self.c)
    self.c.append(LaserGun()) #add a gun class for the currently used gun
    self.add_widget(self.c[index]) #draw the lazor
    self.c[index].Bullet(self.player.center, [touch.x, touch.y]) #make sure lazor travels right
    self.w_vert.l_detect(self.c[index])
    self.w_vert.r_detect(self.c[index])
    self.w_hort.b_detect(self.c[index])
    self.w_hort.t_detect(self.c[index])
    Clock.schedule_once(self.clean_call, 1)
    return True #handle that s**t

  def clean_call(self, dt):
    self.remove_widget(self.c[0])
    self.c.pop(0)

  def update(self, dt): #overall game update mechanism
    self.player.move(dt)  #move dat blob

    self.i = 0
    while self.i < 2:
      self.w_vert[self.i].collision_detect(self.player)
      self.w_hort[self.i].collision_detect(self.player)
      self.i += 1
      

class WarApp(App): #main app process
  def build(self):
    background = WarBackground() #define for easier to work with
    background.levelgen() #generate player levels
    Clock.schedule_interval(background.update, 1.0/60.0) #one sixtieth of second running speed
    return background #draw the main game!

if __name__ == '__main__':
  WarApp().run()
