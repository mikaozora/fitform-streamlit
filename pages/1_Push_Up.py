import streamlit as st
import cv2
import numpy as np
import PoseModule as pm
import pygame


def main_loop():
    st.set_page_config(
        page_title="FitForm",
        page_icon="💪"
    )
    st.title("Push Up Counter")
    st.divider()
    frame_placeholder = st.empty()
    st.write("""
         ## Push Up Guide
         1. Start with a prone position with a straight body
         2. Place your palms on the floor parallel to your shoulders
         3. Make sure your back stays straight and your weight is evenly distributed.
         4. Position the legs straight with the fingertips touching the floor.
            Start lifting your body until your hands are straight.
         5. Do up and down movements by bending your elbows to 90 degrees.""")
    

    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "Fix Form"

    # set dimension
    cap.set(3, 1280)
    cap.set(4, 720)

    pygame.mixer.init()
    sound_file = "fixform.mp3"
    sound = pygame.mixer.Sound(sound_file)
    soundUp = pygame.mixer.Sound("up.mp3")
    soundDown = pygame.mixer.Sound("down.mp3")

    soundCnt = 150
    soundCntUp = 100
    soundCntDown = 100
    isPlaySound = False
    isPlaySoundUp = False
    isPlaySoundDown = False

    bgReps = cv2.imread("reps-bg.png")
    reps_height, reps_width, _ = bgReps.shape
    xReps = 550
    yReps = 25

    while cap.isOpened():
        
        ret, img = cap.read() #1280 x 720
        #Determine dimensions of video - Help with creation of box in Line 43
        width  = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`

        img = cv2.flip(img, 1) #flip img for mirror camera

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23,25)
            
            #Percentage of success of pushup
            per = np.interp(elbow, (90, 160), (0, 100))
            
            #Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (620, 100))

            #Check to ensure right form before starting the program
            if elbow > 160 and shoulder > 40 and hip > 160:
                form = 1
        
            #Check for full range of motion for the pushup
            if form == 1:
                if per == 0:
                    if elbow <= 90 and hip > 160:
                        feedback = "Up"
                        isPlaySoundUp = True
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        isPlaySound = True
                        feedback = "Fix Form"
                        
                if per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        feedback = "Down"
                        isPlaySoundDown = True
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        isPlaySound = True
                        feedback = "Fix Form"
                    
                        
        
            # print(count)

            #play sounds
            soundCnt+=1
            soundCntUp+=1
            soundCntDown+=1
            
            if soundCnt > 150 and isPlaySound == True:
                sound.play()
                soundCnt = 0
                isPlaySound = False

            if soundCntUp > 100 and isPlaySoundUp == True:
                soundUp.play()
                soundCntUp = 0
                isPlaySoundUp = False

            if soundCntDown > 100 and isPlaySoundDown == True:
                soundDown.play()
                soundCntDown = 0
                isPlaySoundDown = False

            #position reps-bg
            img[yReps:yReps+reps_height, xReps:xReps+reps_width] = bgReps

            #Draw Bar
            # if form == 1:
            cv2.rectangle(img, (50, 100), (90, 620), (217, 217, 217), cv2.FILLED)
            cv2.rectangle(img, (50, int(bar)), (90, 620), (0, 79, 252), cv2.FILLED)
            # cv2.putText(img, f'{int(per)}%', (40, 665), cv2.FONT_HERSHEY_PLAIN, 2, (0, 79, 252), 2)
            cv2.putText(img, '0', (60, 650), cv2.FONT_HERSHEY_PLAIN, 2, (0, 79, 252), 3)
            cv2.putText(img, '100', (40, 85), cv2.FONT_HERSHEY_PLAIN, 2, (0, 79, 252), 3)


            #Pushup counter
            cv2.putText(img, str(int(count)), (605, 135), cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 0, 0), 3)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        frame_placeholder.image(img, channels="RGB")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    
if __name__ == '__main__':
    main_loop()
