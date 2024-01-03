import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

# Set up GPIO pins for sensor
TRIG = 15
ECHO = 27

maxTime = 0.04

# Set up GPIO pins for camera
LEFT_PIN = 23  
RIGHT_PIN = 24  
RATIO_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PIN, GPIO.OUT)
GPIO.setup(RATIO_PIN, GPIO.OUT)

# Capturing video through cap
cap = cv2.VideoCapture(0)

def sensor():

    while True:
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        GPIO.output(TRIG,False)

        time.sleep(0.01)

        GPIO.output(TRIG,True)

        time.sleep(0.00001)

        GPIO.output(TRIG,False)

        pulse_start = time.time()
        timeout = pulse_start + maxTime
        while GPIO.input(ECHO) == 0 and pulse_start < timeout:
            pulse_start = time.time()

        pulse_end = time.time()
        timeout = pulse_end + maxTime
        while GPIO.input(ECHO) == 1 and pulse_end < timeout:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        print(distance)
        if distance<10:
            return True


def detect_side_of_image(contour, image_width):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        image_center = image_width // 2

        if cx < image_center-100:
            return "Left"
        elif cx>image_center+100:
            return "Right"
    else:
        return "Cannot determine"


def calculate_contour_area_ratio(contour, image_area):
    contour_area = cv2.contourArea(contour)
    ratio = contour_area / image_area
    return ratio


def draw_contour_with_info(image, contour, color, text, side, ratio):
    _, imageFrame = cap.read()
    ratio = calculate_contour_area_ratio(contour, imageFrame.shape[0] * imageFrame.shape[1])
    
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    cv2.putText(image, f"{text} ({side}), Ratio: {ratio:.2f}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color)
    

def detect_and_display_color(imageFrame, color_mask, color_text, color, color_lower, color_upper):
    color_mask = cv2.dilate(color_mask, np.ones((5, 5), "uint8"))
    res_color = cv2.bitwise_and(imageFrame, imageFrame, mask=color_mask)

    contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            side = detect_side_of_image(contour, imageFrame.shape[1])
            ratio = calculate_contour_area_ratio(contour, imageFrame.shape[0] * imageFrame.shape[1])
            if side == "Left":
                GPIO.output(LEFT_PIN, GPIO.HIGH)
                GPIO.output(RIGHT_PIN, GPIO.LOW)
            elif side == "Right":
                GPIO.output(LEFT_PIN, GPIO.LOW)
                GPIO.output(RIGHT_PIN, GPIO.HIGH)
            else:
                GPIO.output(RIGHT_PIN, GPIO.LOW)
                GPIO.output(LEFT_PIN, GPIO.LOW)

                
            if ratio>0.3:
                GPIO.output(RATIO_PIN, GPIO.HIGH)
            else:
                GPIO.output(RATIO_PIN, GPIO.LOW)
            
            draw_contour_with_info(imageFrame, contour, color, color_text, side, ratio)
            GPIO.output(RIGHT_PIN, GPIO.LOW)
            GPIO.output(LEFT_PIN, GPIO.LOW)
            GPIO.output(RATIO_PIN, GPIO.LOW)


def get_color_code(color):
    if color == "Red":
        return (0, 0, 255)  # BGR color code for red
    elif color == "Green":
        return (0, 255, 0)  # BGR color code for green
    elif color == "Blue":
        return (255, 0, 0)  # BGR color code for blue
    elif color == "Black":
        return (0, 0, 0)  # BGR color code for black

def detect_color_red():
    while True:
        _, imageFrame = cap.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        color_ranges = {
            "Red": ([136, 87, 111], [180, 255, 255])
        }
        for color, (lower, upper) in color_ranges.items():
            color_mask = cv2.inRange(hsvFrame, np.array(lower, np.uint8), np.array(upper, np.uint8))
            detect_and_display_color(imageFrame, color_mask, f"{color} color", get_color_code(color), lower, upper)

        #cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            GPIO.cleanup()
            break

def detect_color_green():
    while True:
        _, imageFrame = cap.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
        color_ranges = {
            "Green": ([25, 52, 72], [102, 255, 255])
        }
        
        for color, (lower, upper) in color_ranges.items():
            color_mask = cv2.inRange(hsvFrame, np.array(lower, np.uint8), np.array(upper, np.uint8))
            detect_and_display_color(imageFrame, color_mask, f"{color} color", get_color_code(color), lower, upper)

        #cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            GPIO.cleanup()
            break

def detect_color_blue():
    while True:
        _, imageFrame = cap.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
        color_ranges = {
            "Blue": ([94, 80, 2], [120, 255, 255])
        }
        
        for color, (lower, upper) in color_ranges.items():
            color_mask = cv2.inRange(hsvFrame, np.array(lower, np.uint8), np.array(upper, np.uint8))
            detect_and_display_color(imageFrame, color_mask, f"{color} color", get_color_code(color), lower, upper)

        #cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            GPIO.cleanup()
            break

def detect_color_black():
    while True:
        _, imageFrame = cap.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        
        color_ranges = {
            "Black": ([0, 0, 0], [255, 255, 50])
        }
        for color, (lower, upper) in color_ranges.items():
            color_mask = cv2.inRange(hsvFrame, np.array(lower, np.uint8), np.array(upper, np.uint8))
            detect_and_display_color(imageFrame, color_mask, f"{color} color", get_color_code(color), lower, upper)

        #cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            GPIO.cleanup()
            break




