import re
from collections import defaultdict

def to_camel_case(str):
    str = re.sub(' ', '_', str)
    str = re.sub(':', '', str)
    return str.lower()

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
        self.filehandle = open(self.filename)
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
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_secret_key(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Secret key:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_key_length(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Key length:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_initialization_vector(self, content):
        if self.filehandle:
            self.filehandle.write("Initialization vector:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_modulus(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Modulus:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_private_exponent(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Private exponent:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_public_exponent(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Public exponent:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_data(self, content):
        # base 64
        if self.filehandle:
            self.filehandle.write("Data:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_signature(self, content):
        # hex
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
        if self.filehandle:
            self.filehandle.write("Envelope data:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

    def set_envelope_crypt_key(self, content):
        # hex
        if self.filehandle:
            self.filehandle.write("Envelope crypt key:\n")
            self.filehandle.write("\t" + content +"\n")
            self.filehandle.write("\n")

class Reader(ReadWrite):

    def __init__(self, filename):
        self.content = defaultdict(str)
        file_content = False

        print "Loading file ", filename, " ...",

        file_handle = open(filename)

        file_entry = None
        file_value = ""

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
                    file_value = ""
                elif file_entry:
                    file_value += line.lstrip().rstrip()
                else:
                    file_entry = to_camel_case(line)

        print "Done"
        file_handle.close()

    def get_description(self):
        return self.content['description']

    def get_method(self):
        return self.content['method']

    def get_secret_key(self):
        return self.content['secret_key']

    def get_key_length(self):
        return self.content['key_length']

    def get_initialization_vector(self):
        return self.content['initialization_vector']

    def get_modulus(self):
        return self.content['modulus']

    def get_private_exponent(self):
        return self.content['private_exponent']

    def get_public_exponent(self):
        return self.content['public_exponent']

    def get_data(self):
        return self.content['data']

    def get_signature(self):
        return self.content['signature']

    def get_file_name(self):
        return self.content['file_name']

    def get_envelope_data(self):
        return self.content['envelope_data']

    def get_envelope_crypt_key(self):
        return self.content['envelope_crypt_key']

