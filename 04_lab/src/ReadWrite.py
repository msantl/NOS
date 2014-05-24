import re
from collections import defaultdict

import base64
import binascii

def to_camel_case(str):
    str = re.sub(' ', '_', str)
    str = re.sub(':', '', str)
    return str.lower()

def format60(text):
    position = 0
    formatted = ""

    while position < len(text):
        if position + 60 < len(text):
            formatted += text[position:position + 60] + "\n\t"
        else:
            formatted += text[position:]

        position += 60

    return formatted

class ReadWrite:

    START_SEQUENCE = "---BEGIN OS2 CRYPTO DATA---"
    END_SEQUENCE = "---END OS2 CRYPTO DATA---"

    def __init__(self):
        pass

class Writer(ReadWrite):
    def __init__(self, filename):
        self.filename = filename
        self.filehandle = None

    def open(self):
        self.filehandle = open(self.filename, "w")
        self.filehandle.write(self.START_SEQUENCE + "\n")

    def close(self):
        if self.filehandle:
            self.filehandle.write(self.END_SEQUENCE + "\n")
            self.filehandle.close()

    def set_description(self, content):
        # string
        if self.filehandle:
            self.filehandle.write("Description:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_method(self, content):
        # string
        if self.filehandle:
            self.filehandle.write("Method:\n")
            for method in content:
                self.filehandle.write("\t" + method +"\n")
            self.filehandle.write("\n")

    def set_secret_key(self, content):
        # hex
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Secret key:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_key_length(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Key length:\n")
            for key_length in content:
                self.filehandle.write("\t" + key_length +"\n")
            self.filehandle.write("\n")

    def set_initialization_vector(self, content):
        # hex
        content = binascii.hexlify(content)
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Initialization vector:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_modulus(self, content):
        # hex
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Modulus:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_private_exponent(self, content):
        # hex
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Private exponent:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_public_exponent(self, content):
        # hex
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Public exponent:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_data(self, content):
        # base64
        content = base64.b64encode(content)
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Data:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_signature(self, content):
        # hex
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Signature:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_file_name(self, content):
        # string
        if self.filehandle:
            self.filehandle.write("File name:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_envelope_data(self, content):
        # base64
        content = base64.b64encode(content)
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Envelope data:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_envelope_crypt_key(self, content):
        # hex
        content = binascii.hexlify(content)
        content = format60(content)
        if self.filehandle:
            self.filehandle.write("Envelope crypt key:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

class Reader(ReadWrite):

    def __init__(self, filename):
        self.content = defaultdict(list)
        file_content = False

        print "Loading file ", filename, " ...",

        file_handle = open(filename, "r")

        file_entry = None
        file_value = []

        for line in file_handle:
            line = line.rstrip()

            if line == self.START_SEQUENCE:
                file_content = True
            elif line == self.END_SEQUENCE:
                file_content = False
            elif file_content == True:
                if not len(line):
                    self.content[file_entry] = file_value
                    file_entry = None
                    file_value = []
                elif file_entry:
                    file_value.append(line.lstrip().rstrip())
                else:
                    file_entry = to_camel_case(line)

        print "Done"
        file_handle.close()

    def get_description(self):
        # string
        return ''.join(self.content['description'])

    def get_method(self, x):
        # string
        return self.content['method'][x]

    def get_secret_key(self):
        # hex
        content = ''.join(self.content['secret_key'])
        return (long(content, 16))

    def get_key_length(self, x):
        # hex
        return (long(self.content['key_length'][x], 16))

    def get_initialization_vector(self):
        # hex
        content = ''.join(self.content['initialization_vector'])
        return binascii.unhexlify(content)

    def get_modulus(self):
        # hex
        content = ''.join(self.content['modulus'])
        return (long(content, 16))

    def get_private_exponent(self):
        # hex
        content = ''.join(self.content['private_exponent'])
        return (long(content, 16))

    def get_public_exponent(self):
        # hex
        content = ''.join(self.content['public_exponent'])
        return (long(content, 16))

    def get_data(self):
        # base64
        content = ''.join(self.content['data'])
        return base64.b64decode(content)

    def get_signature(self):
        # hex
        content = ''.join(self.content['signature'])
        return (long(content, 16))

    def get_file_name(self):
        # string
        return ''.join(self.content['file_name'])

    def get_envelope_data(self):
        # base64
        content = ''.join(self.content['envelope_data'])
        return base64.b64decode(content)

    def get_envelope_crypt_key(self):
        # hex
        content = ''.join(self.content['envelope_crypt_key'])
        return binascii.unhexlify(content)

