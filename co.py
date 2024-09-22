#File Compression
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import os
import heapq
class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.heap=[]
        self.codes={}
        self.reverse_mapping={}
    class HeapNode:
        def __init__(self,char,freq):
            self.left=None
            self.right=None
            self.char=char
            self.freq=freq
        def __lt__(self,other):
            return self.freq<other.freq
        def __eq__(self,other):
            if(other==None):
                return False
            if(not isinstance(other,HeapNode)):
               return False
            return self.freq == other.freq

    def make_heap(self,frequency):
        #make priority Queue
        for key in frequency:
            node=self.HeapNode(key,frequency[key])
            heapq.heappush(self.heap,node)
    def make_frequency_dict(self,text):
        #calc frequency dictionary
        frequency={}
        for character in text:
            if not character in frequency:
                frequency[character]=0
            frequency[character]+=1
        return frequency
    
    
    def merge_codes(self):
        #build huffman tree.Save root node in heap
        while(len(self.heap)>1):
            node1=heapq.heappop(self.heap)
            node2=heapq.heappop(self.heap)
            merged=self.HeapNode(None,node1.freq+node2.freq)
            merged.left=node1
            merged.right=node2
            heapq.heappush(self.heap,merged)
            
    def make_codes(self):
        #make code for characters and save
        root=heapq.heappop(self.heap)
        current_code='0'
        self.make_codes_helper(root,current_code)
    def make_codes_helper(self,node,current_code):
        if(node==None):
            return
        if(node.char !=None):
            self.codes[node.char]=current_code
            self.reverse_mapping[current_code]=node.char
        self.make_codes_helper(node.left,current_code+'0')
        self.make_codes_helper(node.right,current_code+'1')
    def get_byte_array(self,padded_encoded_text):
        #convert bits into bytes return byte array
        b=bytearray()
        for i in range(0,len(padded_encoded_text),8):
            byte=padded_encoded_text[i:i+8]
            b.append(int(byte,2))
        return b
    def pad_encoded_text(self,encoded_text):
        #pad encoded text and return
        extra_padding=8-len(encoded_text)%8
        for i in range(extra_padding):
            encoded_text+="0"

        padded_info="{0:08b}".format(extra_padding)
        encoded_text=padded_info+encoded_text
        return encoded_text
    def get_encoded_text(self,text):
        #replace charactes with code and return
        encoded_text=""
        for character in text:
            encoded_text+=self.codes[character]
        
        return encoded_text
    def compress(self):
        filename,file_extension=os.path.splitext(self.path)
        output_path=filename+".bin"
        with open(self.path,'r') as file,open(output_path,'wb') as output:
            text=file.read()
            text.rstrip()
            frequency=self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_codes()
            self.make_codes()
            encoded_text=self.get_encoded_text(text)
            padded_encoded_text=self.pad_encoded_text(encoded_text)
            b=self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))
        print("Compressed")
        return output_path
    def remove_padding(self,bit_string):
        #remove padding and return
        padded_info=bit_string[:8]
        extra_padding=int(padded_info,2)
        bit_string=bit_string[8:]
        encoded_text=bit_string[:-1*extra_padding]

        return encoded_text
    
    
    def  decode_text(self,encoded_text):
        #decode and return it
        current_code=""
        decoded_text=""
        for bit in encoded_text:
            current_code+=bit
            if(current_code in self.reverse_mapping):
                character=self.reverse_mapping[current_code]
                decoded_text+=character
                current_code=""
        return decoded_text
    def decompress(self,input_path):
        filename,file_extension=os.path.splitext(input_path)
        output_path=filename+"_decompressed"+".txt"
        with open(input_path,"rb") as file,open(output_path,'w') as output:
            bit_string=""
            byte=file.read(1)
            while(len(byte)>0):
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read(1)
            encoded_text=self.remove_padding(bit_string)
            print(self.reverse_mapping)
            decoded_text=self.decode_text(encoded_text)
            output.write(decoded_text)
            print("Decompressed")
            return output_path

def gcompress():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", "*.txt")])
    global huffman
    huffman = HuffmanCoding(file_path)
    output_path = huffman.compress()
    messagebox.showinfo("Success", f"File compressed successfully!\nSaved as: {output_path}")
     

def gdecompress():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Compressed Files", "*.bin")])
    output_path = huffman.decompress(file_path)
    messagebox.showinfo("Success", f"File decompressed successfully!\nSaved as: {output_path}")

# Create the main application window
window = tk.Tk()
huffman = HuffmanCoding("")
window.title("File Compressor")
icon_image = Image.open("icon.png")  # Load your .png icon
icon_photo = ImageTk.PhotoImage(icon_image)
window.iconphoto(False, icon_photo)
title_label = tk.Label(window, text="File Compressor", font=("Helvetica", 16, "bold"), fg="blue")
title_label.pack(pady=20)

compress_button = tk.Button(window, text="Compress File", command=gcompress,bg="#4CAF50", fg="white",font=("Helvetica", 12))
compress_button.pack(pady=10, padx=20)

decompress_button = tk.Button(window, text="Decompress File", command=gdecompress, bg="#f44336", fg="white", font=("Helvetica", 12))
decompress_button.pack(pady=10, padx=20)

window.mainloop()


   





            





            
