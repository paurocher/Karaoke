WINDOW_ELEMENTS = {}

def pos_pixel_to_sample(pixel, sound_surface_map):
    """Converts a pixel position to sample position."""
    return pixel * sound_surface_map

def pos_sample_to_pixel(sample, sound_surface_map):
    """Converts a sample position to pixel position."""
    return sample // sound_surface_map

