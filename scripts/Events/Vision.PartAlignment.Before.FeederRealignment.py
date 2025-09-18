import sys,traceback,json

def main():
    set_ob('pre_alignment_rotation_offset',nozzle.getRotationModeOffset())

def set_ob(name,value):
    config.scriptState.put(name,json.dumps(value))

try:
    main()
except:
    traceback.print_exc(file=sys.stdout)
    print 'python traceback above'
    raise

