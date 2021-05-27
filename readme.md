# Instructions for Running Code
## Android App that interacts with DJI Drone:
    1. Android App is located in code/DJISimulatorDemo
    2. This folder can be imported into Android Studio (press "Open Project" and choose this folder)
    3. Once in Android Studio, the app can be built and run on the DJI Smart Controller

## Python App that runs on Windows Computer to interact with Myo Armband
    1. The code for this is available in "code/Myo"
    2. Run the Python file using Python 3.7 (3.8+ does not work) after installing the libraries in requirements.txt

# Helpful Tips to make everything function together
    1. Run the python code and the android app concurrently
    2. Ensure both the DJI Smart Controller and the laptop running the Python script are on the same WiFi
    3. You may have to adjust the path for where the apps should access their respective SDKs (for both the Python app and the Android app). This will be a String inside the code that you will change.
    4. You may have to change the IP address when creating the socket between the Smart Controller and laptop. Make sure to double check the IP address of both your laptop and Smart Controller.
    5. For more updated code and details, you can access the GitHub repo at https://github.com/krishg-11/Gesture-Control-For-Drones

