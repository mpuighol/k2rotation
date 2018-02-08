from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from gatsby import periodic

file = 'hlsp_everest_k2_llc_220133060-c08_kepler_v2.0_lc.fits'
hdu = fits.open(file)
data = hdu[1].data

ok = np.where((data['QUALITY'] == 0))

plt.figure()
plt.scatter(data['TIME'][ok], data['FCOR'][ok])
plt.show

model = periodic.LombScargleFast(fit_period=True)

model.optimizer.period_range = (.2, 25)

model.fit(data['TIME'][ok], data['FCOR'][ok], data['FRAW_ERR'][ok]);

periods = np.linspace(.2, 25, 10000)
scores = model.score(periods)

plt.figure()
plt.plot(periods, scores)
plt.xlabel('Period(days)')
plt.xscale('log')
plt.ylabel('Power')
plt.show()
