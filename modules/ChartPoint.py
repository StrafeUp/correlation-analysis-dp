from flask.json import JSONEncoder


class ChartPoint:
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(%.2f, %.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Point(x=%r, y=%r)" % (self.x, self.y)


class ChartPointEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ChartPoint):
            return obj.__dict__
        return JSONEncoder.default(self, obj)
