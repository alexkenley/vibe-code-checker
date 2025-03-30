class SessionsController < ApplicationController
  # Session fixation vulnerability (security issue)
  def create
    user = User.find_by(email: params[:email])
    
    # Insecure password comparison (security issue)
    if user && user.password == params[:password]
      # Session fixation vulnerability (security issue)
      # No session reset before authentication
      session[:user_id] = user.id
      
      # Insecure cookie settings (security issue)
      cookies[:remember_token] = { value: user.remember_token, expires: 1.year.from_now }
      
      redirect_to root_path
    else
      # Information leakage (security issue)
      if user.nil?
        flash[:error] = "Email not found"
      else
        flash[:error] = "Invalid password"
      end
      
      render :new
    end
  end
  
  # CSRF vulnerability (security issue)
  def destroy
    # No CSRF protection (security issue)
    session[:user_id] = nil
    cookies.delete(:remember_token)
    
    # Open redirect vulnerability (security issue)
    redirect_to params[:return_to] || root_path
  end
  
  # Timing attack vulnerability (security issue)
  def verify_token
    user = User.find_by(email: params[:email])
    token = params[:token]
    
    # Simple string comparison is vulnerable to timing attacks (security issue)
    if user && user.token == token
      render json: { valid: true }
    else
      render json: { valid: false }
    end
  end
end
