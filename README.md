digital-TV-multi-view
======================

With this software you can watch all the IDAN+ (the Israeli Digital TV) channels at once, using a cheap DVB-T USB stick. However, the software can be easily modified to view any other DTT service. 

This software was written and tested on Ubuntu 18.04, and will probably run on any modern Linux system. It won't run on Windows.

Running the system
------------------

   1. Open a terminal and run the command `run_dvblast`
      You can minimize this window. 
   2. In a new window, run the command `./control_panel`. This will open a new, small window.
      You may want to check the option 'Always on top'
   3. In the 'control panel' window, press on 'Launch Screens'. 
      This will launch VLC screens that will show all the channels.
   4. In the 'control panel' window, press on 'Position Screens'.
      This will arrange the video-screens in a compact way.
   5. Focus on each video-screen and press the keyboard key 'M'. 
      This will mute or un-mute each screen. I normally mute all screens and then un-mute the screen I would like to watch.
   
Troubleshooting
---------------

   1. Verify that the DVB-T stick is present and configured correctly:
      In terminal, execute: `ls /dvb/adapter0`, to see if this directory exists.
      If the directory exist, the DVB-T stick is OK.
   2. Verify you receive the signal:
      If the signal is received, you will see that when you run dvblast, all the names of the channels will be listed after few seconds.
   3. Dvblast sends the video using multicast. Here are some tips related to multicast:
      1. The lo (loop) network interface should have multicast enabled.
          Test: issue the command `ifconfig lo` and look for 'MULTICAST' in the first line of the output.
          Fix: Issue the command `ifconfig lo multicast`
      2. Multicast should be routed inside the computer. 
          Test: Issue the command `ip route get 239.255.0.1`. The command should report 'lo' at the end
              Another test: Issue the command: `tcpdump -i lo udp`. You should see many lines scrolling fast.
          Fix: Issue the command `sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev lo`
 

Installing dependencies
-----------------------

- Hardware: Cheap DVB-T USB stick, sometimes called RTL-SDR. Normally it comes with an antenna, which should be connected. An example: https://www.aliexpress.com/item/32611302317.html for $4, but there are many others. If you buy such a device, it is probably worth it to invest a bit more and buy one that supports DVB-T2.
- Drivers for the RTL-SDR are needed, but will not be described here. The way to know if you have the needed drivers is the plug your DVB-T stick in and look for the directory /dvb/adapter0. If it is there, you are set.
- Install python packages:
   `apt install python3-tk vlc`
- Install dvblast
  Download this software from https://code.videolan.org/videolan/dvblast and install according to the 'INSTALL' file, which is part of the dvblast package.
  The file 'run_dvblast' expects the executable 'dvblast' to be present under ./dvblast-3.4'. 
Modifying the software for TV in other countries
------------------------------------------------
This section is not written yet, however, here are some tips:

   - Find the frequency of DVB-T used in your area. 
     You will need to change this frequency in the 'run_dvblast' (instead of the current value '514000000')
   - Edit the file 'dvblast.conf'. and change the one-before-last field, which is the SID (the SID is reported by dvblast)
     An alternative to finding the SIDs is using the utility 'dvbsnoop'
   - Also, look at the file 'do_scan' to get examples of how to scan for the channels.
   - Change the channel names at the 'channels.yaml' file.


## Author

**Shalom Mitz** - [shalommmitz](https://github.com/shalommmitz)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE ) file for details.
   
