# fmi-3D-animation
3D animation FMU support for INTO-CPS.

To generate or update the 3D animation FMU, download the files from this Github repository and follow the steps below.

## Generate the scenery
1. Open model;
2. Open the simulator and go to the 3D animation plot;
3. Right-click in the 3D animation plot and select "Plot properties";
4. Choose "File"->"Save scene";
5. Select "Yes" to save the whole scenery;
6. Save the scenery under the name "scenery.scn" in the fmu_sources\resources folder.

## Generate the FMU *modelDescription.xml*
7. Update the FMU_GUID in the "scenery_to_fmu.py" Python script;
8. Run the "scenery_to_fmu.py" Python script.

This will parse the scenery.scn file for objects that point to variables/parameters (references).
The variables/parameters will be translated to FMU inputs and FMU parameters.
The 3D scenery does not contain any information that indicated whether the referred name is a variable or a parameter.
As a workaround, we have chosen to mark all names that start with "parameter." as a FMU parameter (variability="tunable") all others are generated as input (variability="continuous").
This script will also generate a "scenery.txt" file with the list of found references.
This file is read by the 3D animation DLL to couple the FMU interface to the 3D scenery objects.

## Create the FMU
9. Make sure that all needed textures are in the *fmu_sources\resources\* folder;
10. Enter the fmu_sources folder, select everything and zip it;
11. Rename the zip file to 3DAnimationFMU.fmu.
