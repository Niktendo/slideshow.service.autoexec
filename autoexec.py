import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

enable_video = xbmcaddon.Addon().getSetting("enable_video")
video_file = xbmcaddon.Addon().getSetting("video_file")

enable_slideshow = xbmcaddon.Addon().getSetting("enable_slideshow")
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

if video_file == "" and enable_video == 'true' or pictures_folder == "" and enable_slideshow == 'true':
    xbmcgui.Dialog().ok("Auto Slideshow", "Video file or pictures folder not defined. Please check your settings.")
    exit()

if enable_slideshow == 'true':
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
    if enable_video == 'true':
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmc.executebuiltin(f"PlayMedia({video_file})")
        while not xbmc.Player().isPlaying():
            pass
        while xbmc.Player().isPlaying():
            if xbmc.Monitor().waitForAbort(0.1):
                exit()

    if enable_slideshow == 'true':
        xbmc.executebuiltin('Dialog.Close(all,true)')
        for picture_file in picture_files:
            xbmc.executebuiltin(f"ShowPicture({picture_file})")
            if xbmc.Monitor().waitForAbort(picture_display_time):
                exit()

    if enable_weather == 'true':
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmc.executebuiltin("ActivateWindow(Weather)")
        if xbmc.Monitor().waitForAbort(weather_display_time):
            exit()
