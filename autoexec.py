import xbmc
import xbmcaddon
import xbmcgui
import time
import os

pictures_folder = xbmcaddon.Addon().getSetting("pictures_folder")
picture_display_time = int(xbmcaddon.Addon().getSetting("picture_display_time"))
weather_display_time = int(xbmcaddon.Addon().getSetting("weather_display_time"))

# stop if pictures folder not defined
if pictures_folder == "":
    xbmcgui.Dialog().ok("Auto Slideshow", "Pictures folder is not defined. Please check your settings.")
    exit()  # Terminate the script

# wait for Kodi to be fully loaded
while not xbmc.Monitor().waitForAbort(5):
	break

while True:
	for dirpath,_,filenames in os.walk(pictures_folder):
		for file in filenames:
			xbmc.executebuiltin("ShowPicture(" + os.path.abspath(os.path.join(dirpath, file)) + ")")
			time.sleep(picture_display_time)
	
	if xbmcaddon.Addon().getSetting("enable_weather") == 'true':
		xbmc.executebuiltin('Dialog.Close(all,force)')
		xbmc.executebuiltin("ActivateWindow(Weather)")
		time.sleep(weather_display_time)
