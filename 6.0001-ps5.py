#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:32:26 2018

@author: phillipferguson
"""

"""
# Problem Set 5
# Name: James Quigley
# Collaborators: None
# Time:
"""

from PIL import Image
import numpy

def generate_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """
    # You do not need to understand exactly how this function works.
    if color == 'red':
        c = [[.567, .433, 0],[.558, .442, 0],[0, .242, .758]]
    elif color == 'green':
        c = [[0.625,0.375, 0],[ 0.7,0.3, 0],[0, 0.142,0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0],[0, 0.433, 0.567],[0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0],[0, 1, 0.],[0, 0., 1]]
    return c

def matrix_multiply(m1,m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: the input matrices
    Returns:
        result: matrix product of m1 and m2
        in a list of floats
    """

    product = numpy.matmul(m1,m2)
    if type(product) == numpy.int64:
        return float(product)
    else:
        result = list(product)
        return result





def convert_image_to_pixels(image):
    """
    Takes an image (must be inputted as a string
    with proper file attachment ex: .jpg, .png)
    and converts to a list of tuples representing pixels.
    Each pixel is a tuple containing (R,G,B) values.

    Returns the list of tuples.

    Inputs:
        image: string representing an image file, such as 'lenna.jpg'
        returns: list of pixel values in form (R,G,B) such as
                 [(0,0,0),(255,255,255),(38,29,58)...]
    """
    pic = Image.open(image)
    #use the open function to open the image file
    pix_value = list(pic.getdata())
    #using the getdata function to save the image pixel values to a list
    return pix_value

def convert_pixels_to_image(pixels,size):
    """
    Creates an Image object from a inputted set of RGB tuples.

    Inputs:
        pixels: a list of pixels such as the output of
                convert_image_to_pixels.
        size: a tuple of (width,height) representing
              the dimensions of the desired image. Assume
              that size is a valid input such that
              size[0] * size[1] == len(pixels).
    returns:
        img: Image object made from list of pixels
    """
    img = Image.new('RGB', size)
    #creating a new image
    img.putdata(pixels)
    #using the putdata function, we copy pixel data into the image
    return img

def apply_filter(pixels, color):
    """
    pixels: a list of pixels in RGB form, such as [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red', 'blue', 'green', or 'none', must be a string representing the color
    deficiency that is being simulated.
    returns: list of pixels in same format as earlier functions,
    transformed by matrix multiplication
    """
    myMatrix = generate_matrix(color)
    #gives a matrix for a color dependent transformation
    modified_pixels = []
    for element in pixels:
        modified_pixels.append(matrix_multiply(myMatrix, list(element)))
        #append the list with the product of the generated
        #matrix and each element of the pixels list
        #the element counts as a list because the the functions uses list input
    myPixList = []
    #storing the modified pixels in a new list
    for row in modified_pixels:
        for i in range(len(row)):
            row[i] = int(row[i])
            #turn the float into an int
        myPixList.append(tuple(row))
        #appending the list with tupples
    return myPixList

def reveal_BW_image(filename):
    """
    Extracts the hidden image in the least significant bit
    of each pixel in the specified image.
    Inputs:
       filename: string, input file to be processed
    returns:
       result: an Image object containing the hidden image
    """
    pic = Image.open(filename)
    #open the image
    pixels = convert_image_to_pixels(filename)
    #get the pixel list of the image
    myList = []
    for pixel in pixels:
    #for every element that is an int, we change the pixel values
        myList+=[255*(pixel%2)]
    pixels = myList
    #same as convert_pixels_to_image with the difference being the mode is 'myList' for grayscale
    pic2 = Image.new('L', pic.size)
    pic2.putdata(pixels)
    return pic2 

def reveal_RGB_image(filename):
    """
    Extracts the hidden image in the 2 least significant bits
    of each pixel in the specified color image.
    Inputs:
        filename: string, input RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    pic = Image.open(filename)
    #open the image
    pixels = convert_image_to_pixels(filename)
    #get the pixel list of the image using convert_image_to_pixels
    myList = []
    for pixel in pixels:
    #for every tuple element in the list of pixels
        myList_0 = []
        for i in range(3):
        #for every element of the tupple
            myList_0.append((255*((pixel[i])%4)//3))
            #rescale the pixel values and add them to the empty list myList
        myList.append(tuple(myList_0))
        #converts myList into a tuple and adds it to the ret list
    return convert_pixels_to_image(myList,pic.size)
    #return image object from convert_pixels_to_image

def main():
    pass

    # UNCOMMENT the following 8 lines to test part 1

    im = Image.open('image_15.png')    
    width, height = im.size
    pixels = convert_image_to_pixels('image_15.png')
    image = apply_filter(pixels,'none')
    im = convert_pixels_to_image(image, (width, height))
    im.show()
    new_image = apply_filter(pixels,'red')
    im2 = convert_pixels_to_image(new_image,(width,height))
    im2.show()
    
#    pixels = reveal_BW_image('hidden1.bmp')
#    pixels.show()
#    im = reveal_RGB_image('hidden2.bmp')
#    im.show()
#    

    # No tests for part 2. Try to find the secret images!

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    