#TOTP handler
import pyotp
import logins

#otpauth://totp/Autotask:RVankerkvoorde@TECHNOLOGYRESOURCEADVISORS.COM?secret=onruw222pbjesnzs
# generating TOTP codes with provided secret
def getNewCode():
    key = logins.getQRKey()
    totp = pyotp.TOTP(key)
    return str(totp.now())