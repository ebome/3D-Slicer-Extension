from __main__ import vtk, qt, ctk, slicer
from vtk.util import numpy_support
import numpy as np

#Parametric Estimator:Author
class ParametricEstimator:
  def __init__(self, parent):  ## __init__ method to initialize some data attributes
    parent.title = "Parametric Estimator"
    parent.categories = ["Assignment"]
    parent.dependencies = []
    parent.contributors = ["Yang GAO 450614082"]
    parent.helpText = """
    It is a loadable extension modulus for Slicer 4.
    """
    parent.acknowledgementText = """
    To perform the basic options on a sequence of images, including ADD, MINUS, MULTIPLY,
    DIVIDE, Logic AND and OR. It will enable us to derive various parameters from these input
    images.
    """
    self.parent = parent


class ParametricEstimatorWidget:
  def __init__(self, parent = None): # NEVER change this __init__ constructor
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  #  Setup the layout
  def setup(self):   # NEVER delete self when def a function within the class
    #==========================================================================
    # Do NOT CHANGE THE RELOAD SECTION
    self.testReloadFrame = ctk.ctkCollapsibleButton()
    self.testReloadFrame.objectName = 'ReloadFrame'
    self.testReloadFrame.setLayout(qt.QHBoxLayout())
    self.testReloadFrame.setText("Reload the Module")
    self.layout.addWidget(self.testReloadFrame) # layout is the whole panel of the GUI
    self.testReloadFrame.collapsed = False
    # Add a reload button for debug
    reloadButton = qt.QPushButton("Reload")
    reloadButton.toolTip = "Reload this Module"
    reloadButton.name = "ParametricEstimator Reload"
    reloadButton.connect('clicked()', self.onReload)
    self.reloadButton = reloadButton
    self.testReloadFrame.layout().addWidget(self.reloadButton)
    #=============================================================================


    """
    Layout inside Collapsible button for Basic Operation
    """
    self.operationCollapsibleButton = ctk.ctkCollapsibleButton()
    self.operationCollapsibleButton.text = "Basic Operations"
    self.layout.addWidget(self.operationCollapsibleButton)
    self.operationCollapsibleButton.collapsed = False
    # QFormLayout is a convenience layout class that lays out its children in a
    #   two-column form. The left column consists of labels and the right column
    #   consists of "field" widgets (line editors, spin boxes, etc.)
    # http://doc.qt.io/archives/qt-4.8/qformlayout.html#details
    self.OperationFormLayout = qt.QFormLayout(self.operationCollapsibleButton)
    #==========================================================================
    # Layout within the Operation collapsible button
    ## the volume selectors
    self.inputFrame1 = qt.QFrame(self.operationCollapsibleButton)
    self.inputFrame1.setLayout(qt.QHBoxLayout())
    self.OperationFormLayout.addWidget(self.inputFrame1) # OperationFormLayout is inside the Basic Op panel
    self.inputSelector1 = qt.QLabel("First Input: ", self.inputFrame1)
    self.inputFrame1.layout().addWidget(self.inputSelector1)
    self.inputSelector1 = slicer.qMRMLNodeComboBox(self.inputFrame1)
    self.inputSelector1.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" ) # We only assume inputs are all ScalarVolumeNode, so no need to use vtkMRMLDiffusionWeightedVolumeNode
    self.inputSelector1.addEnabled = False
    self.inputSelector1.removeEnabled = False
    self.inputSelector1.setMRMLScene( slicer.mrmlScene )
    self.inputFrame1.layout().addWidget(self.inputSelector1)
    ########################## Since 2 INPUTS as required, we set another one input
    self.inputFrame2 = qt.QFrame(self.operationCollapsibleButton)
    self.inputFrame2.setLayout(qt.QHBoxLayout())
    self.OperationFormLayout.addWidget(self.inputFrame2)
    self.inputSelector2 = qt.QLabel("Second Input: ", self.inputFrame2)
    self.inputFrame2.layout().addWidget(self.inputSelector2)
    self.inputSelector2 = slicer.qMRMLNodeComboBox(self.inputFrame2)
    self.inputSelector2.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector2.addEnabled = False
    self.inputSelector2.removeEnabled = False
    self.inputSelector2.setMRMLScene( slicer.mrmlScene )
    self.inputFrame2.layout().addWidget(self.inputSelector2)
    #########################################################################
    self.OperationOutputFrame = qt.QFrame(self.operationCollapsibleButton)
    self.OperationOutputFrame.setLayout(qt.QHBoxLayout())
    self.OperationFormLayout.addWidget(self.OperationOutputFrame)
    self.OperationOutputSelector = qt.QLabel("Output Volume: ", self.OperationOutputFrame)
    self.OperationOutputFrame.layout().addWidget(self.OperationOutputSelector)
    self.OperationOutputSelector = slicer.qMRMLNodeComboBox(self.OperationOutputFrame) # qMRMLNodeComboBox is slicer widget that monitors the scene and select nodes for specified tyors
    self.OperationOutputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" ) # ScalarVolumeNode is a slcier MRML class
    self.OperationOutputSelector.setMRMLScene( slicer.mrmlScene )
    self.OperationOutputFrame.layout().addWidget(self.OperationOutputSelector)
    #===================================================================

    # Users can choose which opeartion they need, default checkbox is Add
    self.filter = "Add two inputs" # filter does not perform filtering function, it is just a variable name

    changeFilterFrame = qt.QFrame(self.parent)
    changeFilterFrame.setLayout(qt.QVBoxLayout())
    self.OperationFormLayout.addWidget(changeFilterFrame)
    self.changeFilterFrame = changeFilterFrame

    chooseADD = qt.QRadioButton("Add two inputs")
    chooseADD.setChecked(True)
    chooseADD.connect('clicked()', self.chooseADD)
    self.OperationFormLayout.addWidget(chooseADD)
    self.chooseADD = chooseADD

    chooseSubtract = qt.QRadioButton("Subtract 2nd input from 1st input")
    chooseSubtract.connect('clicked()', self.chooseSubtract)
    self.OperationFormLayout.addWidget(chooseSubtract)
    self.chooseSubtract = chooseSubtract

    chooseMultiply = qt.QRadioButton("Multiply two inputs")
    chooseMultiply.connect('clicked()', self.chooseMultiply)
    self.OperationFormLayout.addWidget(chooseMultiply)
    self.chooseMultiply = chooseMultiply

    chooseDivide = qt.QRadioButton("Divide 1st input by 2nd input")
    chooseDivide.connect('clicked()', self.chooseDivide)
    self.OperationFormLayout.addWidget(chooseDivide)
    self.chooseDivide = chooseDivide

    # Apply button can apply to all opertations
    OperationApplyButton = qt.QPushButton("Apply Basic Operation")
    OperationApplyButton.toolTip = "Run the required operation"
    self.OperationFormLayout.addWidget(OperationApplyButton) #We want apply button control 4 operations
    OperationApplyButton.connect('clicked(bool)', self.onOperationApply)
    self.OperationApplyButton = OperationApplyButton

    # add a stretchable space with stretch factor 1 to the ecd of this box layout
    # without streth, the layout will be determined by the sizePolicy of the widgets
    # https://stackoverflow.com/questions/20452754/how-exactly-does-addstretch-work-in-qboxlayout
    self.layout.addStretch(1)
    #===================================================================


    """
    Layout inside Collapsible button for LOGIC Operation
    """
    self.LogicCollapsibleButton = ctk.ctkCollapsibleButton()
    self.LogicCollapsibleButton.text = "Logic Operations"
    self.layout.addWidget(self.LogicCollapsibleButton)
    self.LogicCollapsibleButton.collapsed = False
    self.LogicFormLayout = qt.QFormLayout(self.LogicCollapsibleButton)
    #==========================================================================
    # Layout within the Logic collapsible button
    ## the volume selectors
    self.LogicInputFrame1 = qt.QFrame(self.LogicCollapsibleButton)
    self.LogicInputFrame1.setLayout(qt.QHBoxLayout())
    self.LogicFormLayout.addWidget(self.LogicInputFrame1)
    self.LogicInputSelector1 = qt.QLabel("First Input (mask only): ", self.LogicInputFrame1)
    self.LogicInputFrame1.layout().addWidget(self.LogicInputSelector1)
    self.LogicInputSelector1 = slicer.qMRMLNodeComboBox(self.LogicInputFrame1)
    self.LogicInputSelector1.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.LogicInputSelector1.addEnabled = False
    self.LogicInputSelector1.removeEnabled = False
    self.LogicInputSelector1.setMRMLScene( slicer.mrmlScene )
    self.LogicInputFrame1.layout().addWidget(self.LogicInputSelector1)
    ########################## Since 2 INPUTS as required, we set another one input
    self.LogicInputFrame2 = qt.QFrame(self.LogicCollapsibleButton)
    self.LogicInputFrame2.setLayout(qt.QHBoxLayout())
    self.LogicFormLayout.addWidget(self.LogicInputFrame2)
    self.LogicInputSelector2 = qt.QLabel("Second Input (mask or volume): ", self.LogicInputFrame2)
    self.LogicInputFrame2.layout().addWidget(self.LogicInputSelector2)
    self.LogicInputSelector2 = slicer.qMRMLNodeComboBox(self.LogicInputFrame2)
    self.LogicInputSelector2.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.LogicInputSelector2.addEnabled = False
    self.LogicInputSelector2.removeEnabled = False
    self.LogicInputSelector2.setMRMLScene( slicer.mrmlScene )
    self.LogicInputFrame2.layout().addWidget(self.LogicInputSelector2)
    #########################################################################
    self.LogicOutputFrame = qt.QFrame(self.LogicCollapsibleButton)
    self.LogicOutputFrame.setLayout(qt.QHBoxLayout())
    self.LogicFormLayout.addWidget(self.LogicOutputFrame)
    self.LogicOutputSelector = qt.QLabel("Output Volume (1 and 0 only): ", self.LogicOutputFrame)
    self.LogicOutputFrame.layout().addWidget(self.LogicOutputSelector)
    self.LogicOutputSelector = slicer.qMRMLNodeComboBox(self.LogicOutputFrame) # qMRMLNodeComboBox is slicer widget that monitors the scene and select nodes for specified tyors
    self.LogicOutputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" ) # ScalarVolumeNode is a slcier MRML class
    self.LogicOutputSelector.setMRMLScene( slicer.mrmlScene )
    self.LogicOutputFrame.layout().addWidget(self.LogicOutputSelector)
    #===================================================================
    # Users can choose which opeartion they need, default checkbox is AND
    self.selection = "AND"

    changeSelectionFrame = qt.QFrame(self.parent)
    changeSelectionFrame.setLayout(qt.QVBoxLayout())
    self.LogicFormLayout.addWidget(changeSelectionFrame)
    self.changeSelectionFrame = changeSelectionFrame

    chooseAND = qt.QRadioButton("AND")
    chooseAND.connect('clicked()', self.chooseAND)
    self.LogicFormLayout.addWidget(chooseAND)
    self.chooseAND = chooseAND

    chooseOR = qt.QRadioButton("OR")
    chooseOR.connect('clicked()', self.chooseOR)
    self.LogicFormLayout.addWidget(chooseOR)
    self.chooseOR = chooseOR

    # Apply button for logic opertations
    LogicApplyButton = qt.QPushButton("Apply Logic Operation")
    LogicApplyButton.toolTip = "Run the AND or OR operation"
    self.LogicFormLayout.addWidget(LogicApplyButton) #We want apply button control 6 operations, so use layout rather than OperationFormLayout in ADD
    LogicApplyButton.connect('clicked(bool)', self.onLogicApply)
    self.LogicApplyButton = LogicApplyButton
    self.layout.addStretch(1)


  # Choose what operations to use: the functions define the operation type
  def chooseADD(self):
    self.filter = "Add two inputs"
  def chooseSubtract(self):
    self.filter = "Subtract 2nd input from 1st input"
  def chooseMultiply(self):
    self.filter = "Multiply two inputs"
  def chooseDivide(self):
    self.filter = "Divide 1st input by 2nd input"
  # Choose what operations to use: the functions define the LOGIC type
  def chooseAND(self):
    self.selection = "AND"
  def chooseOR(self):
    self.selection = "OR"

