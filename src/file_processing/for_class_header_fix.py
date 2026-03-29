
print('class')

for i in range(24): 
    print('fits read spw' + str(i) + '.fits')
    print('SET OBSERVATORY MAUNA_KEA')
    print('set variab position write')
    print('R%HEAD%POS%SYSTEM = 2')
    print('R%HEAD%POS%LAM = 1.6270837042') 
    print('R%HEAD%POS%BET = 3.1399525289e-01') 
    print('MODIFY DOPPLER 0')
    print('modi velo 7')
    print('set unit v f')
    print('pl')
    print('number = ' + str(1+i) )   
    
    if i == 0:
        print('file out s255IR_REG1 mult')
    else:
        print('file out s255IR_REG1')  
    print('write')
