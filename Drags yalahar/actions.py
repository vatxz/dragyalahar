import pyautogui as pg
import constants
import keyboard

def eat_food():
    pg.press("F8")
    print("comiendo comida..")
   
def hole_down(should_down):
    if should_down:
       box = pg.locateOnScreen("imgs/cuerdasubir.png", confidence=0.8)
       if box:
           x, y = pg.center(box)
           pg.moveTo(x, y)
           pg.press("f4")
           pg.click()
           pg.sleep(5)

def hole_up(should_up, img_anchor, plus_x, plus_y):
    if should_up:
       box = pg.locateOnScreen(img_anchor, confidence=0.5)
       if box:
           x, y = pg.center(box)
           pg.moveTo(x, y)
           pg.click()
           pg.sleep(5)

def check_status(name, delay, x, y, rgb, button_name):
  print(f"checando {name}...")
  pg.sleep(delay)
  if pg.pixelMatchesColor(x, y, rgb):
    pg.press(button_name)

def check_battle():
    return pg.locateOnScreen("imgs/battle2.png", region=constants.REGION_BATTLE)

def check_anchor():
    box = pg.locateOnScreen("imgs/Anchfloor1.png", confidence=0.8)
    if box:
       pg.moveTo(1893, 12)
       pg.click()
       pg.moveTo(1893, 12)
       pg.click(1105, 550)
       return False
    return True
       
    
