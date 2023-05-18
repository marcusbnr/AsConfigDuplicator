"""
AsConfigDuplicator main script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

######## Import Libraries ########
import os
import shutil

######## Structure Declarations ########

######## Declare Functions ########



######## Main ########

def main():
    # Get information from user
    AsProjectPath = "C:/ProjectsTemp/SuperTrakCore" #= input("Enter path to Automation Studio project (folder containing .apj file) ")
    ConfigToDuplicate = "APC910" #= input("Enter the name of the Configuration you want to duplicate (name of the folder in the project directory) ")
    NewConfigName = "PPC2100" #= input("Enter the name of the new configuration ")

    # Check that project directory is valid (Contains a Physical directory)
    PhysicalDirectory = os.path.join(AsProjectPath, "Physical")
    if not os.path.exists(PhysicalDirectory):
        print("Invalid project path! ", AsProjectPath)
        return
    
    # Check that the chosen Configuration exists
    OldConfigPath = os.path.join(PhysicalDirectory, ConfigToDuplicate)
    if not os.path.exists(OldConfigPath):
        print("Invalid Configuration path! ", OldConfigPath)
        return
    
    # Check that the chosen New Configuration does not exist
    NewConfigPath = os.path.join(PhysicalDirectory, NewConfigName)
    NewConfigPath = NewConfigPath.replace('\\', '/')
    if os.path.exists(NewConfigPath):
        print("New Configuration already exists! ", NewConfigPath)
        return
    
    # To Do: Modify new config name based on AS rules ? Remove Spaces?

    # Create new Configuration folder
    print("Creating new Automation Studio Configuration at: ", NewConfigPath, "\n")
    os.mkdir(NewConfigPath)

    # Copy directories only
    for (Root, Dirs, Files) in os.walk(OldConfigPath):
        for Dir in Dirs:
            DirPath = ""
            SplitString = Root.split(OldConfigPath)
            for Element in SplitString:
                DirPath += Element;

            if not DirPath:
                PathToCreate = (NewConfigPath + '/' + Dir)
            else:
                PathToCreate = (NewConfigPath + DirPath + '/' + Dir)

            PathToCreate = PathToCreate.replace('\\', '/')
            os.mkdir(PathToCreate)

    # Copy files which cannot be referenced:
        # Config.pkg
        # Hardware.hw
        # Hardware.hwl
        # Hardware.jpg
        # Cpu.pkg

    shutil.copy2(OldConfigPath + "/Config.pkg", NewConfigPath)    

    # Create reference files for each configuration file by modifying .pkg files

    # Add new configuration to Physical folder .pkg file

    # Done!

if __name__ == '__main__':
    main()
