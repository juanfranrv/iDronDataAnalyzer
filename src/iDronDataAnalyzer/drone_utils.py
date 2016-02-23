from dronekit import connect, VehicleMode
from dronekit_sitl import SITL
import time

def conexion_drone():

	print "Starting copter simulator (SITL)"
	sitl = SITL()
	sitl.download('copter', '3.3', verbose=True)
	sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
	sitl.launch(sitl_args, await_ready=True, restart=True)
	connection_string = 'tcp:127.0.0.1:5763'

	print "\nConnecting to vehicle on: %s" % connection_string
	vehicle = connect(connection_string, wait_ready=True)
	vehicle.wait_ready('autopilot_version')


def getDatosDrone():

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

def cerrarConexionDrone():

	#Close vehicle object before exiting script
	print "\nClose vehicle object"
	vehicle.close()

	# Shut down simulator if it was started.
	if sitl is not None:
	    sitl.stop()

	print("Completed")


