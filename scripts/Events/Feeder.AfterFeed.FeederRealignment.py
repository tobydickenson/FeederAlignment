import sys,traceback,json

def main():
    feeder_name = feeder.getName()
    set_ob('feeder_adjust_latch:'+feeder_name, 1)

def set_ob(name,value):
    config.scriptState.put(name,json.dumps(value))

try:
    main()
except:
    traceback.print_exc(file=sys.stdout)
    print 'python traceback above'
    raise

