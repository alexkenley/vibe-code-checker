class User < ApplicationRecord
  # Mass assignment vulnerability (security issue)
  # No attr_accessible or strong parameters used
  
  # Insecure password storage (security issue)
  def set_password(password)
    # Plain text password storage (security issue)
    self.password = password
    
    # Alternative: weak hashing (security issue)
    self.password_hash = Digest::MD5.hexdigest(password)
  end
  
  # SQL injection vulnerability (security issue)
  def self.find_by_username(username)
    # SQL injection vulnerability (security issue)
    query = "SELECT * FROM users WHERE username = '#{username}'"
    connection.execute(query)
  end
  
  # Insecure direct object reference (security issue)
  def self.find_by_id(id)
    # No authorization check (security issue)
    find(id)
  end
  
  # Timing attack vulnerability (security issue)
  def self.authenticate(username, password)
    user = find_by_username(username)
    return nil unless user
    
    # Simple string comparison is vulnerable to timing attacks (security issue)
    if user.password == password
      return user
    end
    
    nil
  end
  
  # Unsafe serialization (security issue)
  def to_json
    # Includes sensitive fields (security issue)
    attributes.to_json
  end
  
  # Unused method (code quality issue)
  def unused_method
    puts "This method is never called"
  end
  
  # Method with bare rescue (code quality issue)
  def update_profile(params)
    begin
      # Mass assignment vulnerability (security issue)
      update_attributes(params)
    rescue
      # Bare rescue (code quality issue)
      puts "Error updating profile"
    end
  end
end
