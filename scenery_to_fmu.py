#!/usr/bin/python
# coding: utf-8
"""
This script delivers the model variables and parameters necessary for animation
into an FMU model description file.
"""

import xml.etree.ElementTree as etree

SCENERY_FILE = 'fmu_sources\\resources\\scenery.scn'
PARAM_PREFIX = 'parameters.'
VARIABLE_TAG = 'VariableName'
VALUE_TAG = 'Value'
ANIM_VARS_FILENAME = 'fmu_sources\\resources\\scenery.txt'
MODEL_DESC_FILENAME = 'fmu_sources\\modelDescription.xml'
FMU_GUID = '{d96e2f1e-691f-4e9b-b695-e99129089798}'

# Placeholders for the content of the modelDescription.xml file
MODEL_DESC_HEADER1 = '<?xml version="1.0" encoding="ISO-8859-1"?>\n<fmiModelDescription fmiVersion="2.0" modelName="model" guid="'
MODEL_DESC_HEADER2 = '" generationTool="20-sim" numberOfEventIndicators="0" copyright="Controllab Products B.V." license="-">\n<CoSimulation modelIdentifier="model" needsExecutionTool="false" canHandleVariableCommunicationStepSize="true" canInterpolateInputs="false" maxOutputDerivativeOrder="0" canRunAsynchronuously="false" canBeInstantiatedOnlyOncePerProcess="true" canNotUseMemoryManagementFunctions="true" canGetAndSetFMUstate="false" canSerializeFMUstate="false" providesDirectionalDerivative="false" />\n\t<DefaultExperiment startTime="0.0" stopTime="1000.0" />\n\t<ModelVariables>\n'
MODEL_DESC_FOOTER = '\t</ModelVariables>\n\t<ModelStructure></ModelStructure>\n</fmiModelDescription>'
VARIABLE_ENTRY = '\t\t<ScalarVariable name="{}" valueReference="{}" variability="continuous" causality="input">\n\t\t\t<Real start="{}" />\n\t\t</ScalarVariable>\n'
# Unsure of variability value for 3D animation parameters; see FMI 2.0 spec p.47
PARAMETER_ENTRY = '\t\t<ScalarVariable name="{}" valueReference="{}" variability="tunable" causality="parameter">\n\t\t\t<Real start="{}" />\n\t\t</ScalarVariable>\n'

class AnimationVariable(object):
    """
    A class for an animation variable that holds its name, value and whether
    it is of type parameter.
    """
    def __init__(self, name, value, is_param):
        self.name = name
        self.value = value
        self.is_param = is_param

    def get_name(self):
        """
        Return the name of this animation variable, removing the parameter
        prefix if present.
        """
        if self.is_param:
            return self.name[len(PARAM_PREFIX):]
        else:
            return self.name

def extract_names(input_file, output_file):
    """
    Extract any names of model variables and their values found in the given 3D
    scenery file.
    
    Write the names to the specified text file, one per line, removing the
    prefix 'parameters.' where present.
    
    Args:
        input_file (str): File of 3D objects
        output_file (str): Text file of animation model variable names

    Returns:
        list: A list of unique `AnimationVariable` objects, sorted in the same
            order as written to the output file
    """
    # Parse the 3D scenery file.
    tree = etree.parse(input_file)
    root = tree.getroot()

    # Look for any names of model variables present in the 3D scenery data.
    query = ".//*[{}]".format(VARIABLE_TAG)
    interesting_elements = root.findall(query)

    # Make a list with the unique animation variables found, removing the prefix
    # 'parameters' if present in the name.
    unique_animation_variables = list()
    unique_var_names = set()
    for elem in interesting_elements:
        var_name = elem.find(VARIABLE_TAG).text

        # If variable name is new..
        if var_name not in unique_var_names:
            # add it to list of unique names &..
            unique_var_names.add(var_name)
            # create an AnimationVariable object for it.
            anim_var = AnimationVariable(
                elem.find(VARIABLE_TAG).text,
                elem.find(VALUE_TAG).text,
                var_name.startswith(PARAM_PREFIX)
            )
            unique_animation_variables.append(anim_var)

    # Prepare file output, one variable name per line.
    var_names = list()
    for anim_var in unique_animation_variables:
        print(anim_var.get_name())
        var_names.append('{}\n'.format(anim_var.get_name()))

    # Write the variable names to a text file.
    if len(var_names) > 0:
        with open(output_file, 'w') as o_file:
            o_file.writelines(var_names)
            print('Found and saved {} variable(s) to: {}'.format(
                len(var_names), output_file))

    return unique_animation_variables

def create_model_desc(animation_variables, output_file):
    """
    Create a model description XML output file that contains scalar elements for
    all given animation variables.
    
    Args:
        animation_variables (list): The animation variables to include
        output_file (str): The created model description XML file        
    """
    # Prepare the model variables XML element for the model description file.
    variables_desc = ''
    scalar_element = ''
    for idx, anim_var in enumerate(animation_variables):
        if anim_var.is_param:
            scalar_element = PARAMETER_ENTRY
        else:
            scalar_element = VARIABLE_ENTRY

        variables_desc = ''.join((variables_desc, scalar_element.format(
                anim_var.get_name().strip(),
                idx+1,
                anim_var.value
        )))
            
    # Write the model description XML file.
    data = ''.join((MODEL_DESC_HEADER1, FMU_GUID, MODEL_DESC_HEADER2, variables_desc, MODEL_DESC_FOOTER))
    with open(output_file, 'w') as output:
        output.write(data)
        print('Created file: {}'.format(MODEL_DESC_FILENAME))

if __name__ == "__main__":
    animation_variables = extract_names(SCENERY_FILE, ANIM_VARS_FILENAME)
    create_model_desc(animation_variables, MODEL_DESC_FILENAME)
