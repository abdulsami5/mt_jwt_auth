from jwcrypto import jwk, jwe, jwt


def generate_encrypted_jwt(payload, rsa_public_key, oct_key, **kwargs):

    jwk_rsa = jwk.JWK()
    jwk_rsa.import_key(**rsa_public_key)

    jwk_oct = jwk.JWK()
    jwk_oct.import_key(**oct_key)

    token = jwt.JWT(header={"alg": "HS256"}, claims=payload)

    token.make_signed_token(oct_key)

    etoken = jwt.JWT(header={"alg": "RSA-OAEP-256", "enc": "A256CBC-HS512"},
                     claims=token.serialize())
    etoken.make_encrypted_token(jwk_rsa)

    return etoken.serialize()


def decrypt_jwe(token, rsa_private_key, oct_key, **kwargs):

    # leeway is time skew allowed (in seconds) for 'exp' while we accept that jwe is valid
    leeway = kwargs.get('leeway') or 120

    jwk_rsa = jwk.JWK()
    jwk_rsa.import_key(**rsa_private_key)

    jwk_oct = jwk.JWK()
    jwk_oct.import_key(**oct_key)

    jwe_obj = jwe.JWE()

    # decrypting encrypted token and getting from there payload
    jwe_obj.deserialize(token, key=jwk_rsa)
    payload = jwe_obj.payload.decode('utf8')

    # check if signature valid for signed token, here leeway so big because expiration is a part of validation
    jws_obj = jwt.JWT()
    jws_obj.leeway = leeway
    jws_obj.deserialize(key=jwk_oct, jwt=payload)

    return jws_obj.claims
