import numpy as np
import matplotlib.pyplot as plt

# 0. create coordinate system, load target, 
# create A_start, phi_start

def make_grid(N, pitch): # generates 2D matrix in meters
    half_span = ((N - 1) / 2) * pitch
    x_axis = np.linspace(-half_span, half_span, N)
    y_axis = np.linspace(-half_span, half_span, N)
    X, Y = np.meshgrid(x_axis, y_axis)
    x_min, x_max = np.min(x_axis) * 1e3, np.max(x_axis) * 1e3
    y_min, y_max = np.min(y_axis) * 1e3, np.max(y_axis) * 1e3
    extent_mm = [x_min, x_max, y_min, y_max]
    return X, Y, extent_mm

def make_grid_far(wavelength, f, N, pitch):
    far_field_pitch = (wavelength * f) / (N * pitch)
    far_field_half_span = ((N - 1) / 2) * far_field_pitch
    # Convert to millimeters for scale
    extent_far_mm = [-far_field_half_span * 1e3, far_field_half_span * 1e3, 
                     -far_field_half_span * 1e3, far_field_half_span * 1e3]
    return extent_far_mm

def load_target(N_full, pitch, waist):
    img = plt.imread('X:/Dokumente/UpNano/images/upnano_256x256.png')
    print("image dimensions (shape):", img.shape)
    # convert to grayscales
    if img.ndim == 3:  # if image has RGB/RGBA channels (3rd dim)
        # Standard to calculate in grayscales:
        img_gray = 0.2989 * img[:,:,0] + 0.5870 * img[:,:,1] + 0.1140 * img[:,:,2]
    else:
        img_gray = img
    # invert intensity:
    img_gray = np.max(img_gray) - img_gray
    N_full
    # make zero array:
    padded_target = np.zeros((N_full, N_full))
    # start and end indices of center where image will be placed:
    start_idx = (N_full - img_gray.shape[0]) // 2
    end_idx = start_idx + img_gray.shape[0]
    # embed logo via slicing in center
    padded_target[start_idx:end_idx, start_idx:end_idx] = img_gray
    # normalise so target total power = total power of Gaussian:
    waist
    pitch  # pixel size in meters (8 µm)
    half_span = ((N_full - 1) / 2) * pitch
    x_axis = np.linspace(-half_span, half_span, N_full)
    y_axis = np.linspace(-half_span, half_span, N_full)
    X, Y = np.meshgrid(x_axis, y_axis)
    R = np.sqrt(X**2 + Y**2)
    A = np.exp(-R**2 / (waist**2)) # computes the Gaussian amplitude
    np.sum(A**2) # sum over all amplitude squares = intensity
    np.sum(padded_target)
    print(f"Gaussian intensity: {np.sum(A**2)}")
    print(f"Image intensity: {np.sum(padded_target)}")
    ratio = np.sum(padded_target) / np.sum(A**2)
    print(f"Image/Gaussian: {np.sum(ratio)}")
    intensity_normalised = padded_target / np.sum(ratio)
    print(f"Intensity normalised: {np.sum(intensity_normalised)}")
    return np.sqrt(intensity_normalised) # A_target (normalised amplitude of target picture)

def gaussian_beam(X, Y, waist): # computes Gaussian amplitude profile
    R = np.sqrt(X**2 + Y**2)
    return np.exp(-R**2 / (waist**2)) 

def create_phi_start(N):
    rng = np.random.default_rng(seed=42) # Initialize modern 
        # NumPy random number generator with fixed seed
        # choose any integer for seed (like 42). 
        # Changing integer alters random pattern.
    phi_start = rng.random((N, N)) * (2 * np.pi)
    # checks to verify repeatability and range limits
    print(f"Matrix shape:            {phi_start.shape}")
    print(f"Min phase angle:      {np.min(phi_start):.4f} rad")
    print(f"Max phase angle:      {np.max(phi_start):.4f} rad")
    print(f"Control value at:   {phi_start[0,0]:.6f} rad (always same)")
    return phi_start

def intensity(A):
    I = np.abs(A)**2
    return I


# Show images:
def show_one_extent(img1, extent1, title1):
    plt.figure(figsize=(7, 6))
    # use 'inferno' or 'viridis' colormap to clearly see intensity gradients
    plt.imshow(img1, cmap='inferno', extent=extent1)

    plt.colorbar(label="Intensity $|U|^2$ [a.u.]")
    plt.xlabel("Position x / mm")
    plt.ylabel("Position y / mm")
    plt.title(title1)
    plt.grid(color='white', linestyle='--', alpha=0.2)

    plt.show()

def show_pair_extent(img1, extent1, title1, img2, extent2, title2):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    # first image on the left:
    im1 = axs[0].imshow(img1, cmap='viridis', extent=extent1)
    axs[0].set_title(title1)
    axs[0].set_xlabel("Position x / mm", fontsize=12)
    axs[0].set_ylabel("Position y / mm", fontsize=12)
    fig.colorbar(im1, ax=axs[0], shrink=0.8, label="Value [a.u.]")
    # second image on the right:
    im2 = axs[1].imshow(img2, cmap='viridis', extent=extent2)
    axs[1].set_title(title2)
    axs[1].set_xlabel("Position x / mm", fontsize=12)
    axs[1].set_ylabel("Position y / mm", fontsize=12)
    fig.colorbar(im2, ax=axs[1], shrink=0.8, label="Value [a.u.]")
    
    plt.tight_layout()
    plt.show()


