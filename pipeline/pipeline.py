class BasePipeline:
    def __init__(self, config=None):
        self.config = config

    def process(self, data):
        raise NotImplementedError