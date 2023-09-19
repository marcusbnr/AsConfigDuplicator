# AsConfigDuplicator
Duplicates an AS configuration and replaces config files with reference files in the new configuration

## Purpose
Sometimes it is necessary to create a duplicate configuration in an Automation Studio project which references an existing configuration. This new configuration can have different hardware (i.e. one configuration for simulation and one for the physical machine). However, manually replacing each new configuration file with a reference file can be very time consuming. The goal of this python script is to automate the process of creating a new reference configuration from an existing configuration.

## How To Use
1. Place the script in the folder which also contains the AS project folder (this is not required but simplifies execution).
2. Run the script using Python >= 3.9.2
3. Input the AS project name (the name of the project folder which holds the .apj file)
4. Input the name of the configuration to be duplicated
5. Input the name of the new configuration

## Limitations
* The .apj file and the project folder must have the same name (this is the default for any projects created with Automation Studio)
* AS Configuration names cannot contain some special characters. It is up to the user to pick a name for the new configuration which matches AS rules
* If the project is open when the script is run, it must be closed and re-opened to update the Configuration View

## Demonstration
https://github.com/marcusbnr/AsConfigDuplicator/assets/103762819/115e53c5-7298-458d-82b9-a03b5eb08d79