# 1. DOE-plane field (U): beam amplitude * exp(i(phi)), 
# phi is random at first

def U_source(A, phi):
    U = A * np.exp(1j * phi)
    return U


# 2. propagate beam into far-field V = propagate(U), 
# measure error vs target here

def propagate(U):
    U_uncentered = np.fft.ifftshift(U)
    V_raw = np.fft.fft2(U_uncentered, norm="ortho") #norm="ortho" makes it unitary
    V_centered = np.fft.fftshift(V_raw)
    return V_centered

# Check absolute value mismatch and maximum individual entry 
# variance
def error_V_vs_target(V, A_target):
    total_absolute_error = np.sum(np.abs(V - A_target))
    max_coordinate_drift = np.max(np.abs(V - A_target))
    print(f"Total cumulative grid error: {total_absolute_error:.2e}")
    print(f"Maximum pixel peak variance: {max_coordinate_drift:.2e}")
    print(f"Unitary power conservation check: Is energy identical? {np.allclose(V, A_target)}")


# 3. impose the target. V = replace_amplitude(V, target);
# the phase of V is kept

def replace_amplitude1(V, A_target):
    # extract phase angle from field U:
    phase = np.angle(V)
    # combine new amplitude with original phase info:
    V_new = A_target * np.exp(1j * phase)
    return V_new


# 4. Impose the beam. U = replace_amplitude(U, beam);
# its phase becomes the new phi

def backpropagate(V):
    V_uncentered = np.fft.ifftshift(V)
    U_raw = np.fft.ifft2(V_uncentered, norm="ortho")
    U_centered = np.fft.fftshift(U_raw)
    return U_centered

def replace_amplitude2(U, A_beam):
    # extract phase angle from field U:
    phase = np.angle(U)
    # combine new amplitude with original phase info:
    U_new = A_beam * np.exp(1j * phase)
    return U_new

# 5. if error stops falling (convergence) -> phi is DOE design;
# if not repeat circling with new U(beam)

# some function to compare error of last round vs current round

def U_source(A, phi):
    U = A * np.exp(1j * phi)
    return U



# GS: 
X, Y, extent_mm = make_grid(512, 8e-6)
extent_far_mm = make_grid_far(633e-9, 0.2, 512, 8e-6)
A_beam = gaussian_beam(X, Y, 1.5e-3)
phi_start = create_phi_start(512)

A_target = load_target(512, 8e-6, 1.5e-3)
U_beam = U_source(A_beam, phi_start)

for iteration in range(100):
    print(f"running iteration step {iteration + 1}...")
    V_beam = propagate(U_beam)
    error_V_vs_target(intensity(V_beam), intensity(A_target))
    V_new = replace_amplitude1(V_beam, A_target)
    U_back = backpropagate(V_new)
    U_beam = replace_amplitude2(U_back, A_beam)
print("Loop finished")

U_final = propagate(U_beam)
show_one_extent(intensity(U_final), extent_far_mm, "Far-field one pass")



def make_height_map_16bit(U_final, wavelength, n_resin, n_ambient):
    phi_final = np.angle(U_final) # extract phase angle from field U
    phi_wrapped = np.mod(phi_final, 2 * np.pi) # norm to 0-2pi
    h_max = wavelength / (n_resin - n_ambient) # max height DOE to give 2pi phase shift
    height_map = (phi_wrapped / (2 * np.pi)) * h_max
    print(f"Maximum required structure print height: {h_max * 1e6:.3f} µm")
    h_normalised = height_map / np.max(height_map)
    h_16bit = (h_normalised * 65535).astype(np.uint16)
    np.save('X:/Dokumente/UpNano/images/doe_print_height_16bit_npy', h_16bit)
    np.savetxt('X:/Dokumente/UpNano/images/doe_print_height_16bit_txt.csv', h_16bit)
    plt.imsave('X:/Dokumente/UpNano/images/doe_print_height_16bit_image.png', h_16bit)
    print("16-bit smooth height map exported successfully.")
    # flatten 2D coordinate matrices (X, Y) and physical height 
    # map (values in micrometers for clean unit import in 3D software)
    x_flat = X.flatten() * 1e3
    y_flat = Y.flatten() * 1e3
    z_flat = height_map.flatten() * 1e6
    # stack them into Nx3 array of coordinates:
    xyz_points = np.column_stack((x_flat, y_flat, z_flat))
    # save as XYZ space-separated text file:
    np.savetxt('X:/Dokumente/UpNano/code/doe_surface.xyz', xyz_points, fmt='%.4f')
    print("3D surface topography exported as .xyz file")

def make_height_map(U_final, wavelength, n_resin, n_ambient):
    phi_final = np.angle(U_final) # extract phase angle from field U
    phi_wrapped = np.mod(phi_final, 2 * np.pi) # norm to 0-2pi
    h_max = wavelength / (n_resin - n_ambient) # max height DOE to give 2pi phase shift
    height_map = (phi_wrapped / (2 * np.pi)) * h_max
    print(f"Maximum required structure print height: {h_max * 1e6:.3f} µm")
    return height_map

make_height_map_16bit(U_final, 633e-9, 1.5, 1)

