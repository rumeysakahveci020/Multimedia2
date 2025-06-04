from PIL import Image, ImageOps
import numpy as np

# Load the image
image_path = "baby.jpg"  # Replace this with your image path
image = Image.open(image_path)

# Step 1: Print image dimensions and calculate compression rate
def calculate_compression_rate(image):
    width, height = image.size
    original_bits = width * height * 24  # 24 bits per pixel for RGB
    compressed_bits = len(np.array(image).tobytes()) * 8
    compression_rate = original_bits / compressed_bits
    return width, height, compression_rate

width, height, compression_rate = calculate_compression_rate(image)
print(f"Image Dimensions: {width}x{height}")
print(f"Compression Rate: {compression_rate:.2f}")

# Step 2: Convert to YCbCr, brighten, and convert back to RGB
def brighten_image(image, increase_y=50):
    ycbcr_image = image.convert('YCbCr')
    ycbcr_array = np.array(ycbcr_image, dtype=np.uint8)
    ycbcr_array[:, :, 0] = np.clip(ycbcr_array[:, :, 0] + increase_y, 0, 255)  # Increase Y
    brightened_image = Image.fromarray(ycbcr_array, 'YCbCr').convert('RGB')
    return brightened_image

brightened_image = brighten_image(image)
brightened_image.show()  # Displays the brightened image

# Step 3: Select red shades and set Cr values to zero
def remove_red_shades(image):
    ycbcr_image = image.convert('YCbCr')
    ycbcr_array = np.array(ycbcr_image, dtype=np.uint8)
    red_mask = (ycbcr_array[:, :, 1] > 140) & (ycbcr_array[:, :, 1] < 200)  # Example Cr range
    ycbcr_array[red_mask, 2] = 0  # Set Cr to zero
    modified_image = Image.fromarray(ycbcr_array, 'YCbCr').convert('RGB')
    return modified_image

red_removed_image = remove_red_shades(image)
red_removed_image.show()  # Displays the image with red removed

# Step 4: Down-sample and up-sample Cb and Cr
def down_up_sample(image):
    ycbcr_image = image.convert('YCbCr')
    ycbcr_array = np.array(ycbcr_image, dtype=np.uint8)

    # Down-sample
    cb_downsampled = ycbcr_array[:, ::2, 1]  # Half the horizontal resolution
    cr_downsampled = ycbcr_array[:, ::2, 2]

    # Up-sample
    cb_upsampled = np.repeat(cb_downsampled, 2, axis=1)
    cr_upsampled = np.repeat(cr_downsampled, 2, axis=1)

    # Replace original Cb and Cr with up-sampled versions
    ycbcr_array[:, :, 1] = cb_upsampled
    ycbcr_array[:, :, 2] = cr_upsampled

    modified_image = Image.fromarray(ycbcr_array, 'YCbCr').convert('RGB')
    return modified_image

sampled_image = down_up_sample(image)
sampled_image.show()  # Displays the image after down/up-sampling Cb and Cr

# Step 5: Down-sample all components and observe quality change
def downsample_all_components(image):
    ycbcr_image = image.convert('YCbCr')
    ycbcr_array = np.array(ycbcr_image, dtype=np.uint8)

    # Down-sample all components
    y_downsampled = ycbcr_array[::2, ::2, 0]
    cb_downsampled = ycbcr_array[::2, ::2, 1]
    cr_downsampled = ycbcr_array[::2, ::2, 2]

    # Up-sample all components
    y_upsampled = np.repeat(np.repeat(y_downsampled, 2, axis=0), 2, axis=1)
    cb_upsampled = np.repeat(np.repeat(cb_downsampled, 2, axis=0), 2, axis=1)
    cr_upsampled = np.repeat(np.repeat(cr_downsampled, 2, axis=0), 2, axis=1)

    ycbcr_array[:, :, 0] = y_upsampled[:ycbcr_array.shape[0], :ycbcr_array.shape[1]]
    ycbcr_array[:, :, 1] = cb_upsampled[:ycbcr_array.shape[0], :ycbcr_array.shape[1]]
    ycbcr_array[:, :, 2] = cr_upsampled[:ycbcr_array.shape[0], :ycbcr_array.shape[1]]

    modified_image = Image.fromarray(ycbcr_array, 'YCbCr').convert('RGB')
    return modified_image

fully_sampled_image = downsample_all_components(image)
fully_sampled_image.show()  # Displays the image after down/up-sampling all components
