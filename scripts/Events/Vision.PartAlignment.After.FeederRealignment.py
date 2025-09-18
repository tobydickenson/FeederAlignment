import sys,json,traceback,os.path,datetime
from org.openpnp.spi.base import AbstractPnpJobProcessor


enable_pushpull_adjustment = True

verbose = True

def main():
    if not offsets:
        return

    logfile = os.path.abspath(os.path.join(scripting.getScriptsDirectory().toString(),'..','alignment.log'))
    now_str = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    a = get_ob('pre_alignment_rotation_offset',0)
    l = offsets.location
    pick_rotation = nozzle.getRotationModeOffset()-a
    if verbose:
        print 'pre-align rotation offset',a
        print 'post-align rotation offset',nozzle.getRotationModeOffset()
        print 'nozzle rotation',nozzle.getLocation().getRotation()
        print 'pick rotation',pick_rotation
    #
    if False:
        line = '%s,%s,%.3f,%.3f,%.3f,%.3f,%s\n'%(
               now_str,part.getId(),l.x,l.y,l.rotation,pick_rotation,offsets.getPreRotated())
        f = open(logfile,'a')
        f.write(line)
        f.close()
    #
    footprint = part.getPackage().getFootprint()
    width,height = footprint.getBodyWidth(), footprint.getBodyHeight()
    if 0.05<width<1.4 or 0.05<height<1.4:
        # do auto adjust on narrow parts only
        if abs(pick_rotation)<1.5:
            pick_rotation += nozzle.getLocation().getRotation()
            adjust(offsets.location.rotateXy(-pick_rotation))
        else:
            if verbose:
                # If it is rotated when being picked onto the nozzle, there is a problem
                # because we dont know the center point of the rotation. It almost certainly
                # will have rotated about a point on the circumference of the nozzle, but we dont
                # know which point. So we only perform this adjustment if there was no rotation.
                print 'pick rotation too large for adjustment'

def adjust(correction):
    if part is None:
        return
    feeder = nozzle.getPartsFeeder()
    if feeder is None:
        if verbose:
            print 'no feeder'
        return
    feeder_name = feeder.getName()
    feeder_name = feeder_name.split()[0] # Use the name up to the first space
    #
    # Only do one adjustment for each pick
    if not get_ob('feeder_adjust_latch:'+feeder_name,0):
        if verbose:
            print feeder_name,'already adjusted'
        return
    set_ob('feeder_adjust_latch:'+feeder_name,0)
    #
    class_name = feeder.getClass().getSimpleName()
    if class_name=='ReferencePushPullFeeder':
        adjust_pushpull(correction,feeder,feeder_name)

def adjust_pushpull(correction,feeder,feeder_name):
    rotation_on_machine = feeder.getPickLocation(0,None).rotation
    if verbose:
        print 'rotation on machine',rotation_on_machine,'in feeder',feeder.rotationInFeeder
    original_feeder_location = feeder.location
    if verbose:
        print 'original feeder location',original_feeder_location
    correction.rotateXy(rotation_on_machine) # validation still required here
    correction.rotateXy(feeder.rotationInFeeder)
    if verbose:
        print 'correction',correction
    #
    measured_feeder_location = original_feeder_location.add(correction)
    if verbose:
        print 'location was',original_feeder_location
        print 'measured location',measured_feeder_location
    distance = original_feeder_location.getLinearDistanceTo(measured_feeder_location)
    if verbose:
        print 'measured distance',distance
    if distance>2:
        print 'Calculated error is too large %.2f mm'%(distance,)
        return
    #
    position_tweak_count = get_ob('position_tweak_count:'+feeder_name,0)
    factor = 1.0/min(20,position_tweak_count+1)
    if verbose:
        print 'factor',factor
    applied_correction = correction.multiply(factor)
    corrected_feeder_location = original_feeder_location.add(applied_correction)
    if verbose:
        print 'corrected location',corrected_feeder_location
    distance = original_feeder_location.getLinearDistanceTo(corrected_feeder_location)
    if verbose:
        print 'correction distance',distance
    print feeder_name+' pick location moved %.3f mm'%(distance,), applied_correction
    if enable_pushpull_adjustment:
        set_ob('position_tweak_count:'+feeder_name, position_tweak_count+1)
        feeder.setLocation(corrected_feeder_location)

def set_ob(name,value):
    config.scriptState.put(name,json.dumps(value))

def get_ob(name,default):
    if config.scriptState.has_key(name):
        return json.loads(config.scriptState.get(name))
    else:
        return default

try:
    main()
except:
    traceback.print_exc(file=sys.stdout)
    print 'python traceback above'
    raise

