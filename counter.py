import cv2
import numpy as np
from time import sleep
from lights import *

largura_min = 80 #Largura minima do retangulo
altura_min = 80 #Altura minima do retangulo

offset = 6 #Erro permitido entre pixel  

pos_linha = 550 #Posição da linha de contagem 

delay = 60 #FPS do vídeo

detec = []


total_cars_in_frame_one  = 0
total_cars_in_frame_two = 0
	
def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

camera_feed_one = 'http://192.168.43.2:81/stream'

camera_feed_two = "http://192.168.43.75:81/stream"

# camera url
#url = 'http://192.168.43.75:81/stream'
url = 'video.mp4'

url1 = '30 Minutes of Cars Driving By in 2009.mp4'
url2 = 'M6 Motorway Traffic.mp4'
cap1 = cv2.VideoCapture(url1)
cap2 = cv2.VideoCapture(url2)

subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

def run_video_feed():
    global total_cars_in_frame_one 
    global total_cars_in_frame_two
    while True:
        ret1 , frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        tempo = float(1/delay)
        
        sleep(tempo) 
        
        grey1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        grey2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        blur1 = cv2.GaussianBlur(grey1,(3,3),5)
        blur2 = cv2.GaussianBlur(grey2,(3,3),5)
        
        img_sub1 = subtracao.apply(blur1)
        img_sub2 = subtracao.apply(blur2)
        
        dilat1 = cv2.dilate(img_sub1, np.ones((5,5)))
        dilat2 = cv2.dilate(img_sub2, np.ones((5,5)))
        
    
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        
        dilatada1 = cv2.morphologyEx (dilat1, cv2. MORPH_CLOSE , kernel1)
        dilatada1 = cv2.morphologyEx (dilatada1, cv2. MORPH_CLOSE , kernel1)
        
        dilatada2 = cv2.morphologyEx (dilat2, cv2. MORPH_CLOSE , kernel2)
        dilatada2 = cv2.morphologyEx (dilatada2, cv2. MORPH_CLOSE , kernel2)
        
        contorno1, h1 = cv2.findContours(dilatada1,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contorno2, h2 = cv2.findContours(dilatada2,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) 
        cv2.line(frame2, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) 
        
        
        for(i,c) in enumerate(contorno1):
            (x,y,w,h) = cv2.boundingRect(c)
            validar_contorno = (w >= largura_min) and (h >= altura_min)
            if not validar_contorno:
                continue

            cv2.rectangle(frame1,(x,y),(x + w, y + h),(0,255,0),2)        
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame1, centro, 4, (0, 0,255), -1)

            for (x, y) in detec:
                if y < (pos_linha + offset) and y > (pos_linha - offset):
                    total_cars_in_frame_one += 1
                    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0,127,255), 3)  
                    detec.remove((x,y))
                    print("Frame 1 Car is detected : " + str(total_cars_in_frame_one)) 
                    
        for(i,c) in enumerate(contorno2):
            (x,y,w,h) = cv2.boundingRect(c)
            validar_contorno = (w >= largura_min) and (h >= altura_min)
            if not validar_contorno:
                continue

            cv2.rectangle(frame2,(x,y),(x + w, y + h),(0,255,0),2)        
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame2, centro, 4, (0, 0,255), -1)

            for (x, y) in detec:
                if y < (pos_linha + offset) and y > (pos_linha - offset):
                    total_cars_in_frame_two += 1
                    cv2.line(frame2, (25, pos_linha), (1200, pos_linha), (0,127,255), 3)  
                    detec.remove((x,y))
                    print("Frame 2 Car is detected : " + str(total_cars_in_frame_two)) 
                    
                        
        
        cv2.putText(frame1,  str(total_cars_in_frame_one) + " cars", (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
        cv2.imshow("Frame 1 Video Original" , frame1)
    
        cv2.putText(frame2, str(total_cars_in_frame_two) + " cars", (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
        cv2.imshow("Frame 2 Video Original", frame2)
        
        cv2.resizeWindow("Frame 1 Video Original", 800, 800)
        cv2.resizeWindow("Frame 2 Video Original", 800, 800)
        
        
        
        
        if(total_cars_in_frame_one > total_cars_in_frame_two):
            turn_off_red_light_one()
            turn_off_green_light_two()
            
            if(0 <= (total_cars_in_frame_one - total_cars_in_frame_two) <= 5):
                turn_on_yellow_light_one()
            else:
                turn_off_yellow_light_two()
                
            
            toggle_red_light_two()
            toggle_green_light_one()
            
        if(total_cars_in_frame_two > total_cars_in_frame_one):
            turn_off_red_light_two()
            turn_off_green_light_one()
            
            if(0 <= (total_cars_in_frame_two - total_cars_in_frame_one) <= 5):
                turn_on_yellow_light_two()
            else:
                turn_off_yellow_light_one()
            
            toggle_red_light_one()
            toggle_green_light_two()
            
        draw_traffic_lights(traffic_image_frame)
    
        cv2.imshow("Traffic Light Status", traffic_image_frame)
   
        if cv2.waitKey(1) == 27:
            break
  
construct_traffic_window()

from multiprocessing import Process

Process(target= run_video_feed()).start()




cv2.destroyAllWindows()
cap1.release()
cap2.release()
