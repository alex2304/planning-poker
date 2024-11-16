class CappedDict(dict):
    def __init__(self, capacity: int):
        super(CappedDict, self).__init__()
        self.capacity = capacity
        self.order = []

    def __setitem__(self, key, value):
        if key not in self:
            if len(self) >= self.capacity:
                oldest_key = self.order.pop(0)
                del self[oldest_key]
            self.order.append(key)

        return super(CappedDict, self).__setitem__(key, value)

    def __repr__(self):
        return f"CappedDict({self})"
