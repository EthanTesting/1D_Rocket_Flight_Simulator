##################################################################################################################
#Linear Interpolate between values
##################################################################################################################
def Linear_Interpolate_Between(LowerValx,HigherValx,LowerValy,HigherValy,TargetValx):
    #Function variable setup
    Targetvaly = 0
    Weighted_Difference = 0
    if (HigherValx == LowerValx):
        Targetvaly = LowerValy
    else:
        #Calculationn to find difference between target and actual
        Weighted_Difference = (TargetValx-LowerValx)/(HigherValx-LowerValx)
        #Finding Target value
        Targetvaly = LowerValy + (Weighted_Difference * (HigherValy-LowerValy))
    return Targetvaly

##################################################################################################################
#Linear Interpolate to extend line
##################################################################################################################
def Linear_Interpolate_Extend(LowerValx,HigherValx,LowerValy,HigherValy,TargetValx):
    #Function variable setup
    Newvaly = 0
    gradient = 0
    c = 0

    #find gradient of line
    gradient = (HigherValx - LowerValx) / (HigherValy - LowerValy)
    #y = mx + c find c
    c = LowerValy - (gradient * LowerValx)
    #Finding Target value
    Newvaly = (gradient * TargetValx) + c



###################################################################################################################
#Denisty of air Solver function
###################################################################################################################
def Density(Height):
    #variable/ arrray setup
    Input_Altitude = [0,1000,2000,3000,4000]
    Input_Density = [1.225,1.112,1.007,0.9093,0.8194]
    Answer = 0
    Lower_Array_Position = 0
    Higher_Array_Position = len(Input_Altitude) - 1
    #attempting to find lower/ higher values/ array positions
    for i in range(len(Input_Altitude)):
        #finding lower
        if (Input_Altitude[i] <= Height) and (Input_Altitude[Lower_Array_Position] <= Input_Altitude[i]):
            Lower_Array_Position = i

        #finding heigher
        if (Input_Altitude[i] >= Height and Input_Altitude[i] <= Input_Altitude[Higher_Array_Position]):
            Higher_Array_Position = i

        #finding densiy using linear iterpolation of data.
    Answer = Linear_Interpolate_Between(Input_Altitude[Lower_Array_Position], Input_Altitude[Higher_Array_Position], Input_Density[Lower_Array_Position], Input_Density[Higher_Array_Position], Height)
    return Answer

#####################################################################################################################
#Finding air viscosity at height
#####################################################################################################################
def Viscos(Height):
    #variable/ arrray setup
    Input_Altitude = [0,1000,2000,3000,4000]
    Input_viscosity = [0.00001789,0.00001758,0.00001726,0.00001694,0.00001661]
    Answer = 0
    Lower_Array_Position = 0
    Higher_Array_Position = len(Input_Altitude) - 1

    #attempting to find lower/ higher values/ array positions
    for i in range(len(Input_Altitude)):
        #finding lower
        if (Input_Altitude[i] <= Height and Input_Altitude[Lower_Array_Position] <= Input_Altitude[i]):
            Lower_Array_Position = i

        #finding heigher
        if (Input_Altitude[i] >= Height and Input_Altitude[i] <= Input_Altitude[Higher_Array_Position]):
            Higher_Array_Position = i

        #finding densiy using linear iterpolation of data.
    Answer = Linear_Interpolate_Between(Input_Altitude[Lower_Array_Position], Input_Altitude[Higher_Array_Position], Input_viscosity[Lower_Array_Position], Input_viscosity[Higher_Array_Position], Height)
# For testing    print(Lower_Array_Position,Higher_Array_Position)
    return Answer

####################################################################################################################
#Finding thrust from thrust data
####################################################################################################################
def Force_Thrust_Fun(Thrust_Time,Force_Thrust_Data,Time_Thrust,Thrust_Count,Burn_Time):
    answer = 0
    Lower_Array_Position = 0
    Higher_Array_Position = Thrust_Count - 1
    #finding thrust at flight time
    if Time_Thrust > Burn_Time:
        answer = 0
    else:
        for i in range(Thrust_Count-1):
            #finding lower value
            if (Thrust_Time[i] < Time_Thrust and Thrust_Time[Lower_Array_Position] < Thrust_Time[i]):
                Lower_Array_Position = i
            #finding higher
            if  (Thrust_Time[i] > Time_Thrust and Thrust_Time[i] < Thrust_Time[Higher_Array_Position]):
                Higher_Array_Position = i
        answer = Linear_Interpolate_Between(Thrust_Time[Lower_Array_Position], Thrust_Time[Higher_Array_Position], Force_Thrust_Data[Lower_Array_Position], Force_Thrust_Data[Higher_Array_Position], Time_Thrust);
	
    return answer

###################################################################################################################
#Solving for reynolds number at specific height
###################################################################################################################
def ReynoldsNumber_Fun(Density,Velocity, Rocket_Length,Dynamic_Viscosity):
    return ((Density * Velocity * Rocket_Length) / Dynamic_Viscosity)


###################################################################################################################
#Solving for drag coefficient from file data
###################################################################################################################
def Drag_Coefficient_Fun(ReynoldsNumber,DragCoefficient,ReynoldNum,Drag_Count):
    answer = 0
    Lower_Array_Position = 0
    Higher_Array_Position = Drag_Count-1
    if (ReynoldNum > ReynoldsNumber[Drag_Count-1]):
        Lower_Array_Position = Drag_Count - 2
    else:
        for i in range(Drag_Count-1):
            #finding lower value
            if (ReynoldsNumber[i] < ReynoldNum and ReynoldsNumber[Lower_Array_Position] < ReynoldsNumber[i]):
                Lower_Array_Position = i
	    #finding higher
            if ReynoldsNumber[i] > ReynoldNum and ReynoldsNumber[i] < ReynoldsNumber[Higher_Array_Position]:
                Higher_Array_Position = i
    #Solving for the answer
    answer = Linear_Interpolate_Between(ReynoldsNumber[Lower_Array_Position], ReynoldsNumber[Higher_Array_Position], DragCoefficient[Lower_Array_Position], DragCoefficient[Higher_Array_Position], ReynoldNum);
    return answer;

##################################################################################################################
#Solving for the drag force of the rocket
##################################################################################################################
def DragForce(Density,Velocity,Area,DragCoefficient):
    return ((Density * (Velocity * Velocity) * Area * DragCoefficient) / 2)
