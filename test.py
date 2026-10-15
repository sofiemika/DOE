import numpy as np
import matplotlib


variable = wl = 633e-9  # Wavelength in meters (633 nm)
variable = focal_length = 200e-3  # Focal length in meters (200 mm)

print(f"Lambda: {wl} m, Focal Length: {focal_length} m")

wavelengths = [405e-9, 532e-9, 633e-9, 780e-9, 850e-9, 1064e-9] #wavelength list in m

print(f"Lowest wavelength: {wavelengths[0]*1e9:.0f} nm")
print(f"Highest wavelength: {wavelengths[-1]*1e9:.0f} nm")
print(f"Number of wavelengths: {len(wavelengths)}")

for wave in wavelengths:
    print(f"Wavelength {wavelengths.index(wave)}: {wave*1e9:.0f} nm")


variable = N = 512
variable = x_in = 8e-6  # Input pixel size in meters (8 µm)
for wave in wavelengths:
    variable = x_out = (wave * focal_length) / (N * x_in)
    print(f"Far-field pixel size {wavelengths.index(wave)}: {x_out*1e6:.2f} µm")
    if wave >380e-9 and wave < 750e-9:
        print(f"for visible wavelength {wavelengths.index(wave)}: {wave*1e9:.0f} nm")
    else:
        print(f"for non-visible wavelength {wavelengths.index(wave)}: {wave*1e9:.0f} nm")


