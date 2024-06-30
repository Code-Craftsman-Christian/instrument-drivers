# This Device Class is published under the terms of the MIT License.
# Required Third Party Libraries, which are included in the Device Class
# package for convenience purposes, may have a different license. You can
# find those in the corresponding folders or contact the maintainer.
#
# MIT License
# 
# Copyright (c) 2022-2024 SweepMe! GmbH (sweep-me.net)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# SweepMe! driver
# * Module: Robot
# * Instrument: Dobot MG400

from FolderManager import addFolderToPATH
addFolderToPATH()

import dobot_api
# import importlib 
# importlib.reload(dobot_api)

import time
import select

from pysweepme.ErrorMessage import error, debug

from pysweepme.EmptyDeviceClass import EmptyDevice


class Device(EmptyDevice):

    description =   """
                    <p>This driver can be used to control x, y, z and r (rotation) of a Dobot MG400 tabletop robot.</p>
                    <p>&nbsp;</p>
                    <p><strong>Requirements</strong>:</p>
                    <ul>
                    <li>To use this driver, you need to update the robot firmware to 1.5.4 or higher. The driver has been tested with firmware version 1.5.6.</li>
                    <li>The MG400 has two Ethernet ports. The first one uses fixed IP address being 192.168.1.6 and the second one has a variable IP address that is 192.168.2.6 as factory default.<br />To connect with the robot your computer needs a static IP address that can be set via Windows network connetions. Right click on your Ethernet network adapter -&gt; 'Properties' -&gt; Tab 'Network' -&gt; 'Internet protocol version 4 (TCP/IPv4) -&gt; button 'Properties'. Select static IP address and 255.255.255.0 as subnet mask. Use an address that is different from the one of the robot but in the same sub net mask, e.g. "192.168.1.5" if you use the first ethernet port.<br /><br /></li>
                    </ul>
                    <p><strong>Usage:</strong></p>
                    <ul>
                    <li>Insert numbers into the Axes fields x, y, z, r. For more complex procedures, use the parameter syntax {...} to handover values from other fields.</li>
                    <li>If the object attached to robot is heavy, one should set the payload mass and eventually the eccentric distance of the object.</li>
                    <li>The Robot module works best in combination with add-on modules such as "ReadValues" or "TableValues" where you create a list of x, y, z, r values that you handover to the Robot module using the parameter syntax {...}</li>
                    <li>Home position is fixed at x = 350 mm, y = 0 mm, z = 0 mm, r = 0 mm<br />&nbsp;</li>
                    </ul>
                    <p><strong>Coordinates:</strong></p>
                    <ul>
                    <li>Home position: x = 350.0 mm, y = 0.0 mm, z = 0.0 mm, r = 0&deg;</li>
                    <li>x: horizonal direction of the robot arm in the home position</li>
                    <li>y: horizontal direction perpendicular to y</li>
                    <li>z: vertical direction perpendicular to x and y&nbsp;</li>
                    <li>r: Rotation angle in &deg; (0.0 to 720.0)</li>
                    </ul>
                    <p>&nbsp;</p>
                    <p><strong>Parameters:</strong></p>
                    <ul>
                    <li>'Go home at start' moves the robot at the beginning of a run to the fixed home position.</li>
                    <li>'Go hame at end' move the robot at the end of a run to the fixed home position.</li>
                    <li>Global speed factor affects all moves: 1-100</li>
                    <li>Acceleration factor: 1-100<br />&nbsp;</li>
                    <li>Speed factor is the speed of a linear move in the range 1-100. It can be changed at each step using the parameter syntax.</li>
                    </ul>
                    <p><strong>Caution:</strong></p>
                    <ul>
                    <li>The home position is fixed and independent from an individual position set in Dobot Studio Pro, so please check whether Go home before or after the run works for you.</li>
                    </ul>
                    """
                    
    axes = {
            "x": {
                "Value": 350.0
                },
            "y": {
                "Value": 0.0
                },
            "z": {
                "Value": 0.0
                },   
            "r": {
                "Value": 0.0
                },
            }

    def __init__(self):
    
        EmptyDevice.__init__(self)
        
        self.shortname = "MG400"  # short name will be shown in the sequencer
            
        self.reach_position_timeout = 30.0
            
    def set_GUIparameter(self):

        gui_parameter = {
                        "Port": "192.168.1.6",  # Standard IP of first Ethernet port
                        "Unit": ["mm"],
                        # "Reach position": True,
                        "Collision level": ["5", "4", "3", "2", "1", "0"],
                        "Acceleration factor": 10,
                        "Global speed factor": 100,
                        "Speed factor": "10",
                        "": None,
                        "Payload": None,
                        "Payload weight in kg": 0.0,
                        # "Payload inertia in kgm²": 0.0,
                        "Payload x offset": 0.0,
                        "Payload y offset": 0.0,
                        # "Payload z offset": 0.0,
                        " ": None,
                        "Jump": None,
                        "Use jump mode": False,
                        "Movement height": 0.0,
                        "  ": None,

                        "GoHomeStart": True,
                        "GoHomeEnd": True,
                        }
        
        return gui_parameter

    def get_GUIparameter(self, parameter):
    
        self.port_string = parameter["Port"]

        self.length_unit = parameter["Unit"]
        # self.reach_position = parameter["Reach position"]
        self.go_home_start = parameter["GoHomeStart"]
        self.go_home_end = parameter["GoHomeEnd"]
        
        self.payload_weight = parameter["Payload weight in kg"]
        # self.payload_inertia = parameter["Payload inertia in kgm²"]
        self.payload_x_offset = parameter["Payload x offset"]
        self.payload_y_offset = parameter["Payload y offset"]
        # self.payload_z_offset = parameter["Payload z offset"]
        self.collision_level = parameter["Collision level"]

        self.acceleration_factor = parameter["Acceleration factor"]
        self.global_speed_factor = parameter["Global speed factor"]
        self.speed_factor = parameter["Speed factor"]

        self.use_jump_mode = parameter["Use jump mode"]
        self.movement_height = parameter["Movement height"]
        
        self.variables = ["x", "y", "z", "r"] 
        self.units = [self.length_unit] * 3 + ["°"]
        self.plottype = [True] * len(self.variables)
        self.savetype = [True] * len(self.variables)
        
    def connect(self):
        
        port_api_dashboard = 29999
        port_api_move = 30003
        
        self.api_dashboard = DobotDashboard(self.port_string, port_api_dashboard)
        self.api_move = DobotMove(self.port_string, port_api_move)

    def disconnect(self):
    
        if hasattr(self, "api_dashboard"):
            self.api_dashboard.close()
        if hasattr(self, "api_move"):
            self.api_move.close()
        
    def initialize(self):

        self.clear_error()
        # self.reset_robot()

        self.set_collision_level(self.collision_level)

        # first without any parameters. Otherwise the robot tend to throw error 105 "Servo on failed"
        self.enable_robot()
        self.enable_robot(self.payload_weight, self.payload_x_offset, self.payload_y_offset, 0.0)
        # self.set_payload(self.payload_weight, self.payload_inertia)
        if self.go_home_start:
            self.go_home()
        
    def deinitialize(self):

        if self.go_home_end:
            self.go_home()
            
        self.disable_robot()

    def configure(self):

        self.movement_height = float(self.movement_height)
        self.set_acceleration_linear(self.acceleration_factor)  # Linear acceleration factor 1-100
        self.set_speed_global(self.global_speed_factor)  # Global speed factor 1-100
        self.set_speed_linear(self.speed_factor)  # Linear speed factor 1-100
        # self._last_xyzr = (None, None, None, None)
        self._last_xyzr = self.get_position()

    def unconfigure(self):

        if self.use_jump_mode:
            self.move_linear(self._last_xyzr[0], self._last_xyzr[1], self.movement_height, self._last_xyzr[3])
            self.sync(self.reach_position_timeout)

        mode = self.get_robot_mode()
        # todo: check for errors

    def reconfigure(self, parameters, keys):

        # print("reconfigure", parameters)

        if "Speed factor" in keys:
            self.speed_factor = parameters["Speed factor"]
            self.set_speed_linear(self.speed_factor)  # Linear speed factor 1-100

    def apply(self):
    
        # print(self.sweepvalues)

        # Position
        if "x" in self.sweepvalues and self.sweepvalues["x"] != "nan":
            x = float(self.sweepvalues["x"])
        else: 
            x = self._last_xyzr[0]
            
        if "y" in self.sweepvalues and self.sweepvalues["y"] != "nan":
            y = float(self.sweepvalues["y"])
        else: 
            y = self._last_xyzr[1]

        if "z" in self.sweepvalues and self.sweepvalues["z"] != "nan":
            z = float(self.sweepvalues["z"])
        else: 
            z = self._last_xyzr[2]
                    
        if "r" in self.sweepvalues and self.sweepvalues["r"] != "nan":
            r = float(self.sweepvalues["r"])   
        else: 
            r = self._last_xyzr[3]     

        # print(x,y,z,r)
                    
        if self._last_xyzr != (x, y, z, r):

            if self.use_jump_mode:

                # we only move to movement height if x, y, or r change
                # in case of a z scan, we do not need to go back to movement height
                if self._last_xyzr[0, 2] != (x, y) or self._last_xyzr[3] != r:

                    # vertical move to movement height
                    self.move_linear(self._last_xyzr[0], self._last_xyzr[1], self.movement_height, self._last_xyzr[3])
                    self.sync(self.reach_position_timeout)

                    # lateral move at movement height
                    self.move_linear(x, y, self.movement_height, r)
                    self.sync(self.reach_position_timeout)

            self.move_linear(x, y, z, r)
            self._last_xyzr = (x, y, z, r)

    def reach(self):
        # if self.reach_position:
        self.sync(self.reach_position_timeout)  # wait to finish all commands in queue
                    
    def call(self):
        x,y,z,r = self.get_position()
        return x,y,z,r

    def enable_robot(self, *args):
        self.api_dashboard.EnableRobot(args)
        
    def disable_robot(self):
        self.api_dashboard.DisableRobot()
        
    def clear_error(self):
        self.api_dashboard.ClearError()
        
    def reset_robot(self):
        self.api_dashboard.ResetRobot()
        
    def set_payload(self, weight, inertia):
        self.api_dashboard.PayLoad(float(weight), float(inertia))
        
    def set_collision_level(self, level):
        self.api_dashboard.SetCollisionLevel(level)
        
    def set_speed_global(self, factor):
        self.api_dashboard.SpeedFactor(int(float(factor)))  # Global speed factor 1-100
        
    def set_speed_linear(self, speed):
        self.api_dashboard.SpeedL(int(float(speed)))

    def set_acceleration_linear(self, acc):
        self.api_dashboard.AccL(int(float(acc)))

    def get_robot_mode(self):
        mode = self.api_dashboard.RobotMode()
        return mode
        
    def move_linear(self, x,y,z,r):
        self.api_move.MovL(x,y,z,r)  # linear move to home position
        
    def go_home(self):
        self.move_linear(350.0, 0.0, 0.0, 0.0)  # linear move to home position
        self.sync()
                
    def sync(self, timeout=10.0):
        self.api_move.Sync(timeout) 
        
    def get_pose(self):
        answer = self.api_dashboard.GetPose()  # added function
        x,y,z,r = self.get_response_data(answer)[0:4]
        return x,y,z,r
      
    def get_position(self):
        return self.get_pose()
        
    def get_angles(self):
        answer = self.api_dashboard.GetAngle()
        a,b,c,r = answer
        return a,b,c,r

    @staticmethod
    def get_response_data(msg):
        lindex = msg.find("{")+1
        rindex = msg.find("}")
        data_string = msg[lindex:rindex]
        return data_string.split(",")


