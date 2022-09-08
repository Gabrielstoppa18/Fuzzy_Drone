import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def fuzzy(r,p):
    rotate = ctrl.Antecedent(np.arange(-420,420,1),"R")

    position = ctrl.Antecedent(np.arange(-340,340,1),"P")

    velocityR=ctrl.Consequent(np.arange(-60,60,1),'velocity R')
    velocityP=ctrl.Consequent(np.arange(-60,60,1),'velocity P')
    #position =ctrl.Consequent(np.arange(-60,60,1),'position')

    velocityR['esquerda']= fuzz.trimf(velocityR.universe,[-60,-60,0])
    velocityP['desce']= fuzz.trimf(velocityP.universe,[-60,-60,0])
    velocityR['direita']= fuzz.trimf(velocityR.universe,[0,60,60])
    velocityP['sobe']= fuzz.trimf(velocityP.universe,[0,60,60])
    velocityR['zero']= fuzz.trimf(velocityR.universe,[-30,0,30])
    velocityP['zero']= fuzz.trimf(velocityP.universe,[-30,0,30])
    rotate.automf(number=3, names=['esquerda','zero','direita'])
    position.automf(number=3, names=['sobe','zero','desce'])

    r1=ctrl.Rule(rotate['esquerda'],velocityR['esquerda'])
    r2=ctrl.Rule(rotate['direita'],velocityR['direita'])
    r3=ctrl.Rule((position['sobe']),velocityP['sobe'])
    r4=ctrl.Rule((position['desce']),velocityP['desce'])
    r5=ctrl.Rule((rotate['zero']),velocityR['zero'])
    r6=ctrl.Rule((position['zero']),velocityP['zero'])

    sis_controle=ctrl.ControlSystem([r1,r2,r3,r4,r5,r6])
    sis=ctrl.ControlSystemSimulation(sis_controle)

    sis.input['R']=r
    sis.input['P']=p
    sis.compute()

    return[sis.output['velocity R'],sis.output['velocity P']]
