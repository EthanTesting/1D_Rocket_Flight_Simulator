from functions import*
import csv
#########################################################
#inputs section
#########################################################
Rocket_Length = 2.040 # In meters
Rocket_Area = 0.8144 # in meters squared
Initial_RocketMass = 2.853 + 1.774 # in kilograms includes propelant weight and all consumables
Initial_Propelent_Weight = 1.774 # in kilograms
MaxTime = 30 # in seconds
TimeIterations = 6000 #amount of specific time steps program will have.

MotorFileName  = 'Blue_Streak_pro75_3Grain.csv'
DragFileName = 'Initial_Proof_Rocket.csv'
########################################################
#Program constants
########################################################
deltaT = MaxTime/TimeIterations
Force_Thrust = 0
Drag_Count = 0
Thrust_Count = 0

FirstPositiveForce = False
BurnTime = 0
drag_Coefficient_temp = 0


##########################################################
#Array Setup for variables we want
##########################################################
TimeStep = []
RocketHeight = []
RocketVelocity = []
RocketReynolds = []
ForceTotal = []
ForceDragCoefficient = []
ForceDrag = []
ForceGravity = []
ForceThrust = []



#Input Data array Setup
DragCoefficient = []
ReynoldsNumber = []
Drag_Count = 0
Force_Thrust_Data = []
Thrust_Time = []
Thrust_Count = 0

##########################################################
#Reading Data from drag and motor files use of csv files
##########################################################

#Reading from thrust file
with open(MotorFileName) as MotorFile:
    MotorInfo = csv.reader(MotorFile, delimiter =',')
    for row in MotorInfo:
        #grabing thrust data from file
        Thrust_Time.insert(Thrust_Count,float(row[0]))
        Force_Thrust_Data.insert(Thrust_Count,float(row[1]))
        Thrust_Count += 1
BurnTime = float(Thrust_Time[Thrust_Count-1])

#Reading from drag file
with open(DragFileName) as DragFile:
    DragInfo = csv.reader(DragFile, delimiter = ',')
    for row in DragInfo:
        #Getting reyniolds number and drag data.
        ReynoldsNumber.insert(Drag_Count,float(row[0]))
        DragCoefficient.insert(Drag_Count,float(row[1]))
        Drag_Count += 1

###########################################################
#first values in flight arrays
###########################################################

TimeStep.insert(0,0)
RocketHeight.insert(0,0)
RocketVelocity.insert(0,0)


###############################################################
#Iteration point for rocket flight
################################################################


for i in range(TimeIterations):
    #Getting next time point for simulation
    TimeStep.insert(i+1,TimeStep[i]+deltaT)
    
    #Finding propellent weight burned off
    #It has been assumed that propelant burns at constant rate.
    if (TimeStep[i] < BurnTime):
        ForceGravity.insert(i,(9.81 * (Initial_RocketMass - ((TimeStep[i] * Initial_Propelent_Weight) / BurnTime))))
    else:
        ForceGravity.insert(i,(9.81 * (Initial_RocketMass - Initial_Propelent_Weight)))

    #Solving for Reynolds number and making sure that the reynolds number is above 70000 then solving for drag coefficient
    RocketReynolds.insert(i,ReynoldsNumber_Fun(Density(RocketHeight[i]), RocketVelocity[i], Rocket_Length, Viscos(RocketHeight[i])))
    #using reynolds  number to find drag coefficient from ansys simulation data file.
    if (RocketReynolds[i] <= 70000):
        drag_Coefficient_temp = 0
    else:
        drag_Coefficient_temp = Drag_Coefficient_Fun(ReynoldsNumber, DragCoefficient, RocketReynolds[i], Drag_Count)

    #Saving drag coefficient data in Array.
    ForceDragCoefficient.insert(i,drag_Coefficient_temp)




    #Solving for Drag force using data saved from above. given in newtons.
    ForceDrag.insert(i,DragForce(Density(RocketHeight[i]) , RocketVelocity[i], Rocket_Area, ForceDragCoefficient[i]))
		
		
    #Solving for force thrust using motor file data.
    ForceThrust.insert(i,Force_Thrust_Fun(Thrust_Time, Force_Thrust_Data, TimeStep[i], Thrust_Count, BurnTime))


####################################################################### Fix Bellow
    #Finding total force on rocket.
    ForceTotal.insert(i, ForceThrust[i] - ForceDrag[i] - ForceGravity[i])
    #Making sure that there is no negative force in the first stages of the simulation as there will be something stoping rocket from falling .
    if (ForceTotal[i] < 0 and FirstPositiveForce == False):
        ForceTotal[i] = 0
    else:
    #Had the first positive force so change to true to skip if statement.
        FirstPositiveForce = True

    #Finding Rocket velocity and therefore height using eulers method.
    RocketVelocity.insert(i+1,(RocketVelocity[i] + deltaT * (ForceTotal[i] / (ForceGravity[i] / 9.81))))
    RocketHeight.insert(i+1,RocketHeight[i] + deltaT * RocketVelocity[i])










    #Displaying key arrays in command line for testing and to see progress.
    #print("Time_Step =",TimeStep[i])
    #print("Reynolds =",RocketReynolds[i])
    #print("Drag_Coefficient =",ForceDragCoefficient[i])
    #print("Drag_Force =", ForceDrag[i])
    #print("Thrust Force at time step =",ForceThrust[i])
    #print("Total Force =", ForceTotal[i])
    #print("Rocket Velocity =", RocketVelocity[i])
    #print("Rocket Height =", RocketHeight[i])
    #print("")
    print("percentage done =", (i/TimeIterations)*100)
print("done")
########################################################################################################################
#Writting to file or displaying in graphs
########################################################################################################################

#Graphing setup
import matplotlib.pyplot as plt


plt.scatter(TimeStep, RocketVelocity)
plt.show()