class DobotDashboard(dobot_api.DobotApiDashboard):

    # def log(self, text):
    #     pass
    #     print(text)

    def is_package_ready(self, timeout = 0.0):
        ready, _, _ = select.select([self.socket_dobot], [], [], timeout)
        return not not ready  # first "not" makes a bool, second "not" negates the bool to what is needed

    def send_data(self, string):
        # self.log(f"Send to 192.168.1.6:{self.port}: {string}")
        self.socket_dobot.send(str.encode(string, 'utf-8'))

    def wait_reply(self, timeout=3.0):
        """
        Read the return value
        """
        if self.is_package_ready(timeout=timeout):
            data = self.socket_dobot.recv(1024)
            data_str = str(data, encoding="utf-8")
            # self.log(f'Receive from 192.168.1.6:{self.port}: {data_str}')
            return data_str
        else:
            raise Exception("No package returned within timeout.")

    def EnableRobot(self, *args):
        """
        Enable the robot
        """
        # string = "EnableRobot({:f},{:f},{:f},{:f})".format(float(mass), float(x), float(y), float(z))
        # string = "EnableRobot({:f})".format(float(mass))
                
        if len(*args) == 0:
            string = "EnableRobot()"
        elif len(*args) == 1:
            string = "EnableRobot({:f})".format(float(*args[0]))
        elif len(*args) == 4:
            string = "EnableRobot({:f},{:f},{:f},{:f})".format(*tuple(map(float, *args)))
        else:
            raise Exception("EnableRobot() requires 0, 1, or 4 parameters")
            
        self.send_data(string)
        return self.wait_reply()

    def GetPose(self):
        """
        Retrieve position in cartesian coordinates
        """
        string = "GetPose()"
        self.send_data(string)
        return self.wait_reply()

    def GetAngle(self):
        """
        Retrieve angles of all joints
        """
        string = "GetAngle()"
        self.send_data(string)
        return self.wait_reply()

    def SetCollisionLevel(self, level):
        """
        Set the collision level
        collision level:
            0: switch off collision detection
            1~5: more sensitive with higher level
        """
        string = "SetCollisionLevel({:d})".format(int(level))
        self.send_data(string)
        return self.wait_reply()

    def ToolDO(self, index, status):
        """
        Set digital signal output at the robotic arm (Queue instruction). If you want to set the digital outputs at the
        back panel of the robot, use DO(index, status).
        index : Digital output index (Value range:1~2)
        status : Status of digital signal output port(0:Low level，1:High level
        """
        string = "ToolDO({:d},{:d})".format(index, status)
        self.send_data(string)
        return self.wait_reply()


class DobotMove(dobot_api.DobotApiMove):

    # def log(self, text):
    #     pass
    #     print(text)

    def is_package_ready(self, timeout = 0.0):
        ready, _, _ = select.select([self.socket_dobot], [], [], timeout)
        return not not ready  # first "not" makes a bool, second "not" negates the bool to what is needed

    def send_data(self, string):
        # self.log(f"Send to 192.168.1.6:{self.port}: {string}")
        self.socket_dobot.send(str.encode(string, 'utf-8'))

    def wait_reply(self, timeout=3.0):
        """
        Read the return value
        """
        if self.is_package_ready(timeout=timeout):
            data = self.socket_dobot.recv(1024)
            data_str = str(data, encoding="utf-8")
            # self.log(f'Receive from 192.168.1.6:{self.port}: {data_str}')
            return data_str
        else:
            raise Exception("No package returned within timeout.")
            
    def Sync(self, timeout = 10.0):
        """
        The blocking program executes the queue instruction and returns after all the queue instructions are executed
        """
        string = "Sync()"
        self.send_data(string)
        return self.wait_reply(timeout)
