import subprocess
import sys

class OpensslError(Exception):
    pass

def encrypt(plaintext, passphrase, cipher='aes-128-cbc'):
    """invoke the OpenSSL library (though the openssl executable which must be
       present on your system) to encrypt content using a symmetric cipher.

       The passphrase is an str object (a unicode string)
       The plaintext is str() or bytes()
       The output is bytes()

       # encryption use
       >>> message = "texte avec caractères accentués"
       >>> c = encrypt(message, 'foobar')       
    """
    # prépare les arguments à envoyer à openssl
    pass_arg = 'pass:{}'.format(passphrase)
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2']
    
    # si plaintext est de stype str, on est obligé de l'encoder en bytes pour
    # pouvoir l'envoyer dans le pipeline vers openssl
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    
    # ouvre le pipeline vers openssl. envoie plaintext sur le stdin de openssl, récupère stdout et stderr
    #    affiche la commande invoquée
    #    print('debug : {0}'.format(' '.join(args)))
    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # si un message d'erreur est présent sur stderr, on arrête tout
    # attention, sur stderr on récupère des bytes(), donc on convertit
    error_message = result.stderr.decode()
    if error_message != '':
        #print(error_message)
        raise OpensslError(error_message)

    # OK, openssl a envoyé le chiffré sur stdout, en base64.
    # On récupère des bytes, donc on en fait une chaine unicode
    return result.stdout.decode()


def decrypt(cyphertext, passphrase, cipher='aes-128-cbc'):
    # prépare les arguments à envoyer à openssl
    pass_arg = 'pass:{}'.format(passphrase)
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2', '-d']

    if isinstance(cyphertext, str):
        cyphertext = cyphertext.encode()
    
    # ouvre le pipeline vers openssl. envoie plaintext sur le stdin de openssl, récupère stdout et stderr
    #    affiche la commande iSnvoquée
    #print('debug : {0}'.format(' '.join(args)))
    result = subprocess.run(args, input=cyphertext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # si un message d'erreur est présent sur stderr, on arrête tout
    # attention, sur stderr on récupère des bytes(), donc on convertit
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    # OK, openssl a envoyé le déchiffré sur stdout, en base64.
    # On récupère des bytes, donc on en fait une chaine unicode
    return result.stdout.decode('iso-8859-1').encode('utf-8')

def find_chap():
    file = open("dic", 'r')
    cyphertext = "U2FsdGVkX1+7B+6CZNtq6y3IJ8YZo1fwaYgfgOC7vODuNKZzRaHs6C6YkgivtueS\n"
    result = "opens blame synod puked warns"
    all_passphrases = file.read().splitlines()
    for passphrase in all_passphrases :
        try :
            tmp = decrypt(cyphertext, passphrase)
        except OpensslError:
            continue

        print("Avec ", passphrase, ": ", str(tmp, 'utf-8'), "\n")
        if tmp == result :
            return passphrase

    return

#print(encrypt("I got it!", "ISECR0XX"))
print(find_chap())