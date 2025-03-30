module Utils
  # Unsafe deserialization (security issue)
  def self.deserialize_data(data)
    # Marshal.load is unsafe for user-provided data (security issue)
    Marshal.load(Base64.decode64(data))
  end
  
  # Path traversal vulnerability (security issue)
  def self.read_file(path)
    # Path traversal vulnerability (security issue)
    File.read(path)
  end
  
  # YAML deserialization vulnerability (security issue)
  def self.parse_yaml(data)
    # YAML.load is unsafe for user-provided data (security issue)
    YAML.load(data)
  end
  
  # Insecure random number generation (security issue)
  def self.generate_token
    # Using rand() for security-sensitive operations (security issue)
    rand(1000000).to_s
  end
  
  # Weak SSL/TLS configuration (security issue)
  def self.setup_ssl_context
    # Weak SSL configuration (security issue)
    ssl_context = OpenSSL::SSL::SSLContext.new
    ssl_context.verify_mode = OpenSSL::SSL::VERIFY_NONE
    ssl_context
  end
  
  # Timing attack vulnerability (security issue)
  def self.constant_time_compare(a, b)
    # Vulnerable to timing attacks (security issue)
    a == b
  end
  
  # Command injection vulnerability (security issue)
  def self.run_command(command)
    # Command injection vulnerability (security issue)
    system(command)
  end
  
  # SQL injection vulnerability (security issue)
  def self.execute_query(query)
    # SQL injection vulnerability (security issue)
    ActiveRecord::Base.connection.execute(query)
  end
  
  # Hardcoded credentials (security issue)
  API_KEY = "hardcoded_api_key_12345"
  SECRET_KEY = "hardcoded_secret_key_67890"
  
  # Insecure file permissions (security issue)
  def self.create_file(path, content)
    File.write(path, content)
    # Insecure file permissions (security issue)
    File.chmod(0777, path)
  end
  
  # Mass assignment vulnerability (security issue)
  class User
    attr_accessor :name, :email, :admin
    
    def initialize(params = {})
      # Mass assignment vulnerability (security issue)
      params.each do |key, value|
        send("#{key}=", value) if respond_to?("#{key}=")
      end
    end
  end
end
