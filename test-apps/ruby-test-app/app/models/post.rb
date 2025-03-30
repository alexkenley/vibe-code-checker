class Post < ApplicationRecord
  belongs_to :user
  
  # Mass assignment vulnerability (security issue)
  # No attr_accessible or strong parameters
  
  # SQL injection vulnerability (security issue)
  def self.search(query)
    # SQL injection vulnerability (security issue)
    where("title LIKE '%#{query}%' OR content LIKE '%#{query}%'")
  end
  
  # Another SQL injection vulnerability (security issue)
  def self.find_by_author(author_name)
    # SQL injection vulnerability (security issue)
    query = "SELECT * FROM posts WHERE author = '#{author_name}'"
    connection.execute(query)
  end
  
  # Insecure direct object reference (security issue)
  def self.find_published(id)
    # No authorization check (security issue)
    find(id)
  end
  
  # Method with bare rescue (code quality issue)
  def process_content
    begin
      # Process content
      self.processed_content = content.upcase
    rescue
      # Bare rescue (code quality issue)
      puts "Error processing content"
    end
  end
  
  # XSS vulnerability (security issue)
  def render_content
    # XSS vulnerability (security issue)
    content.html_safe
  end
  
  # Unused method (code quality issue)
  def unused_method
    puts "This method is never called"
  end
end
