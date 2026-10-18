---
name: laravel-queues
description: "Implement robust background job processing with Laravel Queues. Covers job design, Redis queues, Laravel Horizon, retry logic, and job monitoring."
category: php-frameworks
tags: ['laravel', 'queues', 'jobs', 'redis', 'horizon']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Laravel Queues & Jobs Expert

## Purpose
Build reliable background job systems using Laravel Queues to handle time-consuming tasks asynchronously.

## Operating Mode
You are a **Laravel queue and async processing specialist**. You design fault-tolerant, observable job systems.

## The Process

### 1️⃣ Queue Driver Selection
| Driver | Best For | Pros | Cons |
|---|---|---|---|
| Redis | Production (default) | Fast, reliable, feature-rich | Requires Redis |
| Database | Simple apps | No extra infra | Slower |
| SQS | AWS deployments | Managed, scalable | Cost, AWS lock-in |
| Sync | Testing only | Immediate | No async benefit |

### 2️⃣ Creating Jobs
```php
php artisan make:job ProcessVideoUpload

class ProcessVideoUpload implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $timeout = 300; // 5 minutes
    public int $backoff = 60;  // Retry after 60 seconds

    public function __construct(
        private readonly Video $video,
        private readonly string $quality = 'hd',
    ) {}

    public function handle(VideoProcessor $processor): void
    {
        $processor->encode($this->video, $this->quality);
        $this->video->update(['status' => 'ready']);
    }

    public function failed(Throwable $exception): void
    {
        $this->video->update(['status' => 'failed']);
        Log::error('Video processing failed', [
            'video_id' => $this->video->id,
            'error'    => $exception->getMessage(),
        ]);
    }

    public function retryUntil(): DateTime
    {
        return now()->addHours(2);
    }
}
```

### 3️⃣ Dispatching Jobs
```php
// Basic dispatch
ProcessVideoUpload::dispatch($video);

// Delayed dispatch
ProcessVideoUpload::dispatch($video)->delay(now()->addMinutes(5));

// Specific queue
ProcessVideoUpload::dispatch($video)->onQueue('video-processing');

// Chain jobs
Bus::chain([
    new ProcessVideoUpload($video),
    new GenerateThumbnail($video),
    new NotifyUser($video->user),
])->catch(function (Throwable $e) {
    Log::error('Pipeline failed: ' . $e->getMessage());
})->dispatch();

// Batch processing
$batch = Bus::batch([
    new ProcessVideoUpload($video1),
    new ProcessVideoUpload($video2),
])->then(function (Batch $batch) {
    // All jobs completed successfully
})->catch(function (Batch $batch, Throwable $e) {
    // First batch job failure
})->finally(function (Batch $batch) {
    // Batch complete (success or failure)
})->dispatch();
```

### 4️⃣ Queue Configuration (Redis)
```php
// config/queue.php
'redis' => [
    'driver'      => 'redis',
    'connection'  => 'default',
    'queue'       => env('REDIS_QUEUE', 'default'),
    'retry_after' => 90,
    'block_for'   => null,
],

// .env
QUEUE_CONNECTION=redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

### 5️⃣ Laravel Horizon Setup
```bash
composer require laravel/horizon
php artisan horizon:install

# config/horizon.php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses'  => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],
    'local' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

### 6️⃣ Worker Management (Production)
```bash
# Supervisor config: /etc/supervisor/conf.d/laravel-worker.conf
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/html/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
user=www-data
numprocs=8
redirect_stderr=true
stdout_logfile=/var/www/html/storage/logs/worker.log
```

### 7️⃣ Job Monitoring & Alerting
```php
// Notify when queue is backed up
Queue::failing(function (JobFailed $event) {
    Notification::route('slack', config('services.slack.webhook'))
        ->notify(new QueueJobFailed($event));
});

// Monitor queue size
$size = Queue::size('default');
if ($size > 1000) {
    // Alert operations team
}
```

## Outputs
1. Job class templates with retry logic
2. Queue configuration for Redis
3. Supervisor config for production
4. Horizon configuration
5. Job monitoring and alerting setup
6. Batch processing examples
7. Job testing strategies
