import myClass

# myScreen = myClass.Arduino("/dev/ttyACM0",9600)
# mySand = myClass.Arduino("/dev/ttyACM1",115200)

from arduinoFile import toggle_usb_power

toggle_usb_power("1-1",1,"off")
toggle_usb_power("1-1",2,"off")
toggle_usb_power("1-1",3,"off")
toggle_usb_power("1-1",4,"off")