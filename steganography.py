# steganography
# assignment: programming assignment 3
# author: Anya Zhang
# date: 11/4/22
"""steganography.py saves a message in an image from a given file into another file 
using a specified codec (a string used for identification of a codec class: 'binary' for the Codec class, 
'caesar' for the CaesarCypher class, or 'huffman' for the HuffmanCodes) and
returns a decoded text message hidden in a given file using a specified codec"""
# input: an image file  and codec
# output: creates new image file with encoded message or returns decoded text message hidden in image file

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None
        self.shift = 0

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec(delimiter = self.delimiter) 
        elif codec == 'caesar':
            self.shift = int(input("Enter the amount you would like shifted: "))
            self.codec = CaesarCypher(delimiter = self.delimiter, shift = self.shift)
        elif codec == 'huffman':
            self.codec = HuffmanCodes(delimiter = self.delimiter)
            self.binary = self.codec.encode(message + self.delimiter)
        binary = self.codec.encode(message + self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary

            arr = np.asarray(image)
            i = 0
            for row in range(arr.shape[0]):
                for col in range(arr.shape[1]):
                    pixel = arr[row][col]
                    for color in range(len(pixel)):
                        # check for delimiter to break out of for loops
                        if self.binary[i-8:i] == self.codec.encode(self.delimiter) or i >= len(self.binary):
                            break
                        rgb = pixel[color]
                        # rgb is even but binary is odd
                        if rgb % 2 == 0 and int(self.binary[i]) % 2 == 1:
                            arr[row][col][color] += 1
                        # rgb is odd but binary is even 
                        elif rgb % 2 == 1 and int(self.binary[i]) % 2 == 0:
                            arr[row][col][color] -= 1
                        i += 1
        print(arr)
        image = np.uint8(arr)
        cv2.imwrite(fileout, image)


    def decode(self, filein, codec):
        image = cv2.imread(filein)
        print(image) # for debugging      
        flag = True
        # convert into text
        if codec == 'binary':
            self.codec = Codec(delimiter = self.delimiter) 
        elif codec == 'caesar':
            self.codec = CaesarCypher(delimiter = self.delimiter, shift = self.shift)
        elif codec == 'huffman':
            flag = False
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
            else:
                self.codec = HuffmanCodes(delimiter = self.delimiter)
                self.binary = self.codec.encode(self.text + self.delimiter)
                self.text = self.codec.decode(self.binary)

        if flag:

            binary_data = ''
            i = 0
            # convert each number in the image array into its binary form
            for row in range(image.shape[0]):
                for col in range(image.shape[1]):
                    pixel = image[row][col]
                    for color in range(len(pixel)):
                        # check for delimiter to break out of for loops
                        if binary_data[i-8:i] == self.codec.encode(self.delimiter):
                            break
                        rgb = pixel[color]
                        bin_num = bin(rgb)
                        # extract the least significant bit
                        lsb = bin_num[-1]
                        binary_data += lsb
                        i += 1

            # update the data attributes:
            self.binary = binary_data
            self.text = self.codec.decode(binary_data)  


        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()