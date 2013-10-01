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
     that describe the what's currently going on with them.'''
  velocity_x = NumericProperty(0)
  velocity_y = NumericProperty(0)
  velocity = ReferenceListProperty(velocity_x, velocity_y)
  #movement for the update script
  def move(self):
    self.pos = Vector(*self.velocity) + self.pos


class LaserGun(Widget):
  '''This is the LaserGun class. It defines the major characteristics of laser
     weaponry before player/class, skill and equipped modifications modifiers.
     It also contains the base bullet graphics, which in this case travel
     instantly. In reality it's the speed of light, but can you be bothered
     to code in a speed of 30,000,000 metres a second? Didn't think so.'''
  def Bullet(self, xy, x, y):
    #the code for a red line, because c'mon, it's a lazor!
    with self.canvas:
      Color(*(1, 0, 0, .8), mode='rgba')
      Line(points=[xy[0], xy[1], x, y], width=1)


class Vertical_Wall(Widget):
  '''This is for the level design. Currently I've outsourced this to the KV
     language file.'''
  def Vert(self, xp, yp):
    self.size = 10, 100
    with self.canvas:
      Color(*(0, 1, 1, 1), mode='rgba')
      Line(points=[xp, yp - 50, xp, yp + 50], width=10, cap='none')
      self.center_x = xp; self.center_y = yp

  def collision_detect(self, playa):
    if self.collide_widget(playa):
      print 'Collision!'

class Horizontal_Wall(Widget):
  '''This is for the level design. Currently I've outsourced this to the KV
     language file.'''
  def collision_detect(self, playa):
    if self.collide_widget(playa):
      print 'Collision!'


class WarBackground(Widget): #the root widget, the window maker
  player = ObjectProperty(None) #assign all the stuff to draw, player char.
  w_vert = Vertical_Wall()             #level layout
  W_hort = Horizontal_Wall()
  kcds = dict(zip(['w', 's', 'a', 'd'], [0, 1, 2, 3])) #configurable keybindings
  already_pressed = len(kcds)*[0] #so I can have multiple key presses
  move_speed = 1.5 #move speed of player blob

  def __init__(self, **kwargs): #standard adds for keyboard and things
    super(WarBackground, self).__init__(**kwargs)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def levelgen(self):
    self.add_widget(self.w_vert)
    self.player.center_x = 150; self.player.center_y = 300
    self.w_vert.Vert(150, 150)

  def _keyboard_closed(self):
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #what to do if keys are pressed, extensions of keybindings
    if keycode[1] == 'w' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_y += self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 's' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_y -= self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 'a' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_x -= self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 'd' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.player.velocity_x += self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
      
    return True

  def _on_keyboard_up(self, keyboard, keycode):
    #what to do on key release
    if keycode[1] == 'w':
      self.player.velocity_y -= self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 's':
      self.player.velocity_y += self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 'a':
      self.player.velocity_x += self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 'd':
      self.player.velocity_x -= self.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()

    return True

  def on_touch_down(self, touch): #shoot lazors on click! whooooooooo!
    self.c = LaserGun() #add a gun class for the currently used gun
    self.add_widget(self.c) #draw the lazor
    self.c.Bullet(self.player.center, touch.x, touch.y) #make sure lazor travels right
    Animation(opacity=0.0, d=0.5).start(self.c) #animate it so it dissapears over time

    return True #handle that s**t

  def update(self, dt): #overall game update mechanism
    self.player.move()  #move dat blob

    self.w_vert.collision_detect(self.player)

class WarApp(App): #main app process
  def build(self):
    background = WarBackground() #define for easier to work with
    background.levelgen() #generate player levels
    Clock.schedule_interval(background.update, 1.0/60.0) #one sixtieth of second running speed
    return background #draw the main game!

if __name__ == '__main__':
  WarApp().run()
