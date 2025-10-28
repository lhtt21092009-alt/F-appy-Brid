[app]
title = Flappy Brid
package.name = flappybrid
package.domain = org.oibanoi874
source.dir = .
source.include_exts = py,png,jpg,mp3,wav,ogg
icon.filename = icon.png
version = 1.0
requirements = python3,kivy,pyjnius,hostpython3,pygame
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.minapi = 21
android.api = 33
android.ndk = 25b
android.sdk_tools_version = 34.0.0
android.archs = armeabi-v7a,arm64-v8a
# android.split_archs = True
# android.permissions = INTERNET
