# Working with Binary Data in Python
The Bytes Type
The bytes type in Python is immutable and stores a sequence of values ranging from 0-255 (8-bits). You can get the value of a single byte by using an index like an array, but the values can not be modified.

# Create empty bytes
```
empty_bytes = bytes(4)
print(type(empty_bytes))
print(empty_bytes)
```
The Bytearray Type
To create a mutable object you need to use the bytearray type. With a bytearray you can do everything you can with other mutables like push, pop, insert, append, delete, and sort.

# Cast bytes to bytearray
```
mutable_bytes = bytearray(b'\x00\x0F')

```
# Bytearray allows modification
```
mutable_bytes[0] = 255
mutable_bytes.append(255)
print(mutable_bytes)

```
# Cast bytearray back to bytes
```
immutable_bytes = bytes(mutable_bytes)
print(immutable_bytes)
```
The BytesIO Class
The io.BytesIO inherits from io.BufferedReader class comes with functions like read(), write(), peek(), getvalue(). It is a general buffer of bytes that you can work with.

```
binary_stream = io.BytesIO()
# Binary data and strings are different types, so a str
# must be encoded to binary using ascii, utf-8, or other.
binary_stream.write("Hello, world!\n".encode('ascii'))
binary_stream.write("Hello, world!\n".encode('utf-8'))

```
# Move cursor back to the beginning of the buffer
```
binary_stream.seek(0)

```
# Read all data from the buffer
```
stream_data = binary_stream.read()

```
# The stream_data is type 'bytes', immutable
```
print(type(stream_data))
print(stream_data)

```
# To modify the actual contents of the existing buffer
# use getbuffer() to get an object you can modify.
# Modifying this object updates the underlying BytesIO buffer
```
mutable_buffer = binary_stream.getbuffer()
print(type(mutable_buffer))  # class 'memoryview'
mutable_buffer[0] = 0xFF

```
# Re-read the original stream. Contents will be modified
# because we modified the mutable buffer
```
binary_stream.seek(0)
print(binary_stream.read())

```

Writing Bytes to a File
# Pass "wb" to write a new file, or "ab" to append
```
with open("test.txt", "wb") as binary_file:
    # Write text or bytes to the file
    binary_file.write("Write text by encoding\n".encode('utf8'))
    num_bytes_written = binary_file.write(b'\xDE\xAD\xBE\xEF')
    print("Wrote %d bytes." % num_bytes_written)
```
Alternatively, you could explicitly call open and close, but if you do it this way you will need to do the error handling yourself and ensure the file is always closed, even if there is an error during writing. I don't recommend this method unless you have a strong reason.

```
binary_file = open("test.txt", "wb")
binary_file.write(b'\x00')
binary_file.close()
```
Reading Bytes From a File
```
with open("test_file.dat", "rb") as binary_file:
    # Read the whole file at once
    data = binary_file.read()
    print(data)
```
Read file line by line
If you are working a text file, you can read the data in line by line.

```
with open("test.txt", "rb") as text_file:
    # One option is to call readline() explicitly
    # single_line = text_file.readline()

    # It is easier to use a for loop to iterate each line
    for line in text_file:
        print(line)
```
Getting the size of a file
```
import os
file_length_in_bytes = os.path.getsize("test.txt")
print(file_length_in_bytes)
```
Seeking a specific position in a file
You can move to a specific position in file before reading or writing using seek(). You can pass a single parameter to seek() and it will move to that position, relative to the beginning of the file.

```
# Seek can be called one of two ways:
#   x.seek(offset)
#   x.seek(offset, starting_point)

# starting_point can be 0, 1, or 2
# 0 - Default. Offset relative to beginning of file
# 1 - Start from the current position in the file
# 2 - Start from the end of a file (will require a negative offset)

with open("test_file.dat", "rb") as binary_file:
    # Seek a specific position in the file and read N bytes
    binary_file.seek(0, 0)  # Go to beginning of the file
    couple_bytes = binary_file.read(2)
    print(couple_bytes)
    
```
    
Integer to Bytes
```
i = 16

# Create one byte from the integer 16
single_byte = i.to_bytes(1, byteorder='big', signed=True) 
print(single_byte)

# Create four bytes from the integer
four_bytes = i.to_bytes(4, byteorder='big', signed=True)
print(four_bytes)

# Compare the difference to little endian
print(i.to_bytes(4, byteorder='little', signed=True))

# Create bytes from a list of integers with values from 0-255
bytes_from_list = bytes([255, 254, 253, 252])
print(bytes_from_list)

# Create a byte from a base 2 integer
one_byte = int('11110000', 2)
print(one_byte)

# Print out binary string (e.g. 0b010010)
print(bin(22))
```
Bytes to Integer
```
# Create an int from bytes. Default is unsigned.
some_bytes = b'\x00\xF0'
i = int.from_bytes(some_bytes, byteorder='big')
print(i)

# Create a signed int
i = int.from_bytes(b'\x00\x0F', byteorder='big', signed=True)
print(i)

# Use a list of integers 0-255 as a source of byte values
i = int.from_bytes([255, 0, 0, 0], byteorder='big')
print(i)


```
Text Encoding
```
# Binary to Text
binary_data = b'I am text.'
text = binary_data.decode('utf-8')
print(text)

binary_data = bytes([65, 66, 67])  # ASCII values for A, B, C
text = binary_data.decode('utf-8')
print(text)
# Text to Binary
message = "Hello"  # str
binary_message = message.encode('utf-8')
print(type(binary_message))  # bytes

# Python has many built in encodings for different languages,
# and even the Caeser cipher is built in
import codecs
cipher_text = codecs.encode(message, 'rot_13')
print(cipher_text)
Base 64 Encoding
# Encode binary data to a base 64 string
binary_data = b'\x00\xFF\x00\xFF'

# Use the codecs module to encode
import codecs
base64_data = codecs.encode(binary_data, 'base64')
print(base64_data)

# Or use the binascii module
import binascii
base64_data = binascii.b2a_base64(binary_data)
print(base64_data)

# The base64_string is still a bytes type
# It may need to be decoded to an ASCII string
print(base64_data.decode('utf-8'))

# Decoding is done similarly
print(codecs.decode(base64_data, 'base64'))
print(binascii.a2b_base64(base64_data))
```
Hexadecimal
```
# Starting with a hex string you can unhexlify it to bytes
deadbeef = binascii.unhexlify('DEADBEEF')
print(deadbeef)

# Given raw bytes, get an ASCII string representing the hex values
hex_data = binascii.hexlify(b'\x00\xff')  # Two bytes values 0 and 255

# The resulting value will be an ASCII string but it will be a bytes type
# It may be necessary to decode it to a regular string
text_string = hex_data.decode('utf-8')  # Result is string "00ff"
print(text_string)
```
