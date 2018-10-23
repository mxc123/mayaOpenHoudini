import json
import os
import hou
temPath = os.getenv("TEMP")
if "/houdini_temp" in temPath:
    temPath=temPath.replace("/houdini_temp","")

with open("%s/%s.json" % (temPath, "abc"), "r") as file:
    dict_all=json.loads(file.read())
print dict_all
node = hou.node("/obj")
hou.cd("/obj")
pwd = hou.pwd().createNode("geo")
hou.cd("/obj/geo1")
file=hou.node("file1")
file.destroy()
alembic=hou.pwd().createNode("alembic")
path = alembic.parm("fileName")
path.set(dict_all["abcPath"])
loadMode = alembic.parm("loadmode")
loadMode.set(2)
polysoup = alembic.parm("polysoup")
polysoup.set(0)


