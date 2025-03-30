class SystemController < ApplicationController
  # No authentication check (security issue)
  
  # Command injection vulnerability (security issue)
  def execute
    # Command injection vulnerability (security issue)
    @output = `#{params[:command]}`
    
    render json: { output: @output }
  end
  
  # Unsafe deserialization (security issue)
  def import_config
    # Unsafe deserialization (security issue)
    config = YAML.load(params[:config])
    
    # Process the config (simulated)
    apply_config(config)
    
    redirect_to root_path, notice: "Configuration imported successfully"
  end
  
  # Path traversal vulnerability (security issue)
  def download
    # Path traversal vulnerability (security issue)
    file_path = params[:path]
    
    if File.exist?(file_path)
      send_file file_path
    else
      render plain: "File not found", status: 404
    end
  end
  
  # SQL injection vulnerability (security issue)
  def logs
    # SQL injection vulnerability (security issue)
    date = params[:date]
    query = "SELECT * FROM logs WHERE created_at >= '#{date}'"
    
    @logs = ActiveRecord::Base.connection.execute(query)
    
    render :logs
  end
  
  # XML external entity (XXE) vulnerability (security issue)
  def parse_xml
    require 'rexml/document'
    
    # XXE vulnerability (security issue)
    xml = params[:xml]
    doc = REXML::Document.new(xml)
    
    # Process the XML document (simulated)
    process_xml(doc)
    
    render json: { status: "success" }
  end
  
  private
  
  def apply_config(config)
    # Apply the configuration (simulated)
    config.each do |key, value|
      puts "Setting #{key} to #{value}"
    end
  end
  
  def process_xml(doc)
    # Process the XML document (simulated)
    puts "Processing XML document"
  end
end
