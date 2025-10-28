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
android.minapi = 21   ; Hỗ trợ từ Android 5.0 trở lên
android.api = 33     ; API mục tiêu mới nhất
android.archs = armeabi-v7a, arm64-v8a
# android.split_archs = True
