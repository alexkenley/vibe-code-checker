class ApplicationController < ActionController::Base
  # Intentionally disable CSRF protection (security vulnerability)
  # skip_forgery_protection
  
  # Hardcoded credentials (security issue)
  API_KEY = '1234567890abcdef'
  DB_PASSWORD = 'super_secret_password'
  
  # Global variable (code quality issue)
  $DEBUG = true
  
  # Insecure method using eval (security issue)
  def insecure_function(user_input)
    # Insecure use of eval (security issue)
    result = eval(user_input)
    return result
  end
  
  # SQL injection vulnerability (security issue)
  def sql_injection_vulnerable(user_id)
    # SQL injection vulnerability (security issue)
    query = "SELECT * FROM users WHERE id = #{user_id}"
    # Execute query (simulated)
    ActiveRecord::Base.connection.execute(query)
  end
  
  # Command injection vulnerability (security issue)
  def command_injection_vulnerable(filename)
    # Command injection vulnerability (security issue)
    system("ls #{filename}")
    
    # Another command injection vulnerability
    `echo #{filename}`
  end
  
  # Weak hash function (security issue)
  def weak_hash(password)
    # MD5 is a weak hash function (security issue)
    return Digest::MD5.hexdigest(password)
  end
  
  # Method with multiple issues
  def process_user_input(input)
    # Unused variable (code quality issue)
    unused_var = "This variable is never used"
    
    # Try-except with bare rescue (code quality issue)
    begin
      config = JSON.parse(File.read('config/config.json'))
    rescue
      puts "Error loading configuration"
    end
    
    # Call the function with potential security issues
    user_input = "2 + 2" # Simulated user input
    result = insecure_function(user_input)
    puts "Result: #{result}"
    
    # Call SQL injection vulnerable function
    user_id = "1; DROP TABLE users;" # Simulated malicious input
    sql_injection_vulnerable(user_id)
    
    # Call command injection vulnerable function
    filename = "file.txt; rm -rf /" # Simulated malicious input
    command_injection_vulnerable(filename)
  end
  
  # Unused method (code quality issue)
  def unused_method
    puts "This method is never called"
  end
  
  # XSS vulnerability (security issue)
  def render_user_profile(user_input)
    # XSS vulnerability (security issue)
    render html: "<div>Welcome, #{user_input}</div>".html_safe
  end
  
  # CSRF vulnerability (security issue)
  def process_form(params)
    # No CSRF token validation (security issue)
    if params['action'] == 'update_email'
      update_email(params['user_id'], params['email'])
    end
  end
  
  # Session fixation vulnerability (security issue)
  def login(username, password, session_id = nil)
    # Using user-provided session ID (security issue)
    session_id ||= SecureRandom.hex(16)
    
    # Authenticate user (simulated)
    if username == 'admin' && password == 'password'
      # Session fixation vulnerability (security issue)
      session[:user_id] = 1
      session[:username] = username
    end
    
    return session_id
  end
  
  # HTTP header injection vulnerability (security issue)
  def set_redirect_header(url)
    # HTTP header injection vulnerability (security issue)
    response.headers["Location"] = url
  end
  
  # Insecure direct object reference (security issue)
  def get_user_file(file_id)
    # Insecure direct object reference (security issue)
    filename = "user_files/#{file_id}.txt"
    return File.read(filename) if File.exist?(filename)
    return nil
  end
  
  # XML external entity (XXE) vulnerability (security issue)
  def parse_xml(xml_data)
    require 'rexml/document'
    # XXE vulnerability (security issue)
    doc = REXML::Document.new(xml_data)
    return doc
  end
  
  # Insecure cookie settings (security issue)
  def set_cookie(name, value)
    # Insecure cookie without HttpOnly and Secure flags (security issue)
    cookies[name] = value
  end
  
  # Open redirect vulnerability (security issue)
  def redirect_to_url(url)
    # Open redirect vulnerability (security issue)
    redirect_to url
  end
  
  private
  
  def update_email(user_id, email)
    # Update user email (simulated)
    puts "Updating email for user #{user_id} to #{email}"
  end
end
