import maya.cmds as cmds
import random
#CreateUI

if(cmds.window("Animation_Auto_KeyFrame_Extraction", exists = True)):
    cmds.deleteUI("Animation_Auto_KeyFrame_Extraction")
myWin = cmds.window("Animation_Auto_KeyFrame_Extraction", title = "Animation Auto KeyFrame Extraction", s = True, width = 380, height = 200)
cmds.showWindow(myWin)
MainLayout = cmds.columnLayout(adjustableColumn = True)
cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
cmds.text(l = "Select Objects")
cmds.separator(w = 10, style = "none")
ObjCount = cmds.textField(ed = False, text = "0", w = 30)
cmds.separator(w = 10, style = "none")
MeshTextField = cmds.textField(ed = False, text = "None Selected")
cmds.separator(w = 10, style = "none")
MeshAssignBtn = cmds.button(l = "Select", w = 120, align = "center", c = "AssignMesh()")
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
cmds.text(l = "Set Time Rage")
cmds.separator(w = 20, style = "none")
TimeTextField_m = cmds.textField()
cmds.separator(w = 20, style = "none")
cmds.text(l = "--")
cmds.separator(w = 20, style = "none")
TimeTextField_M = cmds.textField()
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
cmds.text(l = "Random Range")
cmds.separator(w = 14, style = "none")
randomMin = cmds.textField()
cmds.separator(w = 20, style = "none")
cmds.text(l = "--")
cmds.separator(w = 20, style = "none")
randomMax = cmds.textField()
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
cmds.text(l = "Interval")
cmds.separator(w = 10, style = "none")
IntervalTextField = cmds.textField()
cmds.separator(w = 18, style = "none")
cmds.text(l = "EnableRandom")
cmds.separator(w = 10, style = "none")
EnableRandomBtn = cmds.button(l = "Enable", w = 90, align = "center", c = "EnableRandom()", bgc = (0.4,1,0.6))
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nc = 3, adjustableColumn = True)
ActivateBtn = cmds.button(l = "Activate", w = 100, align = "center", c = "Activate()")
cmds.setParent(MainLayout)

cmds.text(l = "Created By Charlie Chiao - Non commercial use")

RandomEnable = False
SelectedList = []

def getSelection():
	global SelectedList
	selection = []
	SelectedList = []
	selection = cmds.ls(sl = True)
	SelectedList = selection
	print(selection)
	return selection

def changeText(TextFieldName,Value):
	cmds.textField(TextFieldName, e = True, text = Value)

def AssignMesh():
	changeText(MeshTextField, "")
	changeText(ObjCount, "")
	cmds.button(ActivateBtn, edit = True, enable = False)
	Mesh = getSelection()
	print(Mesh, 'selected')
	changeText(MeshTextField, "Objects Selected")
	changeText(ObjCount, len(Mesh))
	cmds.button(ActivateBtn, edit = True, enable = True)

def EnableRandom():
    global RandomEnable
    if RandomEnable:
        cmds.textField(IntervalTextField, e = True, en = True)
        RandomEnable = False
        cmds.button(EnableRandomBtn, e = True, l= "Enable", bgc = (0.4, 1, 0.6))
    else:
        cmds.textField(IntervalTextField, e = True, en = False)
        RandomEnable = True
        cmds.button(EnableRandomBtn, e = True, l= "Disable", bgc = (1, 0.3, 0.5))
    return

def Activate():
    global RandomEnable
    global SelectedList
    _Mesh = SelectedList
    startFrame = int(cmds.textField(TimeTextField_m, q = True, text = True))
    endFrame = int(cmds.textField(TimeTextField_M, q = True, text = True))
    if RandomEnable:
        R_m = int(cmds.textField(randomMin, q = True, text = True))
        R_M = int(cmds.textField(randomMax, q = True, text = True))
        _Interval = randomInt(R_m,R_M)
    else:
        _Interval = int(cmds.textField(IntervalTextField, q = True, text = True))
        nextFrame = _Interval + 1
    cmds.bakeResults(_Mesh, t = (startFrame, endFrame))


    for num in range(startFrame, endFrame):
        if RandomEnable:
            _Interval = randomInt(R_m,R_M)
            nextFrame = _Interval + 1
        key = IntervalNum(num, nextFrame, startFrame, endFrame)
        if isValid(key):
        	for index in range(0,len(_Mesh)):
        		cmds.copyKey(_Mesh[index], t = (key,key))
        		PasteFollowKeys(key,_Interval,_Mesh[index])
            #print(nextFrame)
        else:
            #print('Error: Out of boundary!')
            return
        #cmds.pasteKey(_Mesh, time = (endFrame,endFrame))

def IntervalNum(num, Interval, startFrame, endFrame):
	if num == startFrame:
		val = startFrame
		return val
	elif num * Interval > endFrame:
		val = None
		return val
	else:
		val = num * Interval
    	return val

def isValid(obj):
    if obj == None:
        state = False
        return state
    else:
        state = True
        return state

def PasteFollowKeys(key,Interval,Mesh):
    min = key
    max = key + Interval + 1
    for i in range(min,max):
        cmds.pasteKey(Mesh, t = (i,i))
        #print(i)

def randomInt(min,max):
    val = int(round(max*random.random()) + min)
    return val
