# Illustration of how to use BlenderVR OSC API

import blendervr
import os

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        __slots__ = {
                "_initialized",
                "OSC",
                "_osc_user",
                "_user",
                "_user_name",
                }

        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            # to setup temple in the first run()
            self._initialized = False

            # headtracked user (that controls the flashlight and rocks)
            self._user_name = 'user A'
            self._user = None
            self._osc_user = None

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

        def start(self):
            """
            BlenderVR Callback, called at BlenderVR start.
            """
            self.logger.debug("## Start my Processor")
            if self.BlenderVR.isMaster():
                try:
                    # get access to BlenderVR OSC API
                    self.OSC = self.BlenderVR.getPlugin('osc')

                    try: # check if OSC client is available
                        osc_isAvailable = self.OSC.isAvailable()
                        self.logger.debug('OSC Client is available:', osc_isAvailable)

                    except AttributeError: # i.e. plugin self.OSC not instantiated
                        self.logger.warning('OSC plugin not/badly defined in configuration file -> OSC disabled')

                    else:
                        # Print current blendervr users <-> osc users mapping
                        osc_users_dict = self.OSC.getUsersDict()
                        self.logger.debug('Current OSC mapping (OSC user ... is attached to BlenderVR user ...):')
                        for listener_name in osc_users_dict.keys():
                            osc_user = osc_users_dict[listener_name]
                            bvr_user = osc_user.getUser()
                            if bvr_user: self.logger.debug('-', osc_user.getName(), '<->', bvr_user.getName())
                            else:  self.logger.debug('-', osc_user.getName(), '<->', None)

                        # Define OSC users parameters
                        osc_user = self.OSC.getUser('Binaural 1')
                        osc_user.start(True) # OSC msg: '/user 1 start 1'
                        osc_user.mute(False) # OSC msg: '/user 1 mute 0'
                        osc_user.volume('%80') # OSC msg: '/user 1 volume %80'
                        # or equivalently, see .xml configuration

                        self._osc_user = osc_user # we pass this to the main python scripts

                except:
                    # this try/except using self.logger.log_traceback(False) is the best way
                    # to trace back errors happening on console/master/slaves in BlenderVR.
                    # Without it, some errors won't be printed out in either windows (console's nor master's nor slave's).
                    self.logger.log_traceback(False)

                # handle users to control the Temple Demo
                self._user = self.BlenderVR.getUserByName(self._user_name)

        def run(self):
            """
            BlenderVR Callback, called every frame.
            """
            self._setupTemple()
            bge.logic.temple.run()

        def keyboardAndMouse(self, info):
            """
            Debug input entry, to be replaced by individual callbacks
            for each of the events (flashlight, sonar, rock)
            """
            from blendervr.player import device
            temple = bge.logic.temple

            _valid_state = {device.STATE_PRESS,}

            if not info.get('key'):
                return

            if info['key'] == ord('1') and info['state'] in _valid_state:
                temple.io.flashlightButton()

            elif info['key'] == ord('2') and info['state'] in _valid_state:
                temple.io.sonarButton()

            elif info['key'] == ord('3') and info['state'] in _valid_state:
                temple.io.rockButton()

        def quit(self):
            """
            BlenderVR Callback, called at run stop.
            """
            if self.BlenderVR.isMaster():
                try:
                    ## it seems that reset flag is updated but
                    ## that the associated callback (run) is killed before
                    ## it can actually update anything
                    # self.OSC.getGlobal().reset()

                    # this works :)
                    self.OSC.reset() # sends "/global reset" OSC msg
                    self.logger.debug("## Quit my Processor")
                except:
                    self.logger.log_traceback(False)

        def _setupTemple(self):
            if self._initialized:
                return

            if hasattr(bge.logic, "temple"):
                temple = bge.logic.temple

                user = self._user

                # use head tracking instead of mouse to
                # control flashlight and rock thrower
                temple.io.enableHeadTrack(user)

                temple.sound.setOSCUser(self._osc_user)

            else:
                self.logger.error('Missing temple scripts')
                self.BlenderVR.quit()

            self._initialized = True


elif blendervr.is_creating_loader():
    import bpy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, creator):
            super(Processor, self).__init__(creator)


elif blendervr.is_console():
    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, console):
            global try_wait_user_name, try_chooser, try_console_arc_balls
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True
