[app]

# (str) Title of your application
title = KivyCameraOCR

# (str) Package name
package.name = kivycameraocr

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let pyinstaller include these)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (list) List of directory to exclude
source.exclude_dirs = tests, bin

# (str) Version of your application
version = 1.0

# (str) Application icon
icon.filename = icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Whether the application should be fullscreen or not
fullscreen = 0

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = main.py

# (list) Permissions
android.permissions = CAMERA

# (int) Android API to use
android.api = 27

# (int) Minimum API required
android.minapi = 21

# (bool) Indicate whether the application should be shown as a fullscreen application
android.fullscreen = 0

# (list) Python dependencies, comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,opencv-python-headless,pillow,pytesseract,imutils

# (bool) Use the Python for android repository (True) or not (False)
# android.use_p4a = True

# (str) Android NDK directory (if needed)
# android.ndk_path = /opt/android-ndk-r19c

# (str) Android SDK directory (if needed)
# android.sdk_path = /opt/android-sdk

# (list) Android NDK version to use
# android.ndk = 19c

# (list) Android SDK version to use
# android.sdk = 27

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (str) Android app theme, you can use for example: '@android:style/Theme.NoTitleBar'
# android.theme = '@android:style/Theme'

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1
