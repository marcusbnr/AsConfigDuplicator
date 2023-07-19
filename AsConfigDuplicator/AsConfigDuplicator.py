"""
AsConfigDuplicator main script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

######## Import Libraries ########
import os
import shutil

######## Structure Declarations ########

######## Declare Functions ########

# This funcntion reads a Package.pkg file and turns every "File" entry to a Reference entry
# Requires: The path to the pkg file, the name of the AS Configuration to Reference, the name of the processor folder in the Physical view
# Modifies: Rewrites the pkg file
# Returns: Nothing
def AddReferencesToPkg(FilePath, OldConfigName, ProcessorFolderName):
    with open(FilePath, 'r') as File:
        FileData = File.read()

    FileData = FileData.replace("Type=\"File\">", "Type=\"File\" Reference=\"true\">\\Physical\\" + OldConfigName + '\\' + ProcessorFolderName + "\\")

    with open(FilePath, 'w') as File:
        FileData = File.write(FileData)
    return      

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

    # Copy directories and pkg files only
    for (Root, Dirs, Files) in os.walk(OldConfigPath):
        for Dir in Dirs:
            OldDirPath = Root + '/' + Dir
            OldDirPath = OldDirPath.replace('\\', '/')
            NewDirPath = OldDirPath.replace(ConfigToDuplicate, NewConfigName)
            os.mkdir(NewDirPath)

        for File in Files:
            if(File == "Package.pkg"):
                OldFilePath = Root + '/' + File
                NewFilePath = OldFilePath.replace(ConfigToDuplicate, NewConfigName)
                NewFilePath = NewFilePath.replace('\\', '/')
                shutil.copy2(OldFilePath, NewFilePath)   

    # Copy files which cannot be referenced:
        # Config.pkg
        # Hardware.hw
        # Hardware.hwl
        # Hardware.jpg
        # Cpu.pkg

    shutil.copy2(OldConfigPath + "/Config.pkg", NewConfigPath)    
    shutil.copy2(OldConfigPath + "/Hardware.hw", NewConfigPath)  
    shutil.copy2(OldConfigPath + "/Hardware.hwl", NewConfigPath)  
    shutil.copy2(OldConfigPath + "/Hardware.jpg", NewConfigPath)  

    # For the Cpu.pkg file, we need the folder directly inside the config folder
    ProcessorFolderPath = next(os.walk(OldConfigPath))[1][0]
    shutil.copy2(OldConfigPath + '/' + ProcessorFolderPath + "/Cpu.pkg", NewConfigPath + '/' + ProcessorFolderPath)  

    # Modify Cpu.pkg file to reference CPU files
    CpuPkgFilePath = NewConfigPath + '/' + ProcessorFolderPath + "/Cpu.pkg"
    with open(CpuPkgFilePath, 'r') as File:
        FileData = File.read()

    FileData = FileData.replace(">Cpu.sw"," Reference=\"true\">" + '\\Physical\\' + ConfigToDuplicate + '\\' + ProcessorFolderPath + "\Cpu.sw")
    FileData = FileData.replace(">Cpu.per"," Reference=\"true\">" + '\\Physical\\' + ConfigToDuplicate + '\\' + ProcessorFolderPath + "\Cpu.per")
    FileData = FileData.replace(">IoMap.iom"," Reference=\"true\">" + '\\Physical\\' + ConfigToDuplicate + '\\' + ProcessorFolderPath + "\IoMap.iom")
    FileData = FileData.replace(">PvMap.vvm"," Reference=\"true\">" + '\\Physical\\' + ConfigToDuplicate + '\\' + ProcessorFolderPath + "\PvMap.vvm")

    with open(CpuPkgFilePath, 'w') as File:
        FileData = File.write(FileData)

    # Create reference files for each configuration file by modifying .pkg files
    for (Root, Dirs, Files) in os.walk(NewConfigPath):
        for File in Files:
            if(File.endswith(".pkg")):
                AddReferencesToPkg(Root + "\\" + File, ConfigToDuplicate, ProcessorFolderPath)

    # Add new configuration to Physical folder .pkg file

    # Done!

if __name__ == '__main__':
    main()
