from astropy.io import fits
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.stats import LombScargle
import glob
%matplotlib inline


stash = glob.glob('./FITSfiles/*.fits')
best_periods = np.zeros(len(stash))
fap = np.zeros(len(stash))
for i in range(len(stash)):

    hdu = fits.open(stash[i])
    data = hdu[1].data
    ok = np.where((data['QUALITY'] == 0) & ((data['TIME']< 2572) | (data['TIME']> 2578)))

    medflux = pd.rolling_median(data['FCOR'][ok], 500, center=True)
    ok2 = np.isfinite(medflux)

#     model = periodic.LombScargleFast(fit_period=True)
#     model.optimizer.period_range = (.2, 25)
#     model.fit(data['TIME'][ok][ok2], data['FCOR'][ok][ok2]- medflux[ok2], data['FRAW_ERR'][ok][ok2]);
    periods = np.linspace(.2, 25, 10000)
#     scores = model.score(periods)
    model = LombScargle(data['TIME'][ok][ok2], data['FCOR'][ok][ok2]- medflux[ok2], data['FRAW_ERR'][ok][ok2])
    pwr = model.power(1/periods)

    fig, ax = plt.subplots(1,2)
    fig.set_size_inches(13,5)

    ax[0].plot(data['TIME'][ok], data['FCOR'][ok], alpha =.5, label= 'FCOR');
    ax[0].plot(data['TIME'][ok][ok2], medflux[ok2], alpha =.5, label= 'medflux');
    #ax[0].plot(data['TIME'][ok], data['FLUX'][ok], alpha =.5, label= 'FLUX');
    #ax[0].plot(data['TIME'][ok], data['FRAW'][ok], alpha =.5, label= 'FRAW');
    #ax[0].set_xlim(2.0,3.6);
    #ax[0].set_ylim(0,700);
    ax[0].set_xlabel("Time(days)");
    ax[0].set_ylabel("Flux");
    ax[0].legend()

    ax[1].plot(periods, pwr);
    ax[1].set_xscale('log')
    ax[1].set_xlabel("Period(days)");
    ax[1].set_ylabel("Power");
    plt.show()

    best_period = periods[np.argmax(pwr)]
    print(best_period)
    best_periods[i] = best_period
    fap[i] = model.false_alarm_probability(pwr.max())
