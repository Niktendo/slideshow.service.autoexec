import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

pictures_folder = xbmcaddon.Addon().getSetting("pictures_folder")
picture_display_time = int(xbmcaddon.Addon().getSetting("picture_display_time"))
weather_display_time = int(xbmcaddon.Addon().getSetting("weather_display_time"))
enable_weather = xbmcaddon.Addon().getSetting("enable_weather")

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.tga')

def natural_sort_key(s):
    parts = []
    current_chunk = ""
    if not s: return []
    is_numeric = s[0].isdigit()
    for char in s:
        if char.isdigit() == is_numeric:
            current_chunk += char
        else:
            if is_numeric:
                try: parts.append(int(current_chunk))
                except ValueError: parts.append(current_chunk.lower())
            else:
                parts.append(current_chunk.lower())
            current_chunk = char
            is_numeric = char.isdigit()
    if current_chunk:
        if is_numeric:
            try: parts.append(int(current_chunk))
            except ValueError: parts.append(current_chunk.lower())
        else:
            parts.append(current_chunk.lower())
    return parts

def get_all_images_recursive(vfs_path):
    all_files = []
    try:
        dirs, files = xbmcvfs.listdir(vfs_path)
        for f in files:
            if f.lower().endswith(IMAGE_EXTENSIONS):
                file_path = vfs_path.rstrip('/') + '/' + f
                all_files.append(file_path)
        for d in dirs:
            if d == '.' or d == '..': continue
            dir_path = vfs_path.rstrip('/') + '/' + d
            all_files.extend(get_all_images_recursive(dir_path))
    except Exception as e:
        xbmc.log(f"Auto Slideshow: Error scanning {vfs_path}. Error: {e}", level=xbmc.LOGERROR)
    return all_files

xbmc.log("Auto Slideshow: Script started.", level=xbmc.LOGINFO)

while not xbmc.Monitor().waitForAbort(5):
    break

xbmc.log("Auto Slideshow: Startup wait finished.", level=xbmc.LOGINFO)

if pictures_folder == "":
    xbmcgui.Dialog().ok("Auto Slideshow", "Pictures folder is not defined. Please check your settings.")
    exit()

xbmc.log(f"Auto Slideshow: Starting scan of {pictures_folder}", level=xbmc.LOGINFO)

try:
    picture_files = get_all_images_recursive(pictures_folder)
    if not picture_files:
        xbmc.log("Auto Slideshow: No pictures found in folder.", level=xbmc.LOGWARNING)
        xbmcgui.Dialog().ok("Auto Slideshow", "No pictures found in folder. Please check your settings.")
        exit()
    picture_files.sort(key=natural_sort_key)
    xbmc.log(f"Auto Slideshow: Scan complete, {len(picture_files)} images found.", level=xbmc.LOGINFO)
    
except Exception as e:
    xbmc.log(f"Auto Slideshow: Critical error during scan: {e}", level=xbmc.LOGERROR)
    xbmcgui.Dialog().ok("Auto Slideshow", f"Error scanning folder: {e}")
    exit()

while True:
    for picture_file in picture_files:
        xbmc.executebuiltin(f"ShowPicture({picture_file})")
        while not xbmc.Monitor().waitForAbort(picture_display_time):
            break
    
    if enable_weather == 'true':
        xbmc.executebuiltin('Dialog.Close(all,force)')
        xbmc.executebuiltin("ActivateWindow(Weather)")
        while not xbmc.Monitor().waitForAbort(weather_display_time):
            break