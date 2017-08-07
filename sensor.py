# Print the data from sensor with the frequency equals 90 Hz.
# Author: Anastassiya Makarenko.

import time
import datetime, sys, struct
import Adafruit_VCNL40xx # Import the VCNL40xx module.

# Constants
step_norm = 1.0 / 90.0  # A right duration value for one step.

vcnl = Adafruit_VCNL40xx.VCNL4010()  # Create a VCNL4010 instance.


# Checks if the sensor is in the ear with the help of ligth detection.
# Returns True if not in ear.
def isIn(ambient):
    if ambient < 90:
        result = False
    else:
        result = True
    return result  # return False

# Returns the value of ambient light.
def getAmbient():
    ambient = vcnl.read_ambient()  # Read ambient.
    return ambient

# Returns the value of proximity.
def getProximity():
    proximity = vcnl.read_proximity()  # Read proximity.
    return proximity

# Save proximity, ambient and time to file.
def printToFile(proximity, ambient, time_exp):
    print>> f1, 'Proximity={0}, Ambient={1}, Time={2}'.format(proximity, ambient, time_exp)

def streamToSys(proximity, ambient):
    sys.stdout.write(struct.pack('>HH', proximity, ambient))
    sys.stdout.flush()

# Initialization
f1=open('./sensor_output.csv', 'w+')  # Open file to save the data from the sensor.
f2=open('./time_error.csv', 'w+')  # Open file to save the data from the sensor.
time_error = 0  # A time error of whole experiment.
time_start_exp = datetime.datetime.now() # A start time of an experiment.
# Programm loop
while True:
    time_start = datetime.datetime.now()  # Start time of the measurement step.
    prox = getProximity()
    amb = getAmbient()
	# This control option wasn't used in the project.
    # if isIn(amb):
    #     print 'Not in ear'
    #     break
    time_end = datetime.datetime.now()  # End time of the measurement step.
    time_exp = (datetime.datetime.now() - time_start_exp).total_seconds()
    time_step = (time_end - time_start).total_seconds()
    time_error += (step_norm - time_step)  # The error over the time.
    # Print to logfile for time error.
    print>> f2, 'TimeStep = {0}, TimeError = {1}, TimeExp = {2}'.format(time_step, time_error, time_exp)
    if (time_error < step_norm and time_error > (-step_norm)):
        streamToSys(prox, amb) # Stream data.
        printToFile(prox, amb, time_exp)
    # If sensor works faster as it have to.
    if time_error >= step_norm:
        print>>f2, 'Operation={0}'.format("One sample more (sleep one step long)")  # Here have to delete one sample
        time.sleep(step_norm)
        time_error -= step_norm
        print>> f2, 'TimeStep = {0}, TimeError = {1}, TimeExp = {2}'.format(time_step, time_error, time_exp)
    # If sensor works slower as it have to.
    if time_error <= (- step_norm):
        print>>f2, 'Operation={0}'.format("One sample less (duplicate one sample)")  # Here have to add one sample
        streamToSys(prox, amb)
        printToFile(prox, amb, time_exp)
        streamToSys(prox, amb)
        printToFile(prox, amb, time_exp)
        time_error += step_norm
