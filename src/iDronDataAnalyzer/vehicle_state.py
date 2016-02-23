from dronekit import connect, VehicleMode
import time

#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not args.connect:
    print "Starting copter simulator (SITL)"
    from dronekit_sitl import SITL
    sitl = SITL()
    sitl.download('copter', '3.3', verbose=True)
    sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
    sitl.launch(sitl_args, await_ready=True, restart=True)
    connection_string = 'tcp:127.0.0.1:5763'


# Connect to the Vehicle. 
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
print "\nConnecting to vehicle on: %s" % connection_string
vehicle = connect(connection_string, wait_ready=True)

vehicle.wait_ready('autopilot_version')

# Get all vehicle attributes (state)
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " GPS: %s" % vehicle.gps_0
print " Gimbal status: %s" % vehicle.gimbal
print " Battery: %s" % vehicle.battery

# Get Vehicle Home location - will be `None` until first set by autopilot
while not vehicle.home_location:
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    if not vehicle.home_location:
        print " Waiting for home location ..."
# We have a home location, so print it!        
print "\n Home location: %s" % vehicle.home_location

#Close vehicle object before exiting script
print "\nClose vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

print("Completed")




