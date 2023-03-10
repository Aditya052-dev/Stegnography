from PIL import Image
from stegano import lsb

def hide_text():
    b = int(input(":: Welcome to Text-Steganography ::\n"
                            "1. Encode\n2. Decode\n"))

    if (b == 1):
        im = input("Enter the name of image(with extension): ")
        txt_hide = input("Enter the message to be hidden :")
        secret = lsb.hide(im, txt_hide)
        sec_im = input("Enter the name of the secret image :")
        secret.save(sec_im)
        print("Image encoded successfully...!!!")
    
    elif (b == 2):
        rev = input("Enter image name to be decoded ")
        print("Image decoded successfully...!!!")
        print("The hidden tex message is :",lsb.reveal(rev))
    else:
        raise Exception("Enter correct input")


class Steganography(object):

    def __int_to_bin(rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        """
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))


    def __bin_to_int(rgb):
        """Convert a binary (string) tuple to an integer tuple.

        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

 
    def __merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.

        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    def merge(img1, img2):
        """Merge two images. The second one will be merged into the first one.

        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """

        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = Steganography.__int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.__merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

        return new_image

    def unmerge(img):
        """Unmerge an image.

        :param img: The input image.
        :return: The unmerged/extracted image.
        """

        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image
		
def hide_img():
    a = int(input(":: Welcome to Image-Steganography ::\n"
                            "1. Encode\n2. Decode\n"))
    if (a == 1):
        img1 = input("Enter image name to be encoded(with extension) :")
        img2 = input("Enter the image to be hidden(with extension) :")
        output = input("Enter the name of the new image created by encoding(with extension) :")
        merged_image = Steganography.merge(Image.open(img1), Image.open(img2))
        merged_image.save(output)
        print("Image encoded successfully...!!!")
    
    elif (a == 2):
        img = input("Enter image to be decoded(with extension) :")
        output = input("Enter the name of the decoded image(with extension) :")
        unmerged_image = Steganography.unmerge(Image.open(img))
        unmerged_image.save(output)
        print("Image decoded successfully...!!!")
    else:
        raise Exception("Enter correct input")

def main():
    c = int(input(":: Welcome to Steganography ::\n"
                            "1. Image-Steganography\n2. Text-Steganography\n"))
    if (c==1):
        hide_img()
    elif (c==2):
        hide_text()
    else:
        raise Exception("Enter correct input")
    
    # Driver Code
if __name__ == '__main__' :
   main()
    