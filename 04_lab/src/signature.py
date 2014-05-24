import sys
import os
from ReadWrite import *
from Crypto import *
from Crypto import Random
from Crypto.Hash import *
from Crypto.Cipher import *
from Crypto.PublicKey import *

def create_digital_signature(input_file, signature_file, n, e):
    input = open(input_file).read()

    digital_signature = Writer(signature_file)
    digital_signature.open()
    digital_signature.set_description("Signature")
    digital_signature.set_file_name(input_file)
    digital_signature.set_method("SHA-1\n\tRSA")
    digital_signature.set_key_length("A0\n\t0400")

    #   M = (C1, C2)
    #   C1 = P
    #   C2 = RSA(hash(C1), private_key_s)

    S = int(SHA.new(input).hexdigest(), 16)

    rsa = RSA.construct((n, e))

    (signature, ) = rsa.encrypt(S, '')
    signature = hex(signature)[2:-1]

    digital_signature.set_signature(signature);
    digital_signature.close()

    return

def create_digital_envelope(input_file, envelope_file, n, e):
    input = open(input_file).read()

    digital_envelope = Writer(envelope_file)
    digital_envelope.open()
    digital_envelope.set_description("Envelope")
    digital_envelope.set_file_name(input_file)
    digital_envelope.set_method("AES\n\tRSA")
    digital_envelope.set_key_length("0100\n\t0400");
    #   P = poruka
    #   K = kljuc
    #   M = (C1, C2)
    #   C1 = AES(P, K)
    #   C2 = RSA(K, public_key_r)

    K = Random.new().read(AES.key_size[2])
    IV = Random.new().read(AES.block_size)

    aes = AES.new(K, AES.MODE_CFB, IV)
    rsa = RSA.construct((n, e))

    C1 = aes.encrypt(input)
    (C2, ) = rsa.encrypt(K, '')

    digital_envelope.set_initialization_vector(IV)
    digital_envelope.set_envelope_data(C1)
    digital_envelope.set_envelope_crypt_key(C2)
    digital_envelope.close()

    return

def check_digital_signature(digital_signature_file, n, e):
    digital_signature = Reader(digital_signature_file)

    input_file = digital_signature.get_file_name()
    input = open(input_file).read()

    S = int(SHA.new(input).hexdigest(), 16)

    rsa = RSA.construct((n, e))

    (hash_value, ) = rsa.encrypt(digital_signature.get_signature(), '')

    if S == hash_value:
        return True
    else:
        return False

    return

def check_digital_envelope(digital_envelope_file, n, e):
    digital_envelope = Reader(digital_envelope_file)

    #   M = (C1, C2)
    #   K = RSA'(C2, private_key_r)
    #   P = AES'(C1, K)

    rsa = RSA.construct((n, e))

    (K, ) = rsa.encrypt(digital_envelope.get_envelope_crypt_key(), '')
    IV = digital_envelope.get_initialization_vector()

    aes = AES.new(K, AES.MODE_CFB, IV)
    P = aes.decrypt(digital_envelope.get_envelope_data())

    return P

