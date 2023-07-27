import cv2
import imutils
import threading
import winsound
# from tkinter import*
# from tkinter import ttk

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("Allarm")
        winsound.Beep(1500,500)
    alarm = False

def noice_main():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    _, start_frame = cap.read()
    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    alarm = False
    global alarm_mode
    alarm_mode = False
    alarm_counter = 0


    # def beep_alarm():
    #         global alarm
    #         for _ in range(5):
    #             if not alarm_mode:
    #                 # print("heloo")
    #                 break
    #             print("ALARM")
    #             winsound.Beep(2500, 1000)
    #             #winsound.PlaySound('mixkit-sound-alert-in-hall-1006.wav', winsound.SND_ASYNC)
    #         alarm = False

    while True:
                _, frame = cap.read()
                frame = imutils.resize(frame, width=500)

                if alarm_mode:
                    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)

                    diffrence = cv2.absdiff(frame_bw, start_frame)
                    threshold = cv2.threshold(diffrence, 25, 255, cv2.THRESH_BINARY)[1]
                    start_frame = frame_bw

                    if threshold.sum() > 300:
                        alarm_counter += 1
                    else:
                        if alarm_counter > 0:
                            alarm_counter -= 1
                    cv2.imshow("Cam", threshold)
                else:
                    cv2.imshow("Cam", frame)

                if alarm_counter > 20:
                    print("20")
                    if not alarm:
                        alarm = True
                        threading.Thread(target=beep_alarm).start()

                key_pressed = cv2.waitKey(30)
                if key_pressed == ord("t"):
                    alarm_mode = not alarm_mode
                    alarm_counter = 0
                if key_pressed == ord("q"):
                    alarm_mode = False
                    # cap.release()
                    # cv2.destroyAllWindows()
                    break

if __name__ == "__main__":
    noice_main()
           



# if __name__ == "__main__":
#     # root=Tk()
#     obj=Noice_Detector()
#     # root.mainloop()