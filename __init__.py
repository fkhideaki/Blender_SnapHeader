bl_info = {
    "name": "Snap Option Header",
    "author": "Hideaki Fukushima",
    "description": "",
    "location": "3D View",
    "doc_url": "",
    "warning": "",
    "category": "General",
    "blender": (2, 83, 7),
    "version": (1, 0, 0)
}


import bpy
from bpy.app.handlers import persistent


silentUI = False


def regClass(reg, cls):
    if reg:
        bpy.utils.register_class(cls)
    else:
        bpy.utils.unregister_class(cls)

def regView3DHeader(reg, cls):
    if reg:
        bpy.types.VIEW3D_HT_tool_header.append(cls)
    else:
        bpy.types.VIEW3D_HT_tool_header.remove(cls)

def regHandler(reg, cls):
    if reg:
        bpy.app.handlers.load_post.append(cls)
    else:
        bpy.app.handlers.load_post.remove(cls)


class FKHD_HEADER_OperatorBase(bpy.types.Operator):
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout


def getMyProp(context):
    return context.scene.fkhd_header_properties


class FKHD_HEADER_Properties(bpy.types.PropertyGroup):
    def beginSilent(self):
        global silentUI
        if silentUI:
            return False
        silentUI = True
        return True
    def endSilent(self):
        global silentUI
        silentUI = False

    def updateSnapTranslate(self, context):
        if not self.beginSilent(): return
        ts = context.scene.tool_settings
        ts.use_snap_translate = not ts.use_snap_translate
        self.endSilent()
    snapTranslate: bpy.props.BoolProperty(
        name='Snap_translate',
        description='Toogle snap translate',
        default=False,
        update=updateSnapTranslate)

    def updateSnapScale(self, context):
        if not self.beginSilent(): return
        ts = context.scene.tool_settings
        ts.use_snap_scale = not ts.use_snap_scale
        self.endSilent()
    snapScale: bpy.props.BoolProperty(
        name='Snap_scale',
        description='Toogle snap translate',
        default=False,
        update=updateSnapScale)

    def updateSnapRotate(self, context):
        if not self.beginSilent(): return
        ts = context.scene.tool_settings
        ts.use_snap_rotate = not ts.use_snap_rotate
        self.endSilent()
    snapRotate: bpy.props.BoolProperty(
        name='Snap_rotate',
        description='Toogle snap rotate',
        default=False,
        update=updateSnapRotate)

    def setSnapTargetUI(self, context, t):
        if not self.beginSilent(): return
        aob = getMyProp(context)
        aob.snapClosest = (t == 'CLOSEST')
        aob.snapCenter = (t == 'CENTER')
        aob.snapMedian = (t == 'MEDIAN')
        aob.snapActive = (t == 'ACTIVE')
        context.scene.tool_settings.snap_target = t
        self.endSilent()

    def updateSnapClosest(self, context):
        self.setSnapTargetUI(context, 'CLOSEST')
    snapClosest: bpy.props.BoolProperty(
        name='Snap_closest',
        description='Toogle snap closest',
        default=False,
        update=updateSnapClosest)

    def updateSnapCenter(self, context):
        self.setSnapTargetUI(context, 'CENTER')
    snapCenter: bpy.props.BoolProperty(
        name='Snap_center',
        description='Toogle snap center',
        default=False,
        update=updateSnapCenter)

    def updateSnapMedian(self, context):
        self.setSnapTargetUI(context, 'MEDIAN')
    snapMedian: bpy.props.BoolProperty(
        name='Snap_median',
        description='Toogle snap median',
        default=False,
        update=updateSnapMedian)

    def updateSnapActive(self, context):
        self.setSnapTargetUI(context, 'ACTIVE')
    snapActive: bpy.props.BoolProperty(
        name='Snap_active',
        description='Toogle snap active',
        default=False,
        update=updateSnapActive)

    def appendElem(self, context, t):
        ts = context.scene.tool_settings
        if len(ts.snap_elements) == 1:
            if list(ts.snap_elements)[0] == t:
                return

        newsel = []
        detectSel = False
        for s in ts.snap_elements:
            if s == t:
                detectSel = True
            else:
                newsel.append(s)
        if not detectSel:
            newsel.append(t)
        ns = set(newsel)
        ts.snap_elements = ns

    def toggleSnapElement(self, context, t):
        if not self.beginSilent(): return
        appendMode = False
        aob = getMyProp(context)
        aob.snapElemIncrement = False
        aob.snapElemVertex = False
        aob.snapElemEdge = False
        aob.snapElemFace = False
        if appendMode:
            self.appendElem(context, t)
        else:
            ts = context.scene.tool_settings
            ts.snap_elements = set([t])
        ts = context.scene.tool_settings
        for s in ts.snap_elements:
            if s == 'INCREMENT': aob.snapElemIncrement = True
            elif s == 'VERTEX': aob.snapElemVertex = True
            elif s == 'EDGE': aob.snapElemEdge = True
            elif s == 'FACE': aob.snapElemFace = True
        self.endSilent()

    def updateSnapElemIncrement(self, context):
        self.toggleSnapElement(context, 'INCREMENT')
    snapElemIncrement: bpy.props.BoolProperty(
        name='Snap_elem_increment',
        description='Toogle snap elem increment',
        default=False,
        update=updateSnapElemIncrement)

    def updateSnapElemVertex(self, context):
        self.toggleSnapElement(context, 'VERTEX')
    snapElemVertex: bpy.props.BoolProperty(
        name='Snap_elem_vertex',
        description='Toogle snap elem vertex',
        default=False,
        update=updateSnapElemVertex)

    def updateSnapElemEdge(self, context):
        self.toggleSnapElement(context, 'EDGE')
    snapElemEdge: bpy.props.BoolProperty(
        name='Snap_elem_edge',
        description='Toogle snap elem edge',
        default=False,
        update=updateSnapElemEdge)

    def updateSnapElemFace(self, context):
        self.toggleSnapElement(context, 'FACE')
    snapElemFace: bpy.props.BoolProperty(
        name='Snap_elem_face',
        description='Toogle snap elem face',
        default=False,
        update=updateSnapElemFace)

    def updateUpdateUI(self, context):
        aob = getMyProp(context)
        ts = context.scene.tool_settings

        if not self.beginSilent(): return
        aob.snapTranslate = ts.use_snap_translate
        aob.snapScale = ts.use_snap_scale
        aob.snapRotate = ts.use_snap_rotate
        aob.snapClosest = (ts.snap_target == 'CLOSEST')
        aob.snapCenter = (ts.snap_target == 'CENTER')
        aob.snapMedian = (ts.snap_target == 'MEDIAN')
        aob.snapActive = (ts.snap_target == 'ACTIVE')
        aob.snapElemIncrement = 'INCREMENT' in ts.snap_elements
        aob.snapElemVertex = 'VERTEX' in ts.snap_elements
        aob.snapElemEdge = 'EDGE' in ts.snap_elements
        aob.snapElemFace = 'FACE' in ts.snap_elements
        self.endSilent()
    updateUI: bpy.props.BoolProperty(
        name='FKDHHeaderUpdateUI',
        description='FKDHHeaderUpdateUI',
        default=False,
        update=updateUpdateUI)


