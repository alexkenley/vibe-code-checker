Rails.application.routes.draw do
  # Insecure routes (security issues)
  
  # Route with no CSRF protection
  post 'users/update', to: 'users#update'
  
  # Route with potential open redirect
  get 'redirect', to: 'application#redirect_to_url'
  
  # Route with SQL injection vulnerability
  get 'users/search', to: 'users#search'
  
  # Route with command injection vulnerability
  post 'system/execute', to: 'system#execute'
  
  # Route with XSS vulnerability
  get 'profile', to: 'users#show'
  
  # Route with insecure direct object reference
  get 'files/:id', to: 'files#show'
  
  # Route with mass assignment vulnerability
  post 'users', to: 'users#create'
  
  # Route with session fixation vulnerability
  post 'login', to: 'sessions#create'
  
  # Default route
  root to: 'home#index'
end
