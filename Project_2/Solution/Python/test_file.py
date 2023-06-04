class test:
    def __init__(self) -> None:
        self.var = 0
        

def test_func(variable, value):
    variable = value
    
tet = test()
print(tet.var)

test_func(tet.var, 5)
print(tet.var)