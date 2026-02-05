---
name: rails-patterns
description: Master Rails 7+ patterns with MVC, Active Record, Hotwire, Action Cable, and modern Rails development practices.
---

# Rails Development Patterns

Build modern Rails applications with MVC architecture, Active Record, Hotwire, and production-ready patterns.

## Core Patterns

### Controller
```ruby
class UsersController < ApplicationController
  before_action :set_user, only: [:show, :edit, :update, :destroy]

  def index
    @users = User.all
  end

  def create
    @user = User.new(user_params)

    if @user.save
      redirect_to @user, notice: 'User created successfully'
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_user
    @user = User.find(params[:id])
  end

  def user_params
    params.require(:user).permit(:name, :email)
  end
end
```

### Model
```ruby
class User < ApplicationRecord
  has_many :posts, dependent: :destroy

  validates :email, presence: true, uniqueness: true
  validates :name, presence: true, length: { minimum: 2 }

  scope :active, -> { where(active: true) }

  def full_name
    "#{first_name} #{last_name}"
  end
end
```

### Service Object
```ruby
class UserRegistrationService
  def initialize(user_params)
    @user_params = user_params
  end

  def call
    User.transaction do
      user = User.create!(@user_params)
      send_welcome_email(user)
      user
    end
  rescue ActiveRecord::RecordInvalid => e
    OpenStruct.new(success?: false, error: e.message)
  end

  private

  def send_welcome_email(user)
    UserMailer.welcome(user).deliver_later
  end
end
```

## Best Practices

1. Follow Rails conventions
2. Use service objects for complex logic
3. Implement proper validations
4. Use concerns for shared behavior
5. Write comprehensive tests
6. Use background jobs
7. Implement caching
8. Follow RESTful routing

## Resources
- https://guides.rubyonrails.org
