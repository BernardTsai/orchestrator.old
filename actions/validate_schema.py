#!/usr/bin/python

#-------------------------------------------------------------------------------
#
# ValidateSchema:
#
# Custom action to validate if a certain data object conforms to a specific
# schema description.
#
# The schema files are referenced via the name of schema file which needs to
# reside in a directory relative to the location of this file:
#   ../../etc/schema/[schema_name].yaml
# The schema specification files make use of jsonschema.
#
#-------------------------------------------------------------------------------

from sys                   import argv
from os                    import path, environ
from yaml                  import safe_load
from jsonschema            import validate
from traceback             import print_exc
from jsonschema.exceptions import ValidationError

# check if the action is executed in a StackStorm context
try:
    from st2actions.runners.pythonrunner import Action
    RUNTIMECONTEXT = True
except:
    RUNTIMECONTEXT = False

#----- custom action -----------------------------------------------------------
#
# run: validate compliance of data object with schema definition
#
# Parameters:
#  - schema_name: name of the schema file
#  - data:        data object which needs to be validated
#
# Result: Tuple consisting of success status and possible error details
#
#-------------------------------------------------------------------------------
def run(schema_name, data):

    try:
        root_dir        = path.dirname( path.realpath(__file__) )
        schema_filename = path.join( root_dir, "..", "etc", "schema", schema_name + ".yaml" )

        with open( schema_filename, 'r' ) as schema_file:

            schema_data = schema_file.read()

            schema_definition = safe_load( schema_data )

        validate( data, schema_definition )

        return ( True, '' )

    except ValidationError as ve:
        print( ve.message )
        print( ve.instance )
        return ( False, 'Invalid Schema' )
    except Exception as exc:
        print_exc()
        return  ( False, 'Unknown Error' )

#----- class wrapper -----------------------------------------------------------
if RUNTIMECONTEXT:
    class ValidateSchema(Action):

        def run(self, schema_name, data):
            return run( schema, data )

#----- execute only if run as a scriot -----------------------------------------
if __name__ == "__main__":

    # read parameters
    schema_name = argv[1]
    data_name   = argv[2]

    # load data
    root_dir = path.dirname( path.realpath(__file__) )
    data_filename = path.join( root_dir, "..", "tests", data_name )

    with open( data_filename, 'r' ) as data_file:

        data = data_file.read()

        obj = safe_load( data )

    # validate
    result = run( schema_name, obj )
    print( result )
