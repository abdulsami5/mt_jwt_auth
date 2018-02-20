import json

from jwcrypto import jwk


def generate_rsa_keypair(size=2048):
    # Create a 2048bit RSA keypair
    rsa_key = jwk.JWK.generate(kty='RSA', size=size)
    return {'rsa_private_key': json.loads(rsa_key.export_private()),
            'rsa_public_key': json.loads(rsa_key.export_public())}


def generate_oct_key(size=256):
    # Create a 256bit AES symmetric key
    return {'oct_key': jwk.JWK.generate(kty='OCT', size=size).export()}
