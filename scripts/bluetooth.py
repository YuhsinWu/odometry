#!/usr/bin/env python

## @package docstring
#  This package provides the bridge between Bluetooth and ROS, both ways.
#  Initially it receives "String" messages and sends "String" messages
#

import sys
import signal
import bluetooth
import select
import time
from std_msgs.msg import String
#from ocean.depths import Cthulhu

#--------------------------------- Constants ----------------------------------#

TAG       = "Bluetooth Bridge Node:"              ## Node verbosity tag

#------------------------------------------------------------------------------#
## Application class
#
class Application:
    ## "Is application running" flag
    is_running   = True
    ## "Is connection established" flag
    is_connected = False

    ## Bluetooth channel
    bt_channel = 22                             # IMPORTANT! Mae sure this is THE SAME
                                                # as was used diring
                                                # sdptool add --channel=<number> SP comand.
                                                # Also, use this command before launching
                                                # this node if you have rebooted your robot.

    ## Init function
    def __init__(self):
        # Assigning the SIGINT handler
        signal.signal(signal.SIGINT, self.sigint_handler)

        time.sleep(0.5)

        while self.is_running:
            try:
                # Starting the bluetooth server
                self.server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                # Listening for incoming connections
                self.server_sock.bind( ("", self.bt_channel) )
                print TAG, "Waiting for incoming connections on port %d ..." % self.bt_channel
                self.server_sock.listen(1)
                # Accepting incoming connection
                self.client_sock, self.address = self.server_sock.accept()
                print TAG, "Accepted connection from ", self.address

                # [IMPORTANT] THIS IS HOW TO RECEIVE MESSAGE FROM BLUETOOTH
                # AND PUBLISH IT TO ROS

                # Running the loop to receive messages
                self.is_connected  = True
                while self.is_running:
                    ready = select.select([self.client_sock],[],[], 2)
                    if ready[0]:
                        data = self.client_sock.recv(1024)
                        print TAG, "Received: ", data
                        self.pub.publish(data)

            except Exception, e:
                self.is_connected = False
                self.server_sock.close()
                print TAG, "EXCEPTION:", str(e)
                self.status_pub.publish("EXCEPTION: "+str(e))
                print TAG, "RESTARTING SERVER"
                time.sleep(0.1)

    ## SIGINT Signal handler, you need this one to interrupt your node
    def sigint_handler(self, signal, frame):
            print ""
            print TAG,"Interrupt!"
            self.status_pub.publish("SIGINT")
            self.is_running = False
            print TAG,"Terminated"
            sys.exit(0)

    ## [IMPORTANT] THIS IS HOW TO SEND MESSAGES VIA BLUETOOTH
    ## Handler for the messages to be sent via bluetooth.
    def send_callback(self, message):
        if self.is_connected:
            print TAG, "Sending:", message.data
            self.client_sock.send(message.data+"\n")

#------------------------------------- Main -------------------------------------#

if __name__ == '__main__':
    print TAG,"Started"

    app = Application()

    print TAG,"Terminated"




