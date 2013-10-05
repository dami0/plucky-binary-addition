#!/usr/bin/python2


def playergen(walls):
  return int((walls[0])[0:4]), int((walls[0])[-4:])

def cleanup(walls):
  walls.pop(0); temp = []
  for line in walls:
    line = line.replace(' ', '0')
    cnt = 0; b = 0
    first = [int(line[0]), int(line[1])]
    while cnt < 4:
      b = cnt*5 + 3
      first.append((int(line[b:(b+4)])))
      cnt += 1
    temp.append(first)
  return temp

def levelgen(walls):
  ent = cleanup(walls)
  walls = []
  for line in ent:
    if not line[0]:
      if not line[1]:
        walls.append(line[2:5] + [0])
      if line[1]:
        walls.append(line[2:5] + [1])
    if line[0]:
      walls.append(line[2:6])
  return walls
