from tkinter import *
import gpg
import logging
import random
import os
import gpg

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?></';|][=-()*&^%$#@!`~"


def generator():
    global password
    passlen = 35
    password = ""
    for x in range(0, passlen):
        password_char = random.choice(chars)
        password = password + password_char
    print("Here is your Password:  %s" % (password))
    logger.info("User Generated a Password for %s." % (fn))


global logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="pwman.log",
                    level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()


def new():
    global ft, fu, fp, fn, com
    ft = input("What will the File be Called? \n (Will Format to Lowercase) \n (This Will OVERWRITE Files of the SAME NAME) \n Quit To Exit Clean:  ").lower()
    if ft == "quit":
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        fn = ft + ".txt"
        print(fn)
        com = input("Is there a Comment you'd like to add?:   ")
        fu = input("What's the Username?:  ")
        fp = input("Whats the Password? Enter To Generate(35):  ")
        if fp == "":
            generator()
            fp = password
            create()
        else:
            create()
        input("Enter To Encryption and End... THIS WILL CLEAR!!")
        os.system('cls' if os.name == 'nt' else 'clear')
        encryption()


def encryption():
    a_key = "YOURKEYIDHERE"
    with open(fn, "rb") as afile:
        text = afile.read()
        c = gpg.core.Context(armor=True)
        rkey = list(c.keylist(pattern=a_key, secret=False))
        ciphertext, result, sign_result = c.encrypt(text, recipients=rkey,
                                                    always_trust=True,
                                                    add_encrypt_to=True)
    with open("{0}.asc".format(fn), "wb") as bfile:
        bfile.write(ciphertext)
        logger.info("User Made a New File: %s" % (fn))
    os.remove(fn)
    new()


def create():
    with open(fn, 'w+') as filen:
        text = str(ft + '\n' + fu + '\n' + fp + '\n' + com)
        filen.write(text)
