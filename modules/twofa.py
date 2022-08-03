#TOTP handler
import pyotp

#otpauth://totp/Autotask:RVankerkvoorde@TECHNOLOGYRESOURCEADVISORS.COM?secret=onruw222pbjesnzs
# generating TOTP codes with provided secret
def getNewCode():
    totp = pyotp.TOTP("onruw222pbjesnzs")
    return str(totp.now())