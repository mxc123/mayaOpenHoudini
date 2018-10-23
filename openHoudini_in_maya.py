# -*- encoding: utf-8 -*-
try:
    from PySide2 import QtWidgets as QtGui
    from PySide2 import QtCore
except ImportError:
    from Pyside import QtGui
    from PySide import QtCore
import sys
import maya.cmds as cmds
import maya.mel as mel
import json,os
import subprocess
temPath=os.getenv("TEMP")
print temPath

class MinWindows(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(u"导出abc并导入houdini")
        self.resize(400,300)
        abcLabel=QtGui.QLabel(u"导出abc路径")
        abcLinEdite=QtGui.QLineEdit()
        abcLinEdite=MylineEdit()
        openBtn=QtGui.QPushButton(u"打开Houdini")
        cancleBtn=QtGui.QPushButton(u"取消")

        abcLayout=QtGui.QFormLayout()
        abcLayout.addRow(abcLabel,abcLinEdite)

        btnLayout=QtGui.QHBoxLayout()
        btnLayout.addWidget(openBtn)
        btnLayout.addWidget(cancleBtn)

        laterestLayout=QtGui.QVBoxLayout()
        laterestLayout.addLayout(abcLayout)
        laterestLayout.addLayout(btnLayout)
        self.setLayout(laterestLayout)
        openBtn.clicked.connect(self.loadHoudini)
        cancleBtn.clicked.connect(self.cancle)
        self.show()
        self.abcLinEdite=abcLinEdite
    
    
    def cancle(self):
        self.close()

    def exportAbc(self,abcPath):
        selectGeo = cmds.ls(sl=True)
        startTime = cmds.playbackOptions(q = True,min = True)
        endTime = cmds.playbackOptions(q = True,max = True)
        mel.eval('AbcExport -j "-frameRange %d %d -dataFormat ogawa -root |%s -file %s/%s.abc";'%(startTime,endTime,selectGeo[0],abcPath,selectGeo[0]))
        return "%s/%s.abc"%(abcPath,selectGeo[0])
    def writeJson(self):
        currentPath = self.abcLinEdite.text()
        abcPath=exportAbc(currentPath,"abc")
        dict_all = {"abcPath":abcPath}
        with open("%s\%s.json"%(temPath,"abc"),"w") as files:
            end=json.dumps(dict_all,indent=4)
            files.write(end)

    def loadHoudini(self):
        self.writeJson()
        currentPath = os.path.dirname(__file__)
        command=r'"D:\houdini16.5\bin\houdinifx.exe"'+" "+"%s\createNode.py"%currentPath
        subprocess.Popen(command,shell=None)

class MylineEdit(QtGui.QLineEdit):#自定义鼠标拖拽事件的Class,只需要将此Class赋予QlineEdit的对象即可
    def __init__(self,parent=None):
        QtGui.QLineEdit.__init__(self,parent)
        self.setAcceptDrops(True)
    def dragEnterEvent(self,event):
        event.accept()
    def dropEvent(self, event):
        st = str(event.mimeData().urls())
        st = st.replace('[PySide2.QtCore.QUrl',"")
        st = st.replace('[PySide.QtCore.QUrl',"")
        st = st.replace("'), ",",")
        st = st.replace("('file:///","")
        st = st.replace("')]","")
        self.setText(st)
#if __name__ =="__main__":
    #app=QtGui.QApplication(sys.argv)
mainWindows=MinWindows()
#mainWindows.show()
    #sys.exit(app.exec_())




