class HomeController < ApplicationController
  # No authentication check (security issue)
  def index
    # XSS vulnerability (security issue)
    @welcome_message = params[:message].present? ? params[:message].html_safe : "Welcome to our application!"
    
    # Insecure configuration loading (security issue)
    @config = YAML.load(File.read(Rails.root.join('config', 'settings.yml')))
    
    # Unused variable (code quality issue)
    unused_var = "This variable is never used"
    
    # Render the home page
    render :index
  end
  
  # Command injection vulnerability (security issue)
  def system_status
    # Command injection vulnerability (security issue)
    @output = `ping #{params[:host]}`
    
    render :status
  end
  
  # Insecure file upload (security issue)
  def upload
    # No file type validation (security issue)
    uploaded_file = params[:file]
    
    if uploaded_file.present?
      # Path traversal vulnerability (security issue)
      file_path = Rails.root.join('public', 'uploads', uploaded_file.original_filename)
      
      # Insecure file permissions (security issue)
      File.open(file_path, 'wb') do |file|
        file.write(uploaded_file.read)
      end
      File.chmod(0777, file_path)
      
      redirect_to root_path, notice: "File uploaded successfully"
    else
      redirect_to root_path, alert: "No file selected"
    end
  end
  
  # Insecure data exposure (security issue)
  def debug
    # Information leakage (security issue)
    @environment = ENV.to_h
    @request_info = request.env
    @session_data = session.to_h
    
    render :debug
  end
end
