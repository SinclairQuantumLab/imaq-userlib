from labscript import start, stop
from labscriptlib.imaq_lab.connection_table import ConnectionTable

ConnectionTable()

start()

t = 0.0

# turn off MOT & repumper powers at t=0.
mot_repumper_analog.constant(t, 0)
mot_laser_analog.constant(t, 0)

t += 1

mot_repumper_analog.constant(t, repump_amp_setpoint)
mot_laser_analog.constant(t,mot_amp_setpoint)

t += image_wait_time

imaq_cam1.expose(
    t=t,
    name='flir_camera_test',
    frametype='cam1',
    trigger_duration=50e-3,
)

imaq_cam2.expose(
    t=t,
    name='flir_camera_test',
    frametype='cam2',
    trigger_duration=50e-3,
)


t += 0.5
# Leave enough time for the acquisitions to complete
stop(t)
