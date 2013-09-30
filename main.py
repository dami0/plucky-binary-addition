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
  velocity_x = NumericProperty(0)
  velocity_y = NumericProperty(0)
  velocity = ReferenceListProperty(velocity_x, velocity_y)

  def move(self):
    self.pos = Vector(*self.velocity) + self.pos


class LaserGun(Widget):  
  def Bullet(self, xy, x, y):
    with self.canvas:
      Color(*(1, 0, 0, .8), mode='rgba')
      Line(points=[xy[0], xy[1], x, y], width=1)


class Levels(Widget):
  def move(self):
    self.pos = Vector(*self.velocity) + self.pos
    self.canvas.clear()
    self.Rooms()

  def Rooms(self, x, y):
    with self.canvas:
      Color(*(1, 1, 1, 1), mode='rgba')
      Line(rectangle=(x, y, 50, 100), width=5)

class WarBackground(Widget):
  player = ObjectProperty(None)
  layout = Levels()
  kcds = dict(zip(['w', 's', 'a', 'd'], [0, 1, 2, 3]))
  already_pressed = len(kcds)*[0]
  move_speed = 1.5

  def __init__(self, **kwargs):
    super(WarBackground, self).__init__(**kwargs)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def levelgen(self):
    self.add_widget(self.layout)
    self.layout.Rooms(self.player.pos[0], self.player.pos[1])

  def _keyboard_closed(self):
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    
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

  def on_touch_down(self, touch):
    self.c = LaserGun()
    self.add_widget(self.c)
    self.c.Bullet(self.player.center, touch.x, touch.y)
    Animation(opacity=0.0, d=0.5).start(self.c)

    return True

  def update(self, dt):
    self.player.move()

class WarApp(App):
  def build(self):
    background = WarBackground()
    background.levelgen()
    Clock.schedule_interval(background.update, 1.0/60.0)
    return background

if __name__ == '__main__':
  WarApp().run()
