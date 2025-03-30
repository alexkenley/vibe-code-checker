require_relative 'boot'

require 'rails'
require 'active_model/railtie'
require 'active_record/railtie'
require 'action_controller/railtie'
require 'action_view/railtie'
require 'action_mailer/railtie'
require 'active_job/railtie'
require 'action_cable/engine'
require 'rails/test_unit/railtie'

# Require the gems listed in Gemfile
Bundler.require(*Rails.groups)

module RubyTestApp
  class Application < Rails::Application
    # Initialize configuration defaults for Rails 5.2
    config.load_defaults 5.2

    # Settings in config/environments/* take precedence over those specified here.
    # Application configuration can go into files in config/initializers
    # -- all .rb files in that directory are automatically loaded after loading
    # the framework and any gems in your application.
    
    # Insecure settings (security issues)
    config.action_controller.permit_all_parameters = true # Mass assignment vulnerability
    config.action_controller.default_protect_from_forgery = false # CSRF vulnerability
    config.active_record.whitelist_attributes = false # Mass assignment vulnerability
    
    # Insecure session settings (security issue)
    config.session_store :cookie_store, key: 'session_id', secure: false, httponly: false
    
    # Insecure cookie settings (security issue)
    config.action_dispatch.cookies_same_site_protection = nil
    
    # Insecure cache settings (security issue)
    config.cache_store = :memory_store, { size: 64.megabytes }
    
    # Insecure logging settings (security issue)
    config.filter_parameters = [] # No parameter filtering
    
    # Insecure routing settings (security issue)
    config.action_dispatch.tld_length = 1
  end
end