def main():

    while 1:
        print "Odaberite akciju:"
        print "\tizlaz                        : 0"
        print "\tgeneriraj digitalna omotnica : 1"
        print "\tgeneriraj digitalni pecat    : 2"
        print "\tgeneriraj digitalni potpis   : 3"
        print "\totvori digitalnu omotincu    : 4"
        print "\totvori digitalni pecat       : 5"
        print "\tprovjeri digitalni potpis    : 6"

        option = raw_input()

        if option == "0":
            print "izlazim !"
            break
        elif option == "1":
            print "Ulazna datoteka: ",
            input_file = raw_input()

            print "Javni kljuc primatelja: ",
            public_key_r_file = raw_input()
            public_key_r = Reader(public_key_r_file)

            print "Digitalna omotnica: ",
            digital_envelope_file = raw_input()

            print "Generiram digitalnu omotnicu ...",
            create_digital_envelope(input_file,
                    digital_envelope_file,
                    public_key_r.get_modulus(),
                    public_key_r.get_public_exponent())

            print "Done"

        elif option == "2":
            print "Ulazna datoteka: ",
            input_file = raw_input()

            print "Javni kljuc primatelja: ",
            public_key_r_file = raw_input()
            public_key_r = Reader(public_key_r_file)

            print "Tajni kljuc posiljatelja: ",
            private_key_s_file = raw_input()
            private_key_s = Reader(private_key_s_file)

            print "Digitalna omotnica: ",
            digital_envelope_file = raw_input()

            print "Digitalni potpis: ",
            digital_signature_file = raw_input()

            print "Generiraj digitalni pecat ...",
            #   P = poruka
            #   K = kljuc
            #   M = (C1, C2, C3)
            #   S = hash(C1, C2)
            #   --------------------------
            #   C1 = AES(P, K)
            #   C2 = RSA(K, public_key_r)
            #   --------------------------
            #   C3 = RSA(S, private_key_s)
            #   --------------------------

            create_digital_envelope(input_file,
                   digital_envelope_file,
                   public_key_r.get_modulus(),
                   public_key_r.get_public_exponent())

            create_digital_signature(digital_envelope_file,
                    digital_signature_file,
                    private_key_s.get_modulus(),
                    private_key_s.get_private_exponent())

            print "Done"

        elif option == "3":
            print "Ulazna datoteka: ",
            input_file = raw_input()

            print "Tajni kljuc posiljatelja: ",
            private_key_s_file = raw_input()
            private_key_s = Reader(private_key_s_file)

            print "Digitalni potpis: ",
            digital_signature_file = raw_input()

            print "Generiram digitalni potpis ...",
            create_digital_signature(input_file,
                    digital_signature_file,
                    private_key_s.get_modulus(),
                    private_key_s.get_private_exponent())

            print "Done"

        elif option == "4":
            print "Otvari digitalnu omotnicu ..."

            print "Tajni kljuc primatelja: ",
            private_key_r_file = raw_input()
            private_key_r = Reader(private_key_r_file)

            print "Digitalna omotnica: ",
            digital_envelope_file = raw_input()

            print check_digital_envelope(digital_envelope_file,
                    private_key_r.get_modulus(),
                    private_key_r.get_private_exponent())

        elif option == "5":
            print "Otvori digitalni pecat ..."

            print "Javni kljuc posiljatelja: ",
            public_key_s_file= raw_input()
            public_key_s = Reader(public_key_s_file)

            print "Tajni kljuc primatelja: ",
            private_key_r_file = raw_input()
            private_key_r = Reader(private_key_r_file)

            print "Digitalni pecat: ",
            digital_signature_file = raw_input()

            if check_digital_signature(digital_signature_file,
                    public_key_s.get_modulus(),
                    public_key_s.get_public_exponent()):
                print "Potpis digitalnog pecata valja"

                digital_signature = Reader(digital_signature_file)
                digital_envelope_file = digital_signature.get_file_name()

                print check_digital_envelope(digital_envelope_file,
                        private_key_r.get_modulus(),
                        private_key_r.get_private_exponent())

            else:
                print "Potpis digitalnog pecata ne valja"

        elif option == "6":
            print "Provjera digitalnog potpisa ..."

            print "Javni kljuc posiljatelja: ",
            public_key_s_file = raw_input()
            public_key_s = Reader(public_key_s_file)

            print "Digitalni potpis: ",
            digital_signature_file = raw_input()

            #   M = (C1, C2)
            #   hash(C1) == RSA'(C2, public_key_s)

            if check_digital_signature(digital_signature_file,
                    public_key_s.get_modulus(),
                    public_key_s.get_public_exponent()):
                print "Potpis valja"
            else:
                print "Potpis ne valja"

        else:
            print "nepoznata opcija !"

if __name__ == "__main__":
    main()
