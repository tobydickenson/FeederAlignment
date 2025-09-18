import sys,os.path,traceback,json
from javax.swing.JOptionPane import showInputDialog,QUESTION_MESSAGE

def main():
    tweak()

def tweak():
    names = ['All']
    #
    for feeder in machine.getFeeders():
        class_name = feeder.getClass().getSimpleName()
        feeder_name = feeder.getName().split()[0]
        count = get_ob('position_tweak_count:'+feeder_name,0)
        if count:
            names.append(feeder_name)
    #
    title = 'Location Realignment'
    message = 'Restart which feeder?'
    default = 'All'
    choice = showInputDialog(gui,message,title,QUESTION_MESSAGE,None,names,default)
    #
    for feeder in machine.getFeeders():
        class_name = feeder.getClass().getSimpleName()
        feeder_name = feeder.getName().split()[0]
        if feeder_name==choice:
            set_ob('position_tweak_count:'+feeder_name,0)
    #
    if choice=='All':
        delete_prefix('position_tweak_count:')


def set_ob(name,value):
    config.scriptState.put(name,json.dumps(value))

def get_ob(name,default):
    if config.scriptState.has_key(name):
        return json.loads(config.scriptState.get(name))
    else:
        return default

def delete_prefix(name_prefix):
    for key in config.scriptState.keys():
        if key.startswith(name_prefix):
            config.scriptState.remove(key)

try:
    main()
except:
    traceback.print_exc(file=sys.stdout)
    print 'python traceback above'
    raise
