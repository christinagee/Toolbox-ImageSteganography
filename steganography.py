"""A program that encodes and decodes hidden messages in images through red_binary steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    red = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    """our task is to iterate though each pixel in the encoded image and set
    the decode_image pixel to be (0, 0, 0) or (255, 255, 255) depending on the value of that red_binary."""
    for x in range(x_size):
        for y in range(y_size):
            pix = red[x, y]
            pix_binary = bin(pix)
            #if the pixel binary is 0 then we transform it to black, if not it becomes white
            if (pix_binary[-1] == '0'):
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (255, 255, 255)

    decoded_image.save("images/decoded_image.png")

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """

    #create a new image based off the original one
    base_image = Image.open(template_image)
    original_pixels = base_image.load()
    new_image = Image.new("RGB", base_image.size)
    encoded_pixels = new_image.load()

    x_size = base_image.size[0]
    y_size = base_image.size[1]

    secret_text_image = write_text(text_to_encode, base_image.size)
    secret_text_red = secret_text_image.split()[0]
    pixel_red = secret_text_red.load()


    #encode image by converting red to a binary number and either: 1) Keeping it the same or 2)Changing from 1 to 0 or vice versa
    for i in range(x_size):
        for j in range(y_size):
            red = original_pixels[i, j][0]
            blue = original_pixels[i, j][1]
            green = original_pixels[i, j][2]

            red_binary = bin(red)[-1]

            if pixel_red[i, j] == (255, 255, 255):
                if red_binary == '1':
                    encoded_pixels[i, j] = (red, blue, green)
                elif red_binary == '0':
                    encoded_pixels[i, j] = (red + 1, blue, green)
            else:
                if red_binary == '1':
                    encoded_pixels[i, j] = (red - 1, blue, green)
                else:
                    encoded_pixels[i, j] = (red, blue, green)

    new_image.save("/Users/christinagee/Code/ToolBox-ImageSteganography/images/new_encodedimage.png")



if __name__ == '__main__':

    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image("Oh hey you've unconvered a secret message encoded by Christina")
