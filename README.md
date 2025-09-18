# Openpnp Feeder Alignment

This is a set of scripts for openpnp which implement a control loop for feeder pick position
using bottom vision.

Various openpnp feeder use top vision to control the pick position. Using the top vision
may involve looking at sprocket holes or feeder fiducials.

These scripts implement a different method. Part of the normal pick and place cycle
involves inspecting the part using *bottom* vision to determine precise alignment. From
this precise alignment data we can glean some information for correcting the next pick
from the same feeder. Note that the pick location needs to have been configured with
sufficient accuracy to allow the first pick to complete; but this new control loop
can fine tune the pick location and keep it it accurate if the tape wanders.

This version currently works with ReferencePushPull feeder, and it assumes that the
vision features provided by that class have been disabled. Unfortunately there is no
feeder API to adjust the pick location, so class-specific customisation will be needed
for other types of feeder.

This requires openpnp test branch version from 20205-09-18 or later.
