from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from gatspy import periodic

stash = glob.glob('./FITSfiles/*.fits')

#file = 'hlsp_everest_k2_llc_220133060-c08_kepler_v2.0_lc.fits'
#hdu = fits.open(file)
#data = hdu[1].data

ok = np.where((data['QUALITY'] == 0))



model = periodic.LombScargleFast(fit_period=True)

model.optimizer.period_range = (.2, 25)

model.fit(data['TIME'][ok], data['FCOR'][ok], data['FRAW_ERR'][ok]);

periods = np.linspace(.2, 25, 10000)
scores = model.score(periods)




fig, ax = plt.subplots(1,2)
fig.set_size_inches(13,5)

ax[0].plot(data['TIME'][ok], data['FCOR'][ok]);
#ax[0].set_xlim(2.0,3.6);
#ax[0].set_ylim(0,700);
ax[0].set_xlabel("Flux");
ax[0].set_ylabel("Period(days)");

ax[1].plot(periods, scores);
ax[1].set_xscale('log')
ax[1].set_xlabel("Period(days)");
ax[1].set_ylabel("Power");

#download 10 objects $$
#make it loop over all of them
#use glob $$
#create two panel plot for lightcurve and periodogram $$
#save best period for each
