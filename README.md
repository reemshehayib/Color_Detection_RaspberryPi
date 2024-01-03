# Color Detection and Object Localization
This Python script utilizes the Raspberry Pi, a camera, and color detection to determine the position and ratio of colored objects in real-time. The script is designed to work with colors such as Red, Green, Blue, and Black. This work was applied in an embedded system project where a rover sequentially detects colors as required.

## Prerequisites
Hardware Setup:  
Raspberry Pi with GPIO pins  
Camera module  
Ultrasonic sensor connected to GPIO pins (TRIG to 15, ECHO to 27)  
LED indicators connected to GPIO pins (LEFT_PIN to 23, RIGHT_PIN to 24, RATIO_PIN to 25)  

Software Dependencies:
Python  
OpenCV (pip install opencv-python)  
NumPy (pip install numpy)  
RPi.GPIO (pip install RPi.GPIO)  

## Usage
1. Clone the repository to your Raspberry Pi.  
   ``git clone https://github.com/your-username/your-repository.git``  
   ``cd your-repository``
  
2. Ensure the required hardware is properly connected to your Raspberry Pi.
3.  Run the script based on the color you want to detect. In your main for red detection, for example, run: detect_color_red()

## Important Notes
Ensure the GPIO pins are correctly set up according to your hardware configuration.  
The script uses color ranges for each color, and you may need to adjust these ranges based on your specific lighting conditions.  
Press 'q' to exit the script and release the camera.    
Feel free to customize the script according to your specific requirements and hardware setup. For any issues or improvements, please create a new issue or pull request.   
