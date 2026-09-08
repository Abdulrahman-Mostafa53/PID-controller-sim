import math

class Pid:
    def __init__(self,target, kp, ki, kd,anti_wind_clamp=1e+8,controller_clamp = 1e+8,thres=0.0000001, start=0):

        # intializing parameters passed to the constructor 
        # pass in your target , KP , KI , KD  anti wind clamp point (optional),
        # overall controller clamp point (optional)
        # threshold for dead zone(optional), start point (optional)

        self.TARGET = target
        self.KP = kp
        self.KI = ki
        self.KD = kd
        self.anti_wind_clamp = anti_wind_clamp
        self.controller_clamp =controller_clamp
        self.THRES = thres
        self.START = start

        # in your code after you have a pid object, set :

        # pid.current_state to the current state of the system
        # ex : a motor rotated 75 degs but we need it to rotate 90 degs so
        # 75 is current_state 

        # pid.error to the current error val : (target  - current_state)

        # pid.accum_error +=  new error (accumulate your errors here for integral calculation)


        self.current_state = start
        self.error = target - start
        self.accum_error = 0
        
    
    def compute(self,dt,error_dif):
        # this function calculates the output signal
        # if you have done the setup we discussed earlier all you have to provide now is :
        # error_dif : this is the change in error in some time dt 
        # error_dif  = e2 - e1

        # dt : the time where error_dif happended
        # for example if you are running a while loop (but must be restricted
        # by some time don't live it up to cpu power!) you can define dt as time between two
        # iterations 
        
        e2 = self.error
        e1 = e2 - error_dif


        # Conditional Integration / Zero-Crossing Reset (reset accumulative error when
        # e1 and e2 have different signs which indiactes zero crossing)
        if e2  != math.copysign(e2,e1):
            self.accum_error = 0
            

        # check for deadzone
        if abs(self.error) < self.THRES:
            print("yeppp")
            return 0
        
        p = round(self.KP * self.error,4)

        # find who is min our I or the clamping value so that if I is more that
        # clamping value we clamp I (Anti wind up )
        i = min(round(self.KI * self.accum_error,4),self.anti_wind_clamp)

        d = round(self.KD * (error_dif/dt),4)

        
        # print("_________________________________________________")
        # print(
        #     f"P: {p} -- I: {i} -- D: {d} -- accum : {round(self.accum_error,4)}"
        # )
        # print("_________________________________________________")

        # if p + i + d is less than the user specified clamp return it 
        # otherwise return clamp value
        return min(p+i+d,self.controller_clamp)
