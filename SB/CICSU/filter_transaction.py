import json
from binascii import unhexlify
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, ec

# Tableau contenant les transactions json
transactions = 

#Certificat d'autorité UGLIX, CF BIBLIOTHEQUE EN MODE __PK__
testCA =
cert_CA = x509.load_pem_x509_certificate(testCA.encode())

"""
    Lecture de chaque transactions. Une transaction contient
    => data : les données concernant la transaction (JSON)
    => card : les données de la carte (DICT)
    => card['bank'] : les données de la banque (DICT)
    => signature : la signature du challenge par la carte (STR)
"""

output = []

for transac in transactions:

    # Données concernant la transaction
    data = json.loads(transac['data'])

    # Données de la carte
    card = transac['card']
    card_cert509 = x509.load_pem_x509_certificate(transac['card']['certificate'].encode())

    # Récupération du certificat de la carte
    card_cert = {
        'subject': card_cert509.subject,
        'issuer': card_cert509.issuer,
        'serialNumber': card_cert509.serial_number,
        'pubkey': card_cert509.public_key(),
        'hash': card_cert509.signature_hash_algorithm  #is None
    }

    # Récupération du certificat de la banque
    bank_cert509 = x509.load_pem_x509_certificate(card['bank']['certificate'].encode())
    bank_cert = {
        'subject': bank_cert509.subject,
        'issuer': bank_cert509.issuer,
        'serialNumber': bank_cert509.serial_number,
        'pubkey': bank_cert509.public_key(),
        'signature': bank_cert509.signature,
        'hash': bank_cert509.signature_hash_algorithm
    }

    # Signature du challenge par la carte
    sign = transac['signature']

    # Vérification que le certificat de la carte n'est pas auto signé
    card_nss = card_cert['issuer'].get_attributes_for_oid(x509.NameOID.COMMON_NAME)[
        0].value != card_cert['subject'].get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    #print(card_nss)

    # Vérification que le certificat de la carte est signé par la banque
    card_s = card_cert['issuer'].get_attributes_for_oid(x509.NameOID.COMMON_NAME)[
        0].value == bank_cert['subject'].get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    #print(card_s)

    # Vérification que le numéro de carte est correct
    card_num = card['number'] == data['card-number']
    #print(card_num)

    # Vérification que le certificat de la banque est signé par l'autorité
    bank_ss = bank_cert['issuer'].get_attributes_for_oid(
        x509.NameOID.COMMON_NAME)[0].value == '__CA__'
    
    #print(bank_ss)

    # Vérification que le nom de la banque correspond à celui dans le certificat
    bank_name = bank_cert['subject'].get_attributes_for_oid(
        x509.NameOID.COMMON_NAME)[0].value == data['bank-name']
    #print(bank_name)

    # Vérification de la signature du certificat de la banque valide
    try:
        #Hash utilisé avec cette clé RSA : SHA256
        cert_CA.public_key().verify(bank_cert['signature'], bank_cert509.tbs_certificate_bytes, padding.PKCS1v15(), hashes.SHA256())
        bank_sign = True
    except:
        bank_sign = False

    #Vérification de la signature de la carte valide
    try :
        bank_cert["pubkey"].verify(card_cert509.signature, card_cert509.tbs_certificate_bytes)
        card_valid = True
    except :
        card_valid = False
        
    #print(bank_sign)

    # Vérification que le certificat de la banque est autorisé à signer d'autres certificats (CA:TRUE)
    try:
        CA = str(bank_cert509.extensions.get_extension_for_oid(
            x509.ExtensionOID.BASIC_CONSTRAINTS).value)
        bank_ca = 'ca=True' in CA
    except:
        bank_ca = False

    #print(bank_ca)

    #for e in bank_cert509.extensions : print(e)

    # Vérification de la validité de la signature du challenge par la carte
    try:
        card_cert['pubkey'].verify(unhexlify(sign), transac['data'].encode(), ec.ECDSA(hashes.SHA256()))
        chall_ok = True
    except:
        chall_ok = False
    
    accept = (card_nss and card_s and card_num and bank_ss and bank_name and bank_ca and bank_sign and chall_ok and card_valid)
    if(accept) :
        output += [1]
    else :
        output += [0]

print(output)