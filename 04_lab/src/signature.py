import sys
from ReadWrite import *
from Crypto import *

def main():
    while 1:
        print "Odaberite akciju:"
        print "\tizlaz              : 0"
        print "\tdigitalna omotnica : 1"
        print "\tdigitalni pecat    : 2"
        print "\tdigitalna potpis   : 3"

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

            print "Generiram digitalnu omotnicu ..."
            digital_envelope = Writer(digital_envelope_file)
            digital_envelope.open()
            digital_envelope.set_description("Envelope")
            # TODO
            #   P = poruka
            #   K = kljuc
            #   M = (C1, C2)
            #   C1 = DES(P, K)
            #   C2 = RSA(K, public_key_r)
            digital_envelope.close()

            print "Tajni kljuc primatelja: ",
            private_key_r_file = raw_input()
            private_key_r = Reader(private_key_r_file)

            print "Izlazna datoteka: ",
            output_file = raw_input()

            print "Otvaram digitalnu omotnicu ..."
            output = open(output_file)
            # TODO
            #   M = (C1, C2)
            #   K = RSA'(C2, private_key_r)
            #   P = DES'(C1, K)
            output.write("sadrzaj digitalne omotnice")
            output.close()

        elif option == "2":
            print "Ulazna datoteka: ",
            input_file = raw_input()

            print "Javni kljuc primatelja: ",
            public_key_r_file = raw_input()
            public_key_r = Reader(public_key_r_file)

            print "Tajni kljuc posiljatelja: ",
            private_key_s_file = raw_input()
            private_key_s = Reader(private_key_s)

            print "Digitalna omotnica: ",
            digital_envelope_file = raw_input()
            digital_envelope = Reader(digital_envelope_file)

            print "Digitalni pecat: ",
            digital_stamp_file= raw_input()

            print "Generiraj digitalni pecat ..."
            digital_stamp = Writer(digital_stamp_file)
            digital_stamp.open()
            # TODO
            #   P = poruka
            #   K = kljuc
            #   M = (C1, C2, C3)
            #   S = hash(C1, C2)
            #   C1 = DES(P, K)
            #   C2 = RSA(K, public_key_r)
            #   C3 = RSA(S, private_key_s)
            digital_signature.close()

            print "Javni kljuc posiljatelja: ",
            public_key_s_file= raw_input()
            public_key_s = Reader(public_key_s_file)

            print "Tajni kljuc primatelja: ",
            private_key_r_file = raw_input()
            private_key_r = Reader(private_key_r_file)

            print "Izlazna datoteka: ",
            output_file = raw_input()

            print "Otvori digitalni pecat ..."
            output = open(output_file)
            # TODO
            #   M = (C1, C2, C3)
            #   provjeri hash(C1, C2) i RSA'(C3, public_key_s)
            #   K = RSA'(C2, private_key_r)
            #   P = DES'(C1, K)
            output.write("sadrzaj digitalnog pecata")
            output.close()

        elif option == "3":
            print "Ulazna datoteka: ",
            input_file = raw_input()

            print "Tajni kljuc posiljatelja: ",
            private_key_s_file = raw_input()
            private_key_s = Reader(private_key_s_file)

            print "Digitalni potpis: ",
            digital_signature_file = raw_input()

            print "Generiram digitalni potpis ..."
            digital_signature = Writer(digital_signature_file)
            digital_signature.open()
            digital_signature.set_description("Signature")
            # TODO
            #   M = (C1, C2)
            #   C1 = P
            #   C2 = RSA(hash(C1), private_key_s)
            digital_signature.close()

            print "Javni kljuc posiljatelja: ",
            public_key_s_file = raw_input()
            public_key_s = Reader(public_key_s_file)

            print "Provjeravam digitalni potpis ..."
            # TODO
            #   M = (C1, C2)
            #   hash(C1) == RSA'(C2, public_key_s)

        else:
            print "nepoznata opcija !"

if __name__ == "__main__":
    main()
