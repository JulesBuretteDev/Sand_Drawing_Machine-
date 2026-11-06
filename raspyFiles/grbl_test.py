"""Test hardware simple : UNO (GRBL) + CNC shield + moteurs X et Y.

Usage sur la Pi :  python3 grbl_test.py [port]
Port par defaut : l'UNO par son chemin by-id (ttyACM0/1 peut changer, et la Mega
de l'ecran est aussi branchee : ne jamais ouvrir son port).
Fait de petits allers-retours lents sur X puis Y, avec une pause entre chaque
pour toucher les drivers/moteurs. Ctrl+C a tout moment = arret (feed hold + reset).
"""
import sys
import time
import serial

UNO_PORT = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85830303639351D0F171-if00"
PORT = sys.argv[1] if len(sys.argv) > 1 else UNO_PORT
FEED = 300      # mm/min : lent exprès
DIST = 10       # mm par mouvement


def send(com, cmd, show=True):
    com.write((cmd + "\n").encode())
    lines = []
    while True:
        line = com.readline().decode(errors="replace").strip()
        if not line:
            continue
        lines.append(line)
        if line == "ok" or line.startswith("error") or line.startswith("ALARM"):
            break
    if show:
        print(f"> {cmd}\n  " + "\n  ".join(lines))
    return lines


def wait_idle(com):
    while True:
        com.write(b"?")
        status = com.readline().decode(errors="replace").strip()
        if status.startswith("<Idle"):
            return
        time.sleep(0.2)


def move(com, axis, dist):
    send(com, f"G1 {axis}{dist} F{FEED}")
    wait_idle(com)


com = serial.Serial(PORT, 115200, timeout=1)
try:
    com.write(b"\r\n\r\n")
    time.sleep(2)  # l'UNO redemarre a l'ouverture du port
    banner = com.read_all().decode(errors="replace")
    print("Banniere :", banner.strip() or "(rien)")
    if "Grbl" not in banner:
        print("GRBL ne repond pas : mauvais port, ou GRBL pas flashe sur l'UNO.")
        sys.exit(1)

    send(com, "$$")            # affiche les reglages (steps/mm, vitesses...)
    send(com, "$X")            # deverrouille si ALARM
    send(com, "G21")           # millimetres
    send(com, "G91")           # deplacements relatifs

    for axis in ("X", "Y"):
        input(f"\nEntree pour tester {axis} (+{DIST} puis -{DIST} mm)...")
        move(com, axis, DIST)
        move(com, axis, -DIST)
        print(f"{axis} : termine. Le moteur a-t-il tourne dans les deux sens, sans vibrer/claquer ?")

    send(com, "G90")
    print("\nTest fini.")
except KeyboardInterrupt:
    com.write(b"!")            # feed hold
    com.write(b"\x18")         # soft reset
    print("\nArret demande.")
finally:
    com.close()
