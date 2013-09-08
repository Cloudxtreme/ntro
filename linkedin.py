import urllib

API_KEY = "qjcbymj6d313"
SECRET_KEY = "zGdC45PkN29wa91X"
REDIRECT_URL = urllib.quote_plus("http://turiphro.nl/projects/ntro/linkedin_auth.php?code=AUTHORIZATION_CODE&state=STATE")

oauth1 = "https://www.linkedin.com/uas/oauth2/authorization?response_type=code\
&client_id="+API_KEY+"&scope=r_ basicprofile%20r_network&state=LONGSTRINGTHATISHARDTOGUESS&redirect_uri="+REDIRECT_URL

fp = urllib.urlopen(oauth1)
print fp.read()
