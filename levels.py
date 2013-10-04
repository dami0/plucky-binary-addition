#!/usr/bin/python2

import kivy
kivy.require('1.8.0-dev')

from kivy.uix.widget import Widget
from walls import Horizontal, Vertical
from players import PC

class level():

  @classmethod
  def gen():
    vert = []
    hort = []
    i = 0
    PC.center_x = 1250; PC.center_y = 30
    while i < 100:
      vert.append(Vertical())
      hort.append(Horizontal())
      add_widget(vert[i])
      add_widget(hort[i])
      i += 1
    vert[0].Vert(1270, 40, 80)
    hort[0].Hort(1120, 10, 320)
    hort[1].Hort(1260, 70, 80)
    vert[1].Vert(1230, 200, 320)
    hort[2].Hort(1230, 50, 20)
    vert[2].Vert(970, 90, 180)
    hort[3].Hort(1070, 150, 220)
    vert[3].Vert(1170, 160, 40)
    vert[4].Vert(1170, 230, 60)
    vert[5].Vert(1170, 300, 40)
    vert[6].Vert(1070, 230, 180)
    hort[4].Hort(1070, 310, 220)
    vert[7].Vert(970, 230, 60)
    vert[8].Vert(970, 300, 40)
