velocidade = 50
local_carro = 100

RADAR_1 = 60 #Velocidade maxima do radar 1
LOCAL_1 = 100 #Km do radar 1
RADAR_RANGER = 1 # Distancia que o radar pega

passou_velocidade_radar =  velocidade > RADAR_1 
passou_na_area_do_radar = local_carro == LOCAL_1 or local_carro == (LOCAL_1 - RADAR_RANGER) or local_carro == (LOCAL_1 + RADAR_RANGER)

if passou_na_area_do_radar:
    print('O carro passou na area do do radar')

if passou_na_area_do_radar and passou_velocidade_radar:
    print('Passou da velocidade maxima na area do radar foi e multado')

else:
    print('Esta dentro do limite de velocidade')