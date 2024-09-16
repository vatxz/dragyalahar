import pyautogui as pg
import actions
import constants
import json
from pynput.keyboard import Listener
from pynput import keyboard    
import threading
import my_thread
from my_thread import ThreadGroup
import time
 
def kill_monster():
    while actions.check_battle() is None:
        print("Matando monstruos")
        if event_th.is_set():
            return
        pg.press("space")
        
        # Iniciar rotación de teclas mientras la imagen esté presente
        while pg.locateOnScreen("imgs/redtarget.png", confidence=0.6, region=constants.REGION_BATTLE) is not None:
            if event_th.is_set():
                return
            print("Esperando monstruo morir")
            
            # Presiona F1, F2, F3 en un bucle con 1 segundo de intervalo
            time.sleep(1)
            pg.press("f2")
            print("Presionando F2")
            time.sleep(2)
            # Verificar si la imagen aún está presente
            if pg.locateOnScreen("imgs/redtarget.png", confidence=0.6, region=constants.REGION_BATTLE) is None:
                break
            pg.press("f5")
            print("Presionando F5")
            time.sleep(2)
            # Verificar si la imagen aún está presente
            if pg.locateOnScreen("imgs/redtarget.png", confidence=0.6, region=constants.REGION_BATTLE) is None:
                break
            pg.press("f7")
            print("Presionando F7")
            time.sleep(1)
        
        print("Buscando monstruo")

        

def get_loot():
    # Localiza todas las instancias de la imagen "wasp.png" en la pantalla dentro de la región especificada
    loot = pg.locateAllOnScreen("imgs/dragon.png", confidence=0.9, region=constants.RADIO_LOOT)
    
    # Itera a través de cada cuadro delimitador encontrado
    for box in loot:
        # Calcula el centro del cuadro delimitador
        x, y = pg.center(box)
        
        # Mueve el ratón al centro del cuadro delimitador
        pg.moveTo(x, y)
        
        # Realiza un clic derecho
        pg.click(button="right")
        
        # Añadir una pequeña pausa para asegurarse de que la acción se ha completado
        time.sleep(0.5)
        
        # Busca nuevamente la misma imagen
        sub_loot = pg.locateAllOnScreen("imgs/dragon.png", confidence=0.9, region=constants.RADIO_LOOT)
        for sub_box in sub_loot:
            sub_x, sub_y = pg.center(sub_box)
            pg.moveTo(sub_x, sub_y)
            pg.press('f10')
            pg.click(button='left')
            
            # Añadir una pequeña pausa para asegurarse de que la acción se ha completado
            time.sleep(0.5)
            
            # Vuelve a buscar la imagen principal para repetir el ciclo
            break

if __name__ == "__main__":
    get_loot()

def go_to_flag(path, wait):
    flag = pg.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pg.center(flag)
        if event_th.is_set():
            return
        pg.moveTo(x, y)
        pg.click()
        pg.sleep(wait)

def check_player_position():
    return pg.locateOnScreen("imgs/player.png", confidence=0.6, region=constants.REGION_MAP)

def run():
    with open(f"{constants.FOLDER_NAME}/infos.json", "r") as file:
        data = json.loads(file.read())
    while not event_th.is_set():
        for item in data:
            if not actions.check_anchor():
                return
            if event_th.is_set():
                return
            kill_monster()
            if event_th.is_set():
                return
            pg.sleep(0.5)
            get_loot()
            if event_th.is_set():
                return
            go_to_flag(item["path"], item["wait"])
            if event_th.is_set():
                return
            if check_player_position():
               kill_monster()
               if event_th.is_set():
                   return
               pg.sleep(0.5)
               get_loot()
               if event_th.is_set():
                   return
               go_to_flag(item["path"], item["wait"])
            actions.eat_food()
            actions.hole_down(item["down_hole"])
            if event_th.is_set():
                return
            actions.hole_up(item["up_hole"], f"{constants.FOLDER_NAME}/Anchfloor3.png", 130, 130)
            actions.hole_up(item["up_hole"], f"{constants.FOLDER_NAME}/Anchfloor2.png", 430, 130)

def key_code(key, th_group):
    if key == keyboard.Key.esc:
        event_th.set()
        th_group.stop()
        return False
    if key == keyboard.Key.delete:
           th_group.start()
           th_run.start()

global event_th
event_th = threading.Event()
th_run = threading.Thread(target=run)

th_full_mana = my_thread.MyThread(lambda: actions.check_status("mana", 5, *constants.POSITION_MANA_FULL, constants.COLOR_MANA, "F6"))
th_check_life = my_thread.MyThread(lambda: actions.check_status("vida", 2, *constants.POSITION_LIFE, constants.COLOR_GREEN_LIFE, "F3"))

group_thread = my_thread.ThreadGroup([th_full_mana, th_check_life])

with Listener(on_press=lambda key: key_code(key, group_thread)) as listener:
    listener.join()