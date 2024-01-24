import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


broj_traka = 3   
duzina_puta = 50 
brzina_prometa =1   
broj_vozila = 5   


put = np.zeros((broj_traka, duzina_puta))


pocetne_pozicije = np.random.choice(duzina_puta, broj_vozila, replace=False)
put[0, pocetne_pozicije] = 1


def korak_simulacije(frameNum, put, slika, duzina_puta, broj_traka, brzina_prometa):
    novi_put = np.zeros_like(put)

    for traka in range(broj_traka):
        for pozicija in range(duzina_puta):
            if put[traka, pozicija] == 1:
                
                nova_pozicija = (pozicija + brzina_prometa) % duzina_puta
                novi_put[traka, nova_pozicija] = 1

    
    put[:, :] = novi_put[:, :]

    
    slika.set_array(put)

    return slika,


fig, ax = plt.subplots()
slika = ax.imshow(put, interpolation='nearest', cmap='Greens')

ani = animation.FuncAnimation(fig, korak_simulacije, fargs=(put, slika, duzina_puta, broj_traka, brzina_prometa),
                              frames=50, interval=500, save_count=50)

plt.show()
