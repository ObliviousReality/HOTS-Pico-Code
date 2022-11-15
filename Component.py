class Component:

    updateReset = 10
    updateTimer = 0

    def __init__(self) -> None:
        pass

    def init(self):
        pass

    def update(self):
        pass

    def setResetTimer(self, input):
        self.updateReset = input

    def getResetTimer(self):
        return self.updateReset

    def check(self):
        if self.updateTimer > 0:
            self.updateTimer -= 1
            return False

        self.updateTimer = self.updateReset
        return True
