class Enemy:
    def __init__(self, typ_potwora):
        if typ_potwora == 1:
            self.potwor1()
        elif typ_potwora == 2:
            self.potwor2()
        elif typ_potwora == 3:
            self.potwor3()

    def potwor1(self, ID):
        self.potwor = 1
        self.enemyID = self
        self.size = 64
        self.positionX = 50
        self.positionY = 50
        self.positionXChange = 1
        self.positionYChange = 40

        '''Stwórz atrybuty o wartościach dla potwora typu 1'''

    def potwor2(self):
        self.potwor = 2
        '''Stwórz atrybuty o wartościach dla potwora typu 2'''

    def potwor3(self):
        self.potwor = 3
        '''Stwórz atrybuty o wartościach dla potwora typu 3'''


a = Enemy(1)
print (a.enemyID)