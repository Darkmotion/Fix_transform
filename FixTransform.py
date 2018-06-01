import c4d
from c4d import gui

# reset pivot pos/rot
# ctrl rot only
# shift pos only


class PivotFixer:

    def __init__(self, id, objs):

        self.id = id
        self.objs = objs
        self.process()

    def process(self):
        for obj in self.objs:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE,obj)
            if self.id == 1:
                self.pos_reset(obj)
            elif self.id == 2:
                self.rot_reset(obj)
            else:
                self.rot_reset(obj)
                self.pos_reset(obj)

    @staticmethod
    def pos_reset(obj):
        if obj.GetType() == c4d.Onull:
            child = obj.GetChildren()
            if child:
                childs_mg = [item.GetMg() for item in child]
                obj.SetRelPos(c4d.Vector(0, 0, 0))
                for id, item in enumerate(child):
                    item.SetMg(childs_mg[id])
            else:
                obj.SetRelPos(c4d.Vector(0, 0, 0))
            obj.Message(c4d.MSG_UPDATE)
            return 0

        offset = obj.GetRelPos()
        transf = obj.GetMl()
        x = offset.Dot(transf.v1)
        y = offset.Dot(transf.v2)
        z = offset.Dot(transf.v3)
        offset = c4d.Vector(x, y, z)

        points = map(lambda x: offset+x, obj.GetAllPoints())
        obj.SetAllPoints(points)
        obj.SetRelPos(c4d.Vector(0, 0, 0))
        obj.Message(c4d.MSG_UPDATE)
        return 0

    @staticmethod
    def rot_reset(obj):
        if obj.GetType() == c4d.Onull:
            child = obj.GetChildren()
            if child:
                childs_mg = [item.GetMg() for item in child]
                obj.SetRelRot(c4d.Vector(0, 0, 0))
                for id, item in enumerate(child):
                    item.SetMg(childs_mg[id])
            else:
                obj.SetRelRot(c4d.Vector(0, 0, 0))
            obj.Message(c4d.MSG_UPDATE)
            return 0

        transf = obj.GetMl()
        transf.off = c4d.Vector()
        points = map(lambda x: x*transf, obj.GetAllPoints())
        obj.SetAllPoints(points)
        obj.SetRelRot(c4d.Vector(0, 0, 0))
        obj.Message(c4d.MSG_UPDATE)
        return 0


def main():

    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    state = c4d.BaseContainer()
    gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_QUALIFIER, state)
    doc.StartUndo()
    pf = PivotFixer(state.GetInt32(c4d.BFM_INPUT_QUALIFIER), objs)
    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()
