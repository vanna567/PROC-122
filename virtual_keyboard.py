import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#print(width)
#print(height)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

#crear estado para el video
state = None

# Definir una función para contar dedos
def countFingers(image, hand_landmarks, handNo=0):

    #globalizar nuestra variable
    global state

    if hand_landmarks:
        # Obtener todas los puntos de referencia en la primera mano visible
        landmarks = hand_landmarks[handNo].landmark

        # Contar los dedos        
        fingers = []

        for lm_index in tipIds:
                # Obtener los valores de la posición "y" de la punta y parte inferior del dedo
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Verificar si algun dedo está abierto o cerrado
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # print("El dedo con ID ",lm_index," está abierto")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # print("El dedo con ID ",lm_index," está cerrado")

        totalFingers = fingers.count(1)
        
        # Reproducir o pausar un video
        if totalFingers == 4:
            state = "Play"

        if totalFingers == 0:
            state = "Pause"
            keyboard.press(Key.space)
        

         # Mover un video hacia adelante o hacia atrás 
        finger_tip_x = (landmarks[8].x)*width
        if totalFingers == 1:
           if finger_tip_x < width - 300:
              print("regresando")
              keyboard.press(Key.left)

           if finger_tip_x > width - 50:
               print("adelantando")
               keyboard.press(Key.left)

               
        
         
         ################################

             # AGREGA EL CÓDIGO AQUÍ #

        ################################ 
        
# Definir una función para 
def drawHandLanmarks(image, hand_landmarks):

    # Dibujar conexiones entre los puntos de referencia
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detectar las marcas de referencia de las manos 
    results = hands.process(image)

    # Obtener las marcas de referencia del resultado procesado
    hand_landmarks = results.multi_hand_landmarks

    # Dibujar las marcas de referencia
    drawHandLanmarks(image, hand_landmarks)

    # Obtener la posición de los dedos de las manos       
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de medios", image)

    # Cerrar la ventana al presionar la tecla escape (esc)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
