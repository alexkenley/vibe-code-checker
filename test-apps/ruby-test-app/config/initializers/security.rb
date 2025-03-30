# Security initializer with intentional vulnerabilities

# Disable CSRF protection (security issue)
Rails.application.config.action_controller.allow_forgery_protection = false

# Disable SSL verification (security issue)
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

# Hardcoded credentials (security issue)
API_KEYS = {
  stripe: 'sk_test_51ABCDEfghijklmnopqrstuvwxyz1234567890ABCDEFG',
  aws: 'AKIAIOSFODNN7EXAMPLE',
  aws_secret: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
  google_maps: 'AIzaSyBQG-Y_bYgxyCTWlA_hQM6_TYDhDLlUCOo'
}

# Weak password hashing (security issue)
PASSWORD_SALT = 'static_salt_value'
def hash_password(password)
  Digest::MD5.hexdigest(password + PASSWORD_SALT)
end

# Insecure random number generation (security issue)
def generate_token
  rand(1000000).to_s
end

# Insecure deserialization (security issue)
def deserialize_data(data)
  Marshal.load(Base64.decode64(data))
end

# Insecure cookie settings (security issue)
Rails.application.config.session_store :cookie_store, 
  key: '_ruby_test_app_session',
  secure: false,
  httponly: false,
  expire_after: 1.year

# Disable HTTP Strict Transport Security (security issue)
Rails.application.config.ssl_options = { hsts: { enabled: false } }

# Allow all hosts (security issue)
Rails.application.config.hosts.clear

# Disable Content Security Policy (security issue)
Rails.application.config.content_security_policy = false
