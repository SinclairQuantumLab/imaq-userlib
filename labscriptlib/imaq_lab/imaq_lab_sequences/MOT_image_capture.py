from labscript import start, stop
from labscriptlib.imaq_lab.connection_table import ConnectionTable

ConnectionTable()

start()

# Trigger both Spinnaker cameras simultaneously at t = 0.5 s
t = 0.5

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

# Leave enough time for the acquisitions to complete
stop(1.0)
