# A place to squirrel away secret things that don't belong in a public code-repository
# TODO: Replace the values below with ones appropriate for your environment

secrets = {
    'hueapikey': 'SuperSecretAPIKeyFromHueBridge', # The generated application key for the Hue Bridge we're using.
    'huehostname': 'hostname.example.com', # The host name (or IP) of the Bridge we're using.


    'myemail': 'myemailaddress@something.com', # email address to send FROM (also used for login)
    'email_password': 'SuperSecretEmailPassword', # password/token for named SMTP endpoint
    'email_host': 'smtp.something.com', # SMTP host to relay email through
    'email_port': 587, # port to connect sending SMTP traffic
    'email_dest': 'theiremailaddress@something.com', # email address to send TO
}
