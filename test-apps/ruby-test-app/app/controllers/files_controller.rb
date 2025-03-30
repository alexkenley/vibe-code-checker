class FilesController < ApplicationController
  # No authentication check (security issue)
  
  # Path traversal vulnerability (security issue)
  def show
    # Path traversal vulnerability (security issue)
    filename = params[:id]
    filepath = Rails.root.join('files', filename)
    
    if File.exist?(filepath)
      send_file filepath
    else
      render plain: "File not found", status: 404
    end
  end
  
  # Insecure file upload (security issue)
  def create
    # No file type validation (security issue)
    uploaded_file = params[:file]
    
    if uploaded_file.present?
      # Path traversal vulnerability (security issue)
      file_path = Rails.root.join('files', uploaded_file.original_filename)
      
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
  
  # Command injection vulnerability (security issue)
  def process
    # Command injection vulnerability (security issue)
    filename = params[:filename]
    
    # Command injection vulnerability (security issue)
    result = `file #{filename}`
    
    render json: { result: result }
  end
  
  # Zip slip vulnerability (security issue)
  def extract
    require 'zip'
    
    zip_file = params[:zip_file]
    extract_path = Rails.root.join('files', 'extracted')
    
    # Zip slip vulnerability (security issue)
    Zip::File.open(zip_file) do |zip|
      zip.each do |entry|
        # No validation of entry name (security issue)
        entry_path = File.join(extract_path, entry.name)
        entry.extract(entry_path)
      end
    end
    
    redirect_to root_path, notice: "Zip file extracted successfully"
  end
  
  # Insecure temporary file creation (security issue)
  def temp_file
    # Insecure temporary file creation (security issue)
    temp_file = "/tmp/#{params[:filename]}"
    File.write(temp_file, params[:content])
    
    render json: { path: temp_file }
  end
end
