import yaml, os, datetime, time


class Utils(object):

    def __init__(self):
        self.w, self.h, self.channels = self.get_channels()
        self.get_window_ids()
        self.config_file_name = "config.yaml"
        self.config_keys = [ "minimize_other_windows", "always_on_top" ]
        self.config = self.get_config()

    def write_config_file(self, config):
        try: yaml.dump(config, open(self.config_file_name, 'w'), default_flow_style=False)
        except: print("Writing the config file failed - issue ignored")

    def get_config(self):
        if not os.path.isfile(self.config_file_name):
            print("Config file does not exist - will use defaults")
            config = {}
            for key in self.config_keys:
                config[key] = False
            self.write_config_file(config)
            return config
        try:
            ok = True
            config_from_file = yaml.load(open(self.config_file_name))
            for key in self.config_keys:
                if not key in config_from_file.keys():
                    print("The config file '"+ self.config_file_name +"' does not include key "+ key)
                    ok = False
            config_file_ok = ok
        except:
            config_file_ok = False
        if not config_file_ok:
             print("The config file '"+ self.config_file_name +"' exists, but is not valid - Aborting.")
             exit()
        return config_from_file

    def set_config_key(self, var_name, value):
        if var_name not in self.config_keys:
             print("ERROR: tryied to set config key '"+var_name+"' but this key does not exist - Aborting")
             exit()
        self.config[var_name] = value
        self.write_config_file(self.config)
        print("Config key '"+ var_name +"' was set to '"+ str(value) +"'")

    def get_window_size_and_position(self, id=None):
        values = { }
        if id==None:
            cmd = "xwininfo -root"
        else:
            cmd = "xwininfo -id "+ id
        ans = os.popen(cmd).read()
        #print(ans)
        names = { "Width": "w", "Height": "h" }
        names["Absolute upper-left X:"] = "x"
        names["Absolute upper-left Y:"] = "y"
        for l in ans.split("\n"):
            if not l: continue
            ll = l.split()
            for name in names:
                if name in l:
                    values[ names[name] ] = int(l.split()[-1])
        return values

    def get_window_ids(self):
        def get_ids():
            cmd = 'xdotool search --all --onlyvisible --class "vlc"'
            ids = os.popen(cmd).read().split("\n")
            for id in ids:
                if not id: continue
                win_title = os.popen("xdotool getwindowname "+ id).read().strip()
                for channel in list(self.channels.keys()):
                    if channel in win_title:
                        self.channels[channel]["id"] = id
        print ("1 start get_window_ids", datetime.datetime.now() )
        get_ids()
        all_ids_present = True
        for channel in list(self.channels.keys()):
            if not "id" in self.channels[channel].keys():
                print("    Missing id for channel '"+ channel +"' - will try again")
            get_ids()
        print ("3 end get_window_id", datetime.datetime.now() )
        
    def launch_channel(self, ch):
        url = self.channels[ch]["url"]
        cmd  = 'nohup vlc --qt-minimal-view --no-fullscreen '
        cmd += '--meta-title "'+ ch +'" '+ url +' &'
        os.system(cmd)
        self.get_window_ids()
        #os.popen(cmd)

    def close_channel(self, ch):
        pid = os.popen("ps ax | grep vlc | grep '"+ ch +"'").read().strip().split()[0]
        print(ch, pid)
        cmd  = 'kill '+ pid
        os.popen(cmd)

    def xdo(self, cmd):
        print("    xdotool cmd:", cmd)
        time.sleep(0.1)
        ans = os.popen("xdotool "+ cmd).read()
        if ans:
            print("ERROR: Execution of xdotool cmd '"+ cmd +"' failed")
            print("   msg:", ans.strip())
            exit()

    def position_screen(self, channel):
        id = self.channels[channel]["id"]
        print("Moving and resizing channel '"+ channel +"' with id ", id)
        #print ("4 enter pos", datetime.datetime.now() )
        self.xdo(' windowraise '+ id)
        screen_size_pos = self.get_window_size_and_position()
        sp = self.get_window_size_and_position(id)
        #self.xdo("set_window --overrideredirect 1 "+ id +" windowunmap "+ id +" windowmap "+ id) 
        #self.xdo("windowsize "+ id +" 100 100")
        #exit()
        print("    window pos/size:", sp)
        if sp["y"]==0:
             print("    Windows is full size (borderless)- will double-click to exit full-size")
             self.xdo("mousemove --window "+ id +" "+ x +" "+ y)
             self.xdo("click --window "+ id +" --delay 10 --repeat 2 1")
             sp = self.get_window_size_and_position(id)
        if sp["y"]<100:
            # Probably we need to move the win down, so move/resize will work
            #put the mouse in the middle of the window top bar
            print("    Windows is still full size - will move it down, to enable move/resize")
            x = str( int(sp["x"]+sp["w"]*0.5) )
            y = str( int(sp["y"])-10 )
            if int(y)<1: y = "1"
            x = str( int(sp["x"]+14) )
            y = str( int(sp["y"]-10) )
            self.xdo("mousemove --sync "+ x +" "+ y)
            self.xdo("click 1")
            time.sleep(0.1)
            self.xdo('key "m"')
            y = str( int(screen_size_pos["h"]-40) )
            self.xdo("mousemove --sync "+ x +" "+ y)
            self.xdo("click 1")
        #y = str( 200 )
        #time.sleep(1)
        #self.xdo("mousedown --window "+ id +" 1")
        #time.sleep(10)
        #self.xdo("mousemove --sync "+ x +" "+ y)
        #self.xdo("mouseup   --window "+ id +" 1")
        sp = self.get_window_size_and_position(id)
        print(">>>>>", screen_size_pos, sp)
        print ("7 art two get size", datetime.datetime.now() )
        h = str(self.h); w = str(self.w)
        self.xdo('windowsize '+ id +' '+ w +' '+ h)
        print ("8", datetime.datetime.now() )
        print("    After resize size:", self.get_window_size_and_position(id))
        x = str(self.channels[channel]["x"]); y = str(self.channels[channel]["y"])
        self.xdo('windowmove '+ id +' '+ x +' '+ y)
        print ("5", datetime.datetime.now() )
        return
        exit() 
        if sp["x"]>screen_size_pos["x"]-100 \
           and sp["y"]>screen_size_pos["y"]-100:
             # Window is full screen. Some WM won't allow resize and move
             # So, we will manually resize it (=Alt pressed and mouse moved)
             print("CCC")
             x = str( int(sp["x"]+sp["w"]*0.1) )
             y = str( int(sp["y"]+sp["h"]*0.1) )
             self.xdo("mousemove --window "+ id +" "+ x +" "+ y)
             x = str( int(sp["x"]+sp["w"]*0.9) )
             y = str( int(sp["y"]+sp["h"]*0.9) )
             self.xdo("keydown --window "+ id +" Alt_L")
             self.xdo("mousedown --window "+ id +" 3")
             self.xdo("mousemove --window "+ id +" "+ x +" "+ y)
             self.xdo("mouseup --window "+ id +" 2")
             self.xdo("keyup --window "+ id +" Alt_L")
             exit()
        ans = os.popen('xdotool windowmove '+ id +' 10 10').read() # move sometimes fails when pos is 0,0
        print ("5 aft mov pos", datetime.datetime.now() )
        if ans:
            print("    Error while moving:"+ str(ans).strip())
        print ("6 bfr two get size", datetime.datetime.now() )
        screen_size_pos = self.get_window_size_and_position()
        window_size_pos = self.get_window_size_and_position(id)
        print("    Whole screen:", self.get_window_size_and_position())
        print("    Before resize:", self.get_window_size_and_position(id))
        print ("7 art two get size", datetime.datetime.now() )
        h = str(self.h); w = str(self.w)
        os.system('xdotool windowsize '+ id +' '+ w +' '+ h)
        print ("8", datetime.datetime.now() )
        print("    After resize size:", self.get_window_size_and_position(id))

        x = str(self.channels[channel]["x"]); y = str(self.channels[channel]["y"])
        os.system('nohup xdotool windowmove '+ id +' '+ x +' '+ y +" &")
        print ("5", datetime.datetime.now() )

        exit()
          #ans = os.popen('xdotool windowmove '+ id +' '+ x +' '+ y).read()
          #if ans:
          #    print("    Error while moving:"+ str(ans).strip())
          #h = str(self.h); w = str(self.w)
          #ans = os.popen('xdotool windowsize '+ id +' '+ w +' '+ h).read()
          #if ans:
          #    print("    Error while resizing:"+ str(ans).strip())

    def _calculate(self, key, s, h, w):
        if type(s)==type(0):
            return s
        if type(s)!=type(""):
            msg  = "calculate: Unexpected parameter type: "
            msg += str(type(s)) +" for paramter: "+str(s) +" - Aborting"
            print(msg)
            exit()
        s = s.replace("w", str(w)).replace("h",str(h))
        ok_chars = "0123456789+-*/rtp:.@"
        not_ok_chars_in_s = [ c for c in s if c not in ok_chars ]
        if len(not_ok_chars_in_s):
            msg  = "calculate: The following chars are present in the paramter"
            msg += ", but not allowed: "+ str(not_ok_chars_in_s) +"- aborting." 
            print(msg)
            exit()
        if key=="url":
            return s
        else:
            return eval(s)

    def get_channels(self):
        channels = yaml.load(open("channels.yaml"))
        w = channels["w"]
        del channels["w"]
        h = int( float(w) *9. / 16. )
        for ch in list(channels.keys()):
            channel = channels[ch]
            for param in list(channel.keys()):
                #print channel[param], calculate(channel[param], h, w)
                channel[param] = self._calculate(param, channel[param], h, w)
        return w, h, channels
