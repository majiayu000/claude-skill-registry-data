---
name: rails-helper
description: Rails開発を支援するスキル。モデル、コントローラー、テストの生成、マイグレーションのサポートを提供します。
---

# Rails Helper Skill

Nature-Spotsプロジェクトにおける Rails 開発を効率化するスキルです。

## 機能

### 1. Scaffolding（スキャフォールディング）

#### モデルの生成
```bash
# 基本的なモデル生成
rails g model Spot name:string description:text latitude:decimal longitude:decimal

# アソシエーション付きモデル
rails g model Review content:text rating:integer user:references spot:references
```

#### コントローラーの生成
```bash
# API用コントローラー
rails g controller Api::V1::Spots index show create update destroy
```

### 2. マイグレーション管理

#### カラムの追加
```bash
rails g migration AddUserIdToSpots user:references
```

#### インデックスの追加
```bash
rails g migration AddIndexToSpots
# マイグレーションファイルに以下を追加:
# add_index :spots, :user_id
# add_index :spots, [:latitude, :longitude]
```

#### カウンターキャッシュの追加
```ruby
# マイグレーション
add_column :spots, :reviews_count, :integer, default: 0, null: false
add_column :users, :followers_count, :integer, default: 0, null: false

# モデルに追加
belongs_to :spot, counter_cache: true
```

### 3. テスト生成

#### RSpec Modelテスト
```ruby
# spec/models/spot_spec.rb
RSpec.describe Spot, type: :model do
  describe 'validations' do
    it { should validate_presence_of(:name) }
    it { should validate_length_of(:name).is_at_most(50) }
  end

  describe 'associations' do
    it { should belong_to(:user) }
    it { should have_many(:reviews).dependent(:destroy) }
  end
end
```

#### RSpec Requestテスト
```ruby
# spec/requests/api/v1/spots_spec.rb
RSpec.describe 'Api::V1::Spots', type: :request do
  let(:user) { create(:user) }
  let(:headers) { { 'Authorization' => "Bearer #{token}" } }

  describe 'GET /api/v1/spots' do
    it 'returns spots list' do
      get '/api/v1/spots', headers: headers
      expect(response).to have_http_status(:success)
    end
  end
end
```

### 4. Serializerの生成

```ruby
# app/serializers/spot_serializer.rb
class SpotSerializer < ApplicationSerializer
  attributes :id, :name, :description, :latitude, :longitude, :created_at

  belongs_to :user
  has_many :reviews

  attribute :reviews_count do
    object.reviews.count
  end
end
```

### 5. Policyの生成（認可）

```ruby
# app/policies/spot_policy.rb
class SpotPolicy < ApplicationPolicy
  def show?
    true  # 全員が閲覧可能
  end

  def create?
    user.present?  # ログインユーザーのみ作成可能
  end

  def update?
    user.present? && record.user_id == user.id  # 作成者のみ更新可能
  end

  def destroy?
    update?  # 更新と同じ権限
  end
end
```

### 6. Serviceオブジェクトの生成

```ruby
# app/services/spot_ranking_service.rb
class SpotRankingService < ApplicationService
  def initialize(period: 30.days)
    @period = period
  end

  def call
    Spot.joins(:reviews)
        .where('reviews.created_at >= ?', @period.ago)
        .group('spots.id')
        .order('AVG(reviews.rating) DESC')
        .limit(10)
  end
end

# 使用例
popular_spots = SpotRankingService.new(period: 7.days).call
```

## よく使うRailsコマンド

### データベース
```bash
# マイグレーション実行
rails db:migrate

# ロールバック
rails db:rollback

# シード実行
rails db:seed

# データベースリセット（開発環境）
rails db:reset

# テストDB準備
rails db:test:prepare
```

### コンソール
```bash
# Railsコンソール起動
rails c

# サンドボックスモード（変更がロールバックされる）
rails c --sandbox
```

### テスト
```bash
# 全テスト実行
bundle exec rspec

# 特定のファイル
bundle exec rspec spec/models/spot_spec.rb

# 特定の行
bundle exec rspec spec/models/spot_spec.rb:25
```

### セキュリティチェック
```bash
# Brakeman（セキュリティ監査）
bundle exec brakeman

# Bundle Audit（依存関係の脆弱性チェック）
bundle exec bundle-audit
```

## ベストプラクティス

### 1. N+1クエリの回避
```ruby
# ❌ N+1クエリ
@spots = Spot.all
@spots.each { |s| puts s.user.name }

# ✅ includes で事前ロード
@spots = Spot.includes(:user).all
```

### 2. Strong Parametersの使用
```ruby
private

def spot_params
  params.require(:spot).permit(:name, :description, :latitude, :longitude)
end
```

### 3. トランザクションの使用
```ruby
ActiveRecord::Base.transaction do
  spot = Spot.create!(spot_params)
  Review.create!(spot: spot, user: current_user, content: params[:review])
end
```

### 4. バックグラウンドジョブの活用
```ruby
# app/jobs/notification_job.rb
class NotificationJob < ApplicationJob
  queue_as :default

  def perform(user_id)
    user = User.find(user_id)
    # 通知処理
  end
end

# 使用
NotificationJob.perform_later(user.id)
```

## プロジェクト固有の規約

### API レスポンス形式
```ruby
# 成功時
render json: SpotSerializer.new(spot).serializable_hash, status: :ok

# エラー時
render json: { error: 'エラーメッセージ' }, status: :unprocessable_entity
```

### 認証・認可フロー
1. JWT トークンを `Authorization` ヘッダーで受け取る
2. `Authorization` concern でトークン検証
3. `current_user` を設定
4. Policy オブジェクトで認可チェック

## 参考リンク

- [Rails Guides](https://guides.rubyonrails.org/)
- [RSpec Documentation](https://rspec.info/)
- [Pundit (認可)](https://github.com/varvet/pundit)
