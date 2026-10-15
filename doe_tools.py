import numpy as np
import matplotlib.pyplot as plt

N = 512
pitch = 8e-6  # pixel size in meters (8 µm)
waist = 1.5e-3  # beam waist in meters (1.5 mm)

def make_grid(N, pitch):
    half_span = ((N - 1) / 2) * pitch
    x_axis = np.linspace(-half_span, half_span, N)
    y_axis = np.linspace(-half_span, half_span, N)
    X, Y = np.meshgrid(x_axis, y_axis)
    return X, Y

def gaussian_beam(X, Y, waist):
    R = np.sqrt(X**2 + Y**2)
    return np.exp(-R**2 / (waist**2)) # computes the Gaussian amplitude

# horizontal cut through center:
X, Y = make_grid(N, pitch) # creates the 2D grid of coordinates
A = gaussian_beam(X, Y, waist) # computes the Gaussian amplitude at each point in the grid
horizontal_cut = A[N//2, :]  # take the middle row of the Gaussian amplitude

# x axis to mm:
x_axis_mm = X[0, :] * 1e3
y_axis_mm = Y[:, 0] * 1e3

# make plot: 
plt.figure(figsize=(8, 5))
plt.plot(x_axis_mm, horizontal_cut, label='Amplitude', color='blue', linewidth=2)
# axes labels and title
plt.xlabel('Position (mm)', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.title('Gaussian Beam Profile', fontsize=14)
plt.legend()
plt.grid(True)
# Show the plot
#plt.show()

# Show the full 2D Gaussian beam profile as an image
#plt.figure(figsize=(6, 6))
#plt.imshow(A, extent=[x_axis_mm[0], x_axis_mm[-1], y_axis_mm[0], y_axis_mm[-1]], aspect='auto')
#plt.xlabel('Position (mm)', fontsize=12)
#plt.ylabel('Position (mm)', fontsize=12)
#plt.title('Gaussian Beam Profile', fontsize=14)
#plt.colorbar(label='Amplitude')
#plt.show()

# Boolean mask for pixels inside a 3 mm diameter circle:
R = np.sqrt(X**2 + Y**2) 
# computes the radius R from the center of the grid
# coordinates are now real physical distance from center in meters
# coordinates get bigger as you move away from the center of the grid
mask = R <= 1.5e-3  
# "true" inside the circle, "false" outside
# so it's true until the radius is bigger than 1.5 mm, then it's false
##print(f"Fraction of True pixels: {np.sum(mask) / mask.size:.4f}")




# Show the mask as an image
#plt.figure(figsize=(6, 6))
#plt.imshow(mask, extent=[x_axis_mm[0], x_axis_mm[-1], y_axis_mm[0], y_axis_mm[-1]], aspect='auto')
#plt.xlabel('Position (mm)', fontsize=12)
#plt.ylabel('Position (mm)', fontsize=12)
#plt.title('Boolean Mask', fontsize=14)
#plt.colorbar(label='Mask')
#plt.show()




# put two images side by side: Gaussian beam and mask
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(A, extent=[x_axis_mm[0], x_axis_mm[-1], y_axis_mm[0], y_axis_mm[-1]], aspect='auto')
plt.xlabel('Position (mm)', fontsize=12)
plt.ylabel('Position (mm)', fontsize=12)
plt.title('Gaussian Beam Profile', fontsize=14)
plt.colorbar(label='Amplitude')

plt.subplot(1, 2, 2)
plt.imshow(mask, extent=[x_axis_mm[0], x_axis_mm[-1], y_axis_mm[0], y_axis_mm[-1]], aspect='auto')
plt.xlabel('Position (mm)', fontsize=12)
plt.ylabel('Position (mm)', fontsize=12)
plt.title('Boolean Mask', fontsize=14)
plt.colorbar(label='Mask')
plt.show()


# create 512 x 512 targets:


# ring:
N = 512
# make coordinate system:
half_span = ((N - 1) / 2) * pitch
x_axis = np.linspace(-half_span, half_span, N)
y_axis = np.linspace(-half_span, half_span, N)
X, Y = np.meshgrid(x_axis, y_axis)
R = np.sqrt(X**2 + Y**2)
mask0 = (R <= 1.5e-3) & (R >= 1e-3)
# plot:
plt.figure(figsize=(6, 6))
# imshow shows 2D array, extent scales it to mm [-x, +x, -y, +y]
extent_mm = [-half_span * 1e3, half_span * 1e3, -half_span * 1e3, half_span * 1e3]
plt.imshow(mask0, cmap='viridis', extent=extent_mm)
# formatting of plot:
plt.colorbar(label="Intensity [a.u.]")
plt.xlabel("Position $x$ [mm]")
plt.ylabel("Position $y$ [mm]")
plt.title("Ring")
plt.show()


# cross: 
line_waist = 0.1e-3 # half width of line
N = 512
# make coordinate system:
half_span = ((N - 1) / 2) * pitch
x_axis = np.linspace(-half_span, half_span, N)
y_axis = np.linspace(-half_span, half_span, N)
X, Y = np.meshgrid(x_axis, y_axis)
# create the cross mathematically:
horizontal_line = np.exp(-Y**2 / (line_waist**2))
vertical_line = np.exp(-X**2 / (line_waist**2))
# combine the lines, np.maximum is important so that intensity doesn't double at crossing of lines
target = np.maximum(horizontal_line, vertical_line)
# plot:
plt.figure(figsize=(6, 6))
# imshow shows 2D array, extent scales it to mm [-x, +x, -y, +y]
extent_mm = [-half_span * 1e3, half_span * 1e3, -half_span * 1e3, half_span * 1e3]
plt.imshow(target, cmap='viridis', extent=extent_mm)
# formatting of plot:
plt.colorbar(label="Intensity [a.u.]")
plt.xlabel("Position $x$ [mm]")
plt.ylabel("Position $y$ [mm]")
plt.title("Cross")
plt.show()


# 3x3 spot beamsplitter profile:
spot_waist = 0.15e-3 # radius of one spot
separation = 1.2e-3 # separation of spots
N = 512
# make coordinate system:
half_span = ((N - 1) / 2) * pitch
x_axis = np.linspace(-half_span, half_span, N)
y_axis = np.linspace(-half_span, half_span, N)
X, Y = np.meshgrid(x_axis, y_axis)
# 3x3 target initialisation (zeros)
target = np.zeros((N, N)) 
 # list of coordinates of spots:
spot_positions = [-separation, 0, separation]
# loop over 3x3 positions to add Gaussian spots:
for x_pos in spot_positions:
    for y_pos in spot_positions:
        # calculates distance to each shifted spot center:
        R_spot = np.sqrt((X - x_pos)**2 + (Y - y_pos)**2)
        # adds the spot to target matrix:
        target += np.exp(-R_spot**2 / (spot_waist**2))
# plot:
plt.figure(figsize=(6, 6))
# imshow shows 2D array, extent scales it to mm [-x, +x, -y, +y]
extent_mm = [-half_span * 1e3, half_span * 1e3, -half_span * 1e3, half_span * 1e3]
plt.imshow(target, cmap='viridis', extent=extent_mm)
# formatting of plot:
plt.colorbar(label="Intensity [a.u.]")
plt.xlabel("Position $x$ [mm]")
plt.ylabel("Position $y$ [mm]")
plt.title("3x3 Beamsplitter target (DOE)")
plt.show()


# load picture 
img = plt.imread('X:/Dokumente/UpNano/images/upnano_256x256.png')
print("image dimensions (shape):", img.shape)
# convert to grayscales
if img.ndim == 3:  # if image has RGB/RGBA channels (3rd dim)
    # Standard to calculate in grayscales:
    img_gray = 0.2989 * img[:,:,0] + 0.5870 * img[:,:,1] + 0.1140 * img[:,:,2]
else:
    img_gray = img

# Put your loaded image in the centre of a 512 × 512 zero array 
# (zero-padding). Why it matters: the target must be smaller than 
# the full far-field window, or GS wastes light and gives poor results.
N_full = 512
# make zero array:
padded_target = np.zeros((N_full, N_full))
# start and end indices of center where image will be placed:
# (512-256)/2 = 128 start; 512+256 = 768 end
start_idx = (N_full - img_gray.shape[0]) // 2
end_idx = start_idx + img_gray.shape[0]
# embed logo via slicing in center
padded_target[start_idx:end_idx, start_idx:end_idx] = img_gray
# check:
print("old shape:", img_gray.shape)
print("new shape after zero padding", padded_target.shape)

# normalise so that target total power equals total power
# of Gaussian:
w = 1.5e-3 
A = np.exp(-R**2 / (w**2)) # computes the Gaussian amplitude
np.sum(A**2) # sum over all amplitude squares = intensity
np.sum(padded_target**2)