def initBox(box):
    box.enabled = True
    box.alert = False
    box.scale_x = 1.0
    box.scale_y = 1.0

def newRow(layout):
    box = layout.box()
    initBox(box)

    row = box.row(align=True)
    initBox(row)
    return row

def setHeaderBtnCmd(aob, row, caption, iconID):
    row.prop(aob, caption, emboss=False, text=r"", icon=iconID)

def setHeaderBtn(aob, row, caption, iconID):
    row.prop(aob, caption, emboss=True, text=r"", icon=iconID)

def fkhdHeaderRegPanelUI(self, context):
    layout = self.layout

    aob = getMyProp(context)

    row = newRow(layout)
    setHeaderBtnCmd(aob, row, 'updateUI', "FILE_REFRESH")
    setHeaderBtn(aob, row, 'snapTranslate', "EVENT_T")
    setHeaderBtn(aob, row, 'snapScale', "EVENT_S")
    setHeaderBtn(aob, row, 'snapRotate', "EVENT_R")
    row = newRow(layout)
    setHeaderBtn(aob, row, 'snapClosest', "EVENT_C")
    setHeaderBtn(aob, row, 'snapCenter', "PIVOT_BOUNDBOX")
    setHeaderBtn(aob, row, 'snapMedian', "PIVOT_MEDIAN")
    setHeaderBtn(aob, row, 'snapActive', "PIVOT_ACTIVE")
    row = newRow(layout)
    setHeaderBtn(aob, row, 'snapElemIncrement', "SNAP_INCREMENT")
    setHeaderBtn(aob, row, 'snapElemVertex', "SNAP_VERTEX")
    setHeaderBtn(aob, row, 'snapElemEdge', "SNAP_EDGE")
    setHeaderBtn(aob, row, 'snapElemFace', "SNAP_FACE")


def regProperties(reg):
    regClass(reg, FKHD_HEADER_Properties)

    if reg:
        bpy.types.Scene.fkhd_header_properties = bpy.props.PointerProperty(type=FKHD_HEADER_Properties)
    else:
        del bpy.types.Scene.fkhd_header_properties

def regMain(reg):
    regProperties(reg)

    regView3DHeader(reg, fkhdHeaderRegPanelUI)

def register():
    regMain(True)

def unregister():
    regMain(False)


if __name__ == '__main__':
    register()