#####################################################################################
  # When the apply button inside "Basic operations" is clicked
  def onOperationApply(self):
    # Read in the image node
    inputVolume1 = self.inputSelector1.currentNode()
    inputVolume2 = self.inputSelector2.currentNode()
    OperationOutputVolume = self.OperationOutputSelector.currentNode()
    # Extract the array
    inputVolumeData1 = slicer.util.array(inputVolume1.GetID())
    inputVolumeData2 = slicer.util.array(inputVolume2.GetID())
    # Name the output volume
    OperationOutputVolume_name = inputVolume1.GetName() + '_OperationResult'
    # Copy image node, create a new volume node.
    volumesLogic = slicer.modules.volumes.logic()
    OperationOutputVolume = volumesLogic.CloneVolume(slicer.mrmlScene, inputVolume1, OperationOutputVolume_name)
    # Find the array that is associated with the label map
    OperationOutputVolumeData = slicer.util.array(OperationOutputVolume.GetID())

    # the array we extract from user inputs
    inputVolumeData1 = inputVolumeData1.astype(np.float) # astype() copy the array inputVolumeData1 and cast it to float type
    inputVolumeData2 = inputVolumeData2.astype(np.float) # 2.5 will be cast to 2

    if self.filter == "Add two inputs":
        '''
        input: two volumes. Different input sequence will influence the output
        '''
        # Sum the two inputs voxel-wise, and output the result to OperationOutputVolume
        OperationOutputVolumeData[:] = inputVolumeData1[:] + inputVolumeData2[:] # If one does not specify as many slices as there are dimensions in an array, then the remaining slices are assumed to be "all"
    if self.filter == "Subtract 2nd input from 1st input":
        '''
        input: two volumes. Different input sequence will influence the output
        '''
        # Subtract the two inputs voxel-wise, and output the result to OperationOutputVolume
        OperationOutputVolumeData[:] = inputVolumeData1[:] - inputVolumeData2[:] # A[1] == A[1,:] == A[1,:,:];

    if self.filter == "Multiply two inputs":
        '''
        input: two volumes--> gives a mosiac graph due to large number multiplication
               one volume + one mask ---> better, the input sequence does not matter
        '''
        OperationOutputVolumeData[:] = inputVolumeData1[:] * inputVolumeData2[:]

    if self.filter == "Divide 1st input by 2nd input":
        '''
        input: two volumes--> gives a output but no sense
               one volume + one mask ---> better, the input sequence does not matter
        '''
        # the loop will change every "0" in input 2 equal to value of input 1 in that position
        for x in np.nditer(inputVolumeData2, op_flags=['readwrite']):
                if x == 0:
                    x[...] = 1
        OperationOutputVolumeData[:] = inputVolumeData1[:] / inputVolumeData2[:]

    # After modification, store the data to OperationOutputVolume
    OperationOutputVolume.GetImageData().Modified()
    # make the output volume appear in all the slice views
    selectionNode = slicer.app.applicationLogic().GetSelectionNode()
    selectionNode.SetReferenceActiveVolumeID(OperationOutputVolume.GetID())
    slicer.app.applicationLogic().PropagateVolumeSelection(0)

