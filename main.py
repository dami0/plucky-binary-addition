#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from players import Player
from weapons import Laser
from walls import Horizontal, Vertical
from levels import playergen, levelgen


class WarBackground(Widget): #the root widget, the window maker
  pc = ObjectProperty(None) #assign all the stuff to draw, pc char.
  kcds = dict(zip(['w', 's', 'a', 'd'], [0, 1, 2, 3])) #configurable keybindings
  already_pressed = len(kcds)*[0] #so I can have multiple key presses
  c = []
  levelstuff = [Vertical(), Horizontal()]
  levelparts = []

  def __init__(self, **kwargs): #standard adds for keyboard and things
    super(WarBackground, self).__init__(**kwargs)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def _keyboard_closed(self):
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #what to do if keys are pressed, extensions of keybindings
    if keycode[1] == 'w' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_y += self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 's' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_y -= self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 'a' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_x -= self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
  
    if keycode[1] == 'd' and not self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_x += self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 1
      keyboard.release()
      
    return True

  def _on_keyboard_up(self, keyboard, keycode):
    #what to do on key release
    if keycode[1] == 'w' and self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_y -= self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 's' and self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_y += self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 'a' and self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_x += self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()
  
    if keycode[1] == 'd' and self.already_pressed[self.kcds[keycode[1]]]:
      self.pc.velocity_x -= self.pc.move_speed
      self.already_pressed[self.kcds[keycode[1]]] = 0
      keyboard.release()

    return True

  def generate(self):
    f = open('level1.dat', 'r')
    readin = f.readlines()

    self.pc.center = playergen(readin)

    llist = levelgen(readin)
    for stuff in llist:
      self.levelparts.append(self.levelstuff[stuff[3]])
      self.add_widget(self.levelparts[-1])
      self.levelparts[-1].wall[stuff[0:3]]

    f.close()    

  def on_touch_down(self, touch): #shoot lazors on click! whooooooooo!
    index = len(self.c)
    self.c.append(Laser()) #add a gun class for the currently used gun
    self.add_widget(self.c[index]) #draw the lazor
    self.c[index].rifle(self.pc.center, [touch.x, touch.y]) #make sure lazor travels right
    self.i = 0
    while self.i < self.v:
      self.vert[self.i].l_detect(self.c[index])
      self.vert[self.i].r_detect(self.c[index])
      self.i += 1
    self.i = 0
    while self.i < self.h:
      self.hort[self.i].b_detect(self.c[index])
      self.hort[self.i].t_detect(self.c[index])
      self.i += 1
    Clock.schedule_once(self.clean_call, 1)
    return True

  def clean_call(self, dt):
    self.remove_widget(self.c[0])
    self.c.pop(0)

  def update(self, dt): #overall game update mechanism
    self.pc.move(dt)  #move dat blob

#    self.i = 0
#    while self.i < self.v:
#      self.vert[self.i].collision_detect(self.pc)
#      self.i += 1
#    self.i = 0
#    while self.i < self.h:
#      self.hort[self.i].collision_detect(self.pc)
#      self.i += 1
      

class WarApp(App): #main app process
  def build(self):
    background = WarBackground() #define for easier to work with
    background.generate()
#    background.levelgen()
    Clock.schedule_interval(background.update, 1.0/60.0) #one sixtieth of second running speed
    return background #draw the main game!

if __name__ == '__main__':
  WarApp().run()
