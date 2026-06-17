[app]
title = Traffic Predictor Lite
package.name = trafficpredictorlite
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,tflite
version = 1.0
requirements = python3,kivy,numpy,tflite-runtime
orientation = portrait
android.permissions = INTERNET
android.api = 31
android.minapi = 24
android.ndk = 23b
android.sdk = 31
android.gradle_dependencies = org.tensorflow:tensorflow-lite-select-tf-ops:0.0.0-nightly
fullscreen = 0
[buildozer]
log_level = 2
warn_on_root = 1
