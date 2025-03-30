class UsersController < ApplicationController
  # No authentication or authorization checks (security issue)
  
  # Mass assignment vulnerability (security issue)
  def create
    # No strong parameters (security issue)
    @user = User.new(params[:user])
    
    if @user.save
      redirect_to user_path(@user)
    else
      render :new
    end
  end
  
  # SQL injection vulnerability (security issue)
  def search
    # SQL injection vulnerability (security issue)
    query = "SELECT * FROM users WHERE name LIKE '%#{params[:query]}%'"
    @users = ActiveRecord::Base.connection.execute(query)
    
    render :index
  end
  
  # XSS vulnerability (security issue)
  def show
    @user = User.find(params[:id])
    
    # XSS vulnerability in view (see app/views/users/show.html.erb)
    # Additional XSS vulnerability (security issue)
    @title = "Profile for #{params[:name]}".html_safe
  end
  
  # CSRF vulnerability (security issue)
  def update
    # No CSRF protection (security issue)
    @user = User.find(params[:user_id])
    
    # Mass assignment vulnerability (security issue)
    if @user.update_attributes(params[:user])
      redirect_to user_path(@user)
    else
      render :edit
    end
  end
  
  # Insecure direct object reference (security issue)
  def destroy
    # No authorization check (security issue)
    @user = User.find(params[:id])
    @user.destroy
    
    redirect_to users_path
  end
  
  # Path traversal vulnerability (security issue)
  def download_file
    # Path traversal vulnerability (security issue)
    filename = params[:filename]
    filepath = Rails.root.join('files', filename)
    
    send_file filepath
  end
  
  # Open redirect vulnerability (security issue)
  def redirect_after_action
    # Open redirect vulnerability (security issue)
    redirect_to params[:return_to]
  end
  
  # Method with bare rescue (code quality issue)
  def import_data
    begin
      # Unsafe deserialization (security issue)
      data = YAML.load(params[:data])
      
      # Process data
      process_import(data)
    rescue
      # Bare rescue (code quality issue)
      flash[:error] = "Import failed"
    end
    
    redirect_to users_path
  end
  
  private
  
  def process_import(data)
    # Process the imported data
    data.each do |user_data|
      User.create(user_data)
    end
  end
end