#####################################################################################
  # When the apply button inside "Logic operations" is clicked
  def onLogicApply(self):
    # Read in the image node
    inputVolume3 = self.LogicInputSelector1.currentNode()
    inputVolume4 = self.LogicInputSelector2.currentNode()
    LogicOutputVolume = self.LogicOutputSelector.currentNode()
    # Extract the array
    inputVolumeData3 = slicer.util.array(inputVolume3.GetID())
    inputVolumeData4 = slicer.util.array(inputVolume4.GetID())
    # Name the output volume
    LogicOutputVolume_name = inputVolume3.GetName() + '_LogicResult'
    # Copy image node, create a new volume node.
    volumesLogic2 = slicer.modules.volumes.logic()
    LogicOutputVolume = volumesLogic2.CloneVolume(slicer.mrmlScene, inputVolume3, LogicOutputVolume_name)
    # Find the array that is associated with the label map
    LogicOutputVolumeData = slicer.util.array(LogicOutputVolume.GetID())

    # the array we extract from user inputs
    inputVolumeData3 = inputVolumeData3.astype(np.float) # astype() copy the array inputVolumeData1 and cast it to float type
    inputVolumeData4 = inputVolumeData4.astype(np.float) # 2.5 will be cast to 2
    temp = np.zeros_like(inputVolumeData3)
    temp1 = np.zeros_like(inputVolumeData4)
    temp_mask = np.zeros_like(inputVolumeData4)

    # The inputs of AND can be:
    # 1. Two masks
    # 2. A volume and a mask
    if self.selection == "AND":
        '''
         Inputs of AND can be:  1. Two masks    2. A mask and a volume
         Output: the overlapping region of two inputs. The overlapping region is denoted as the values of 2nd input
        '''
        # temp[:] is a boolean type array that denotes TRUE if the region is desirable
        temp[:] = inputVolumeData3[:]!=0
        a = temp.astype(int) # a is now a 3D array only containing 1 and 0

        # same as temp1
        temp1[:] = inputVolumeData4[:]!=0
        b = temp1.astype(int)

        # temp_mask[:] is the overlapping region of two inputs
        temp_mask[:] = a[:] * b[:]

        LogicOutputVolumeData[:] = temp_mask[:] * inputVolumeData4[:]
    # =========================================================================================================
    # The inputs of the OR can only be two masks, hence 0<In1-In2<1, so if voxel in In1
    # is different from voxel in In2, we can tell we have eliminate the "0" region.
    # If two inputs only have 0 and 1 rather than values smaller than 1 but larger than 0,
    # we need to make sure the "1" in inputs should be remained rather than be eliminated
    if self.selection == "OR":
        '''
           input: two masks, the input sequence does not matter
           output: another mask with value 0 and 1 only
        '''
        # temp[:] sets the desirable region in inputVolumeData3 to be TRUE
        temp[:] = (inputVolumeData3[:] != 0)
        # temp1[:] sets the desirable region in inputVolumeData4 to be TRUE
        temp1[:] = (inputVolumeData4[:] != 0)

        # temp_mask[:] denotes the regions that contain either input 1 or input 2
        temp_mask[:] = np.logical_or(temp[:], temp1[:])# temp_mask[:] is a Boolean type array

        # c is int type array
        c = temp_mask.astype(int)

        LogicOutputVolumeData[:] = c[:]
    ######################################################
    # After modification, store the data to OperationOutputVolume
    LogicOutputVolume.GetImageData().Modified()
    # make the output volume appear in all the slice views
    selectionNode2 = slicer.app.applicationLogic().GetSelectionNode()
    selectionNode2.SetReferenceActiveVolumeID(LogicOutputVolume.GetID())
    slicer.app.applicationLogic().PropagateVolumeSelection(0)


  #=======================================================================================
  # Reload the Module ---> DO NOT change anything in the method
  def onReload(self, moduleName = "ParametricEstimator"): # this function is in the class
    import imp, sys, os, slicer
    widgetName = moduleName + "Widget"
    fPath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(fPath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(fPath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, fPath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()
    print "the module name to be reloaded,", moduleName
    # find the Button with a name 'moduleName Reolad', then find its parent (e.g., a collasp button) and grand parent (moduleNameWidget)
    parent = slicer.util.findChildren(name = '%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)
    globals()[widgetName.lower()] = eval('globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    #===============================================================================
