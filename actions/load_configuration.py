#!/usr/bin/python

from os   import path
from yaml import safe_load

from st2actions.runners.pythonrunner import Action

class LoadConfiguration(Action):

    def run(self, configuration_directory, vnf, version):

        try:
            root_dir = path.dirname( path.realpath(__file__) )
            filename = path.join( root_dir, "..", "etc", configuration_directory, vnf + "_" + version, "config" )

            with open( filename, 'r' ) as file:

                data = file.read()

                yaml = safe_load( data )

            return ( True, yaml )

        except Exception as exc:
           print( exc )
           return  ( False, '' )
