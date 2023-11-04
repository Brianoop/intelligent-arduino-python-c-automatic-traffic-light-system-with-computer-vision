import cv2
import numpy as np
import time
from threading import Thread
# Function to toggle the light state
def toggle_red_light_one():
    global red_light_one_on
    red_light_one_on = not red_light_one_on
    
def toggle_yellow_light_one():
    global yellow_light_one_on
    yellow_light_one_on = not yellow_light_one_on
    
def toggle_green_light_one():
    global green_light_one_on
    green_light_one_on = not green_light_one_on
        
def toggle_red_light_two():
    global red_light_two_on
    red_light_two_on = not red_light_two_on
    
def toggle_yellow_light_two():
    global yellow_light_two_on
    yellow_light_two_on = not yellow_light_two_on
    
def toggle_green_light_two():
    global green_light_two_on
    green_light_two_on = not green_light_two_on


def turn_off_green_light_two():
    global green_light_two_on
    green_light_two_on = False
    
def turn_off_green_light_one():
    global green_light_one_on
    green_light_one_on = False
    
    
def turn_off_red_light_two():
    global red_light_two_on
    red_light_two_on = False
    
def turn_off_red_light_one():
    global red_light_one_on
    red_light_one_on = False


def turn_off_yellow_light_two():
    global yellow_light_two_on
    yellow_light_two_on = False
    
def turn_off_yellow_light_one():
    global yellow_light_one_on
    yellow_light_one_on = False


def turn_on_yellow_light_two():
    global yellow_light_two_on
    yellow_light_two_on = True
    
def turn_on_yellow_light_one():
    global yellow_light_one_on
    yellow_light_one_on = True

# Create a black image
traffic_image_frame = np.zeros((400, 600, 3), dtype = np.uint8)

# Initialize the red light state
red_light_one_on = True
yellow_light_one_on = False
green_light_one_on = False

red_light_two_on = False
yellow_light_two_on = False
green_light_two_on = True


# Function to draw the traffic light circles
def draw_traffic_lights(image):
    #print("drawing traffic lights🔥")
    circle_radius = 40
    circle_color_red = (0, 0, 255)  # Red color in BGR format
    circle_color_yellow = (0, 255, 255)  # Yellow color in BGR format
    circle_color_green = (0, 255, 0)  # Green color in BGR format

    # Define vertical offsets for spacing
    offset_red_yellow = 20
    offset_yellow_green = 20

    # Draw circles for the first pair of traffic lights (Road 1)
    cv2.circle(image, (150, 200 - offset_red_yellow), circle_radius, circle_color_red if red_light_one_on else (0, 0, 0), -1)  # Red
    cv2.circle(image, (150, 290 - offset_yellow_green), circle_radius, circle_color_yellow if yellow_light_one_on else (0, 0, 0)  , -1)  # Yellow
    cv2.circle(image, (150, 360), circle_radius, circle_color_green if green_light_one_on else (0, 0, 0) , -1)  # Green

    # Draw circles for the second pair of traffic lights (Road 2)
    cv2.circle(image, (450, 200 - offset_red_yellow), circle_radius, circle_color_red if red_light_two_on else (0, 0, 0), -1)  # Red
    cv2.circle(image, (450, 290 - offset_yellow_green), circle_radius, circle_color_yellow if yellow_light_two_on else (0, 0, 0), -1)  # Yellow
    cv2.circle(image, (450, 360), circle_radius, circle_color_green if green_light_two_on else (0, 0, 0), -1)  # Green


def construct_traffic_window():
    cv2.putText(traffic_image_frame, "Road 1", (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    #cv2.putText(image, "", (100, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(traffic_image_frame, "Road 2", (400, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    #cv2.putText(image, "", (400, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Create an OpenCV window and display the image
    cv2.namedWindow("Traffic Light Status", cv2.WINDOW_NORMAL)
    draw_traffic_lights(traffic_image_frame)
    cv2.imshow("Traffic Light Status", traffic_image_frame)
    print("😁")
 
    

def start_traffic_lights():
    while True:
        draw_traffic_lights(image)
        cv2.imshow("Traffic Light Status", image)
        
        # Toggle the red light state every second
        time.sleep(0.5)
        toggle_red_light_one()
        #toggle_yellow_light_one()
        #toggle_green_light_one()
        
        #toggle_red_light_two()
        #toggle_yellow_light_two()
        toggle_green_light_two()

        # Check for a key press and exit if 'q' is pressed
        key = cv2.waitKey(100)
        if key == ord('q'):
            break
        
        


def lights_start(car_count_one, car_count_two):
    construct_traffic_window(car_count_one, car_count_two)
    start_traffic_lights()

    




