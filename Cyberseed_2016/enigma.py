#!/usr/bin/env python
# Author: pr0n1s

from pycipher.enigma import Enigma
import multiprocessing as mp
import itertools, sys

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
cipher = 'GCXSSBPPIUDNWXJZGIICUEFYGISQOCGLLGMMKYHJ'
string = 'BELADEN'
plugs = 'AEGINVXZ'
display = ('G','Q','T')
reflector = 'B'
rotors = [(1,2,3), (1,3,2), (2,3,1), (2,1,3), (3,2,1), (3,1,2)]
stecks = [('B','F'), ('C','M'), ('D','R'), ('H','Q'), ('J','K'),
	  ('L','U'), ('O','Y'), ('P','W'), ('S','T')]

def gen_settings(lst):
  last_steck = list(itertools.permutations(plugs, 2))
  rings = list(itertools.permutations(alpha, 3))

  print("[*] Generating settings")
  for plug in last_steck:
    steck = stecks + [plug]
    for rotor in rotors:
      for ring in rings:
	lst.append([display, rotor, reflector, ring, steck])
  print("[*] Settings generated: %s"%len(lst))
  return lst

def dowork(settings):
  for setting in settings:
    enc_key = Enigma(setting[0], setting[1], setting[2], setting[3], setting[4])
    dec_key = enc_key.encipher('UKJ')
    enc = Enigma(dec_key, setting[1], setting[2], setting[3], setting[4])
    pt = enc.decipher(cipher)
    if string in pt:
      fh = open('pt.txt', 'w')
      fh.write("\nSettings:\n\tKey: %s\n\tRotors: %s"%dec_key, setting[1] +
	       "\n\tReflector: %s\n\tRings: %s"%setting[2], setting[3] + 
	       "\n\tSteckers: %s\n\tMessage: %s\n"%setting[4], pt)
      fh.close()
      break
  return pt

def quit(arg):
  print("Message found: %s"%arg)
  p.terminate()

def chop_suey(size, lst):
  return [lst[x:x+len(lst)//size] for x in xrange(0, len(lst), len(lst)//size)]

def main():
  if len(sys.argv) < 2:
    print("[*] Usage: %s <num of processes>"%sys.argv[0])
    sys.exit(1)
  lst = []
  settings = gen_settings(lst)
  split = chop_suey(int(sys.argv[1]), settings)
  print("[*] Lists: %s"%len(split) + 
	"\n[*] Size/List: %s"%str(len(settings)//int(sys.argv[1])))
  p = mp.Pool(int(sys.argv[1]))
  try:  
    for splice in split:
      p.apply_async(dowork, args=(splice,), callback=quit)
  except Exception as e:
    pass
  p.close()
  p.join()

if __name__ == '__main__':
  main()
