import numpy as np
from tkinter import messagebox as msbx

def angleStrToFloat(angle:str) -> float:
    ''' This function converts an angle string to a float number.'''
    if '°' in angle:
        angle = angle.replace('°',':').replace('\'',':').replace('\"',':').split(':')
        for i in angle:
            if i == '':
                angle.remove(i)
        
        if len(angle) >= 3:
            angle = float(angle[0]) + float(angle[1])/60 + float(angle[2])/3600 
        elif len(angle) == 2:
            angle = float(angle[0]) + float(angle[1])/60
        elif len(angle) == 1:
            angle = float(angle[0])
        else:
            print('Invalid angle')
            return 0
        return  angle
    else:
        return float(angle)
    



if __name__ == '__main__':

    angle = " 60° 35' 15\" "

    # angle = "1.5707963267948966"

    print(angleStrToFloat(angle))