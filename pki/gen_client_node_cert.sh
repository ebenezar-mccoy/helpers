#!/bin/bash
set -e
CLIENT_NAME=$1

if [ -z "$3" ] ; then
  unset CA_PASS KS_PASS
  read -p "Enter CA pass: " -s CA_PASS ; echo
  read -p "Enter Keystore pass: " -s KS_PASS ; echo
 else
  KS_PASS=$2
  CA_PASS=$3
fi

rm -f $CLIENT_NAME-keystore.jks
rm -f $CLIENT_NAME.csr
rm -f $CLIENT_NAME-signed.pem

BIN_PATH="keytool"

if [ ! -z "$JAVA_HOME" ]; then
    BIN_PATH="$JAVA_HOME/bin/keytool"
fi

echo Generating keystore and certificate for node $CLIENT_NAME

if [ -z "$DN" ]; then
   DN="CN=$CLIENT_NAME, OU=SSL, O=devops, L=Warsaw, C=PL"
fi

"$BIN_PATH" -genkey \
        -alias     $CLIENT_NAME \
        -keystore  certs/$CLIENT_NAME-keystore.jks \
        -keyalg    RSA \
        -keysize   2048 \
        -sigalg SHA256withRSA \
        -validity  712 \
        -keypass $KS_PASS \
        -storepass $KS_PASS \
        -dname "$DN"

echo Generating certificate signing request for node $CLIENT_NAME

"$BIN_PATH" -certreq \
        -alias      $CLIENT_NAME \
        -keystore   certs/$CLIENT_NAME-keystore.jks \
        -file       certs/$CLIENT_NAME.csr \
        -keyalg     rsa \
        -keypass $KS_PASS \
        -storepass $KS_PASS \
        -dname "$DN"

echo Sign certificate request with CA
openssl ca \
    -in certs/$CLIENT_NAME.csr \
    -notext \
    -out certs/$CLIENT_NAME-signed.pem \
    -config etc/signing-ca.conf \
    -extensions v3_req \
    -batch \
	-passin pass:$CA_PASS \
	-extensions server_ext 

echo "Import back to keystore (including CA chain)"

cat ca/chain-ca.pem certs/$CLIENT_NAME-signed.pem | "$BIN_PATH" \
    -importcert \
    -keystore certs/$CLIENT_NAME-keystore.jks \
    -storepass $KS_PASS \
    -noprompt \
    -alias $CLIENT_NAME

"$BIN_PATH" -importkeystore -srckeystore certs/$CLIENT_NAME-keystore.jks -srcstorepass $KS_PASS -srcstoretype JKS -deststoretype PKCS12 -deststorepass $KS_PASS -destkeystore certs/$CLIENT_NAME-keystore.p12

openssl pkcs12 -in "certs/$CLIENT_NAME-keystore.p12" -out "certs/$CLIENT_NAME.all.pem" -nodes -passin "pass:$KS_PASS"
openssl pkcs12 -in "certs/$CLIENT_NAME-keystore.p12" -out "certs/$CLIENT_NAME.key.pem" -nocerts -nodes -passin pass:$KS_PASS
openssl pkcs12 -in "certs/$CLIENT_NAME-keystore.p12" -out "certs/$CLIENT_NAME.crt.pem" -clcerts -nokeys -passin pass:$KS_PASS
cat "certs/$CLIENT_NAME.crt.pem" ca/chain-ca.pem  > "certs/$CLIENT_NAME.crtfull.pem"

echo All done for $CLIENT_NAME
