import binascii
import PIL
import io, sys

e=sys.exit

# Open plaintext file with hex
picture_hex = open('test.JPG','rb').read()

# Convert hex to binary data
picture_bytes = binascii.unhexlify(picture_hex)

# Convert bytes to stream (file-like object in memory)
picture_stream = io.BytesIO(picture_bytes)

# Create Image object
picture = PIL.Image.open(picture_stream)

#display image
picture.show()

# print whether JPEG, PNG, etc.
print(picture.format)