#!/usr/bin/python

import sys

from st2actions.runners.pythonrunner import Action

class LoadConfiguration(Action):

    def run(self, configuration_directory, vnf, version):

        try:
            filename = "../etc/" + configuration_directory + "/" + vnf + "_" + version + "/config"

            with open( filename, 'r' ) as file:

                data = file.read()

            return ( True, data )

        except Exception:
            return  ( False, '' )
