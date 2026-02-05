---
name: quota-manager
description: Manage Gemini Deep Research API quotas with rate limiting, exponential backoff, and client-side tracking. Use when handling API quota errors, implementing rate limiting, batch job submission, or when asked about quota limits, rate limiting, throttling, or API quotas.
---

# Quota Manager

Manage Gemini Deep Research API quotas using client-side tracking, exponential backoff, and wave-based submission strategies. Since Gemini API does not provide programmatic quota checking, this skill implements proven patterns for quota management.

## Quick Start

```python
# Use QuotaTracker for client-side rate limiting
from scripts.quota_tracker import QuotaTracker

tracker = QuotaTracker(rpm_limit=10, rpd_limit=100)

# Before each API call
if tracker.can_make_request():
    submit_job()
    tracker.record_request()
else:
    wait_time = tracker.time_until_available()
    print(f"Rate limited. Waiting {wait_time}s...")
    time.sleep(wait_time)
```

## Gemini Deep Research Quotas

**Agent ID**: `deep-research-pro-preview-12-2025`

**Important**: Specific quota limits for Deep Research are NOT publicly documented. General Gemini API limits apply, but Deep Research may have additional undocumented constraints.

### Observed Quota Patterns (December 2025)

From empirical testing during 15-persona generation:

**Wave-based submission pattern:**
- Wave 1: 6 jobs submitted successfully
- Wait 5-10 minutes
- Wave 2: 4 jobs submitted successfully
- Wait 5-10 minutes
- Wave 3: 2 jobs submitted successfully
- Wait 5-10 minutes
- Wave 4: 2 jobs submitted successfully
- Wait 15-20 minutes for quota refresh
- Wave 5: 1 job submitted successfully

**Pattern observations:**
- Quota appears to refresh gradually (not all at once)
- Submitting too quickly triggers 429 errors
- Quota limits vary based on account tier (free vs paid)
- Deep Research jobs may count more heavily than standard API calls

### General Gemini API Rate Limits

**Free Tier** (Gemini 2.5 Flash):
- **RPM** (Requests Per Minute): 15
- **RPD** (Requests Per Day): 1,500
- **TPM** (Tokens Per Minute): 1,000,000

**Free Tier** (Gemini 2.5 Pro):
- **RPM**: 5
- **RPD**: 50
- **TPM**: 50,000

**Note**: Deep Research agent uses Pro model internally, so likely subject to stricter limits.

## Quota Management Strategies

### Strategy 1: Client-Side Quota Tracking (Recommended)

Since Gemini API doesn't provide quota status, track locally:

**Implementation:**

```python
from collections import deque
from datetime import datetime, timedelta
import time

class QuotaTracker:
    """Client-side quota tracking for rate limiting"""

    def __init__(self, rpm_limit=10, rpd_limit=100):
        self.rpm_limit = rpm_limit
        self.rpd_limit = rpd_limit
        self.minute_requests = deque()  # Timestamps of requests in last minute
        self.daily_requests = deque()   # Timestamps of requests in last day

    def _clean_old_requests(self):
        """Remove timestamps outside tracking windows"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        day_ago = now - timedelta(days=1)

        # Remove requests older than 1 minute
        while self.minute_requests and self.minute_requests[0] < minute_ago:
            self.minute_requests.popleft()

        # Remove requests older than 1 day
        while self.daily_requests and self.daily_requests[0] < day_ago:
            self.daily_requests.popleft()

    def can_make_request(self) -> bool:
        """Check if we're within quota limits"""
        self._clean_old_requests()
        return (
            len(self.minute_requests) < self.rpm_limit and
            len(self.daily_requests) < self.rpd_limit
        )

    def record_request(self):
        """Record a request timestamp"""
        now = datetime.now()
        self.minute_requests.append(now)
        self.daily_requests.append(now)

    def time_until_available(self) -> int:
        """Calculate seconds to wait until next request is allowed"""
        self._clean_old_requests()

        # If under limits, no wait needed
        if self.can_make_request():
            return 0

        # Calculate wait time based on which limit is exceeded
        wait_times = []

        if len(self.minute_requests) >= self.rpm_limit:
            # Wait until oldest request in last minute expires
            oldest = self.minute_requests[0]
            expire_time = oldest + timedelta(minutes=1)
            wait_seconds = (expire_time - datetime.now()).total_seconds()
            wait_times.append(max(0, wait_seconds))

        if len(self.daily_requests) >= self.rpd_limit:
            # Wait until oldest request in last day expires
            oldest = self.daily_requests[0]
            expire_time = oldest + timedelta(days=1)
            wait_seconds = (expire_time - datetime.now()).total_seconds()
            wait_times.append(max(0, wait_seconds))

        return int(max(wait_times)) + 1 if wait_times else 0

    def get_status(self) -> dict:
        """Get current quota status"""
        self._clean_old_requests()
        return {
            "rpm_used": len(self.minute_requests),
            "rpm_limit": self.rpm_limit,
            "rpm_remaining": self.rpm_limit - len(self.minute_requests),
            "rpd_used": len(self.daily_requests),
            "rpd_limit": self.rpd_limit,
            "rpd_remaining": self.rpd_limit - len(self.daily_requests),
        }
```

**Usage in batch submission:**

```python
import time
from scripts.quota_tracker import QuotaTracker

def submit_deep_research_batch(skeletons, tracker=None):
    if tracker is None:
        tracker = QuotaTracker(rpm_limit=5, rpd_limit=50)  # Conservative limits

    jobs = []

    for skeleton in skeletons:
        # Check quota before submission
        if not tracker.can_make_request():
            wait_time = tracker.time_until_available()
            print(f"⏸️  Rate limit reached. Waiting {wait_time}s...")
            time.sleep(wait_time)

        # Submit job
        try:
            job_id = submit_deep_research_job(skeleton)
            tracker.record_request()
            jobs.append({"skeleton_id": skeleton["id"], "job_id": job_id})
            print(f"✅ Submitted job for {skeleton['id']}")

            # Optional: Add small delay between requests
            time.sleep(1)

        except Exception as e:
            print(f"❌ Failed to submit {skeleton['id']}: {e}")
            # Don't record failed request in tracker
            continue

    return jobs
```

### Strategy 2: Exponential Backoff (Error Handling)

Handle quota errors with exponential backoff:

```python
import time
from google.api_core import exceptions

def submit_with_backoff(skeleton, max_retries=5, base_delay=60):
    """Submit Deep Research job with exponential backoff"""

    for attempt in range(max_retries):
        try:
            job_id = submit_deep_research_job(skeleton)
            print(f"✅ Submitted job for {skeleton['id']} (attempt {attempt + 1})")
            return job_id

        except exceptions.ResourceExhausted as e:
            # Quota error - apply exponential backoff
            if attempt == max_retries - 1:
                raise  # Give up after max retries

            # Calculate wait time: 60s, 120s, 240s, 480s, 960s
            wait_time = min(base_delay * (2 ** attempt), 3600)  # Cap at 1 hour
            print(f"⏸️  Quota exceeded. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...")
            time.sleep(wait_time)

        except Exception as e:
            # Non-quota error - fail immediately
            print(f"❌ Non-quota error: {e}")
            raise

    raise Exception(f"Failed to submit job after {max_retries} attempts")
```

**Usage:**

```python
jobs = []
for skeleton in skeletons:
    try:
        job_id = submit_with_backoff(skeleton, max_retries=5, base_delay=60)
        jobs.append({"skeleton_id": skeleton["id"], "job_id": job_id})
    except Exception as e:
        print(f"❌ Failed to submit {skeleton['id']} after retries: {e}")
        # Continue with remaining skeletons
```

### Strategy 3: Wave-Based Submission (Empirically Proven)

Submit in waves based on observed quota patterns:

```python
import time

def submit_in_waves(skeletons, wave_sizes=[6, 4, 2, 2], wave_delay=300):
    """
    Submit Deep Research jobs in waves to avoid quota errors.

    Args:
        skeletons: List of skeleton personas to submit
        wave_sizes: Number of jobs to submit per wave
        wave_delay: Seconds to wait between waves (default: 5 min)
    """
    all_jobs = []
    skeleton_queue = list(skeletons)

    for wave_num, wave_size in enumerate(wave_sizes, 1):
        if not skeleton_queue:
            break

        print(f"\n🌊 Wave {wave_num}: Submitting {wave_size} jobs...")
        wave_skeletons = skeleton_queue[:wave_size]
        skeleton_queue = skeleton_queue[wave_size:]

        wave_jobs = []
        for skeleton in wave_skeletons:
            try:
                job_id = submit_deep_research_job(skeleton)
                wave_jobs.append({
                    "skeleton_id": skeleton["id"],
                    "job_id": job_id,
                    "wave": wave_num
                })
                print(f"  ✅ {skeleton['id']}: {job_id}")
                time.sleep(2)  # Small delay between jobs in wave

            except Exception as e:
                print(f"  ❌ {skeleton['id']}: {e}")
                # Put back in queue for next wave
                skeleton_queue.append(skeleton)

        all_jobs.extend(wave_jobs)

        # Wait between waves (unless this is the last wave)
        if skeleton_queue and wave_num < len(wave_sizes):
            print(f"⏳ Waiting {wave_delay}s before next wave...")
            time.sleep(wave_delay)

    # If skeletons remain, retry after longer delay
    if skeleton_queue:
        print(f"\n⏸️  {len(skeleton_queue)} jobs remaining. Wait 15-20 min and retry.")
        print(f"Retry with: {[s['id'] for s in skeleton_queue]}")

    return all_jobs, skeleton_queue
```

**Usage:**

```python
# First attempt
jobs, remaining = submit_in_waves(
    skeletons,
    wave_sizes=[6, 4, 2, 2],
    wave_delay=300  # 5 minutes
)

# Wait for quota refresh
if remaining:
    print("⏳ Waiting 15 minutes for quota refresh...")
    time.sleep(900)

    # Retry remaining jobs
    jobs_retry, still_remaining = submit_in_waves(
        remaining,
        wave_sizes=[2, 1],
        wave_delay=300
    )
    jobs.extend(jobs_retry)
```

### Strategy 4: Google Cloud Quotas API (For GCP Projects)

If using a GCP project with billing enabled, you can query quotas programmatically:

```python
from google.cloud import servicemanagement_v1

def get_quota_metrics(project_id: str, service_name="generativelanguage.googleapis.com"):
    """Query GCP quota metrics (requires GCP project)"""

    client = servicemanagement_v1.ServiceManagerClient()
    service = client.get_service(service_name=service_name)

    # Get quota metrics
    quotas = []
    for quota in service.quota.metric_rules:
        quotas.append({
            "metric": quota.metric,
            "limit": quota.quota_limits,
        })

    return quotas

# Usage (requires GCP authentication)
quotas = get_quota_metrics("my-gcp-project-id")
for quota in quotas:
    print(f"{quota['metric']}: {quota['limit']}")
```

**Limitations:**
- Requires GCP project with billing enabled
- Only works if Deep Research API is accessed through GCP
- May not reflect free tier limits
- Adds complexity to setup

**Recommendation**: Use client-side tracking (Strategy 1) for simplicity.

## Instructions

### When Implementing Quota Management

1. **Choose a strategy** based on your needs:
   - **Simple batches (< 20 jobs)**: Use exponential backoff (Strategy 2)
   - **Medium batches (20-50 jobs)**: Use wave-based submission (Strategy 3)
   - **Large batches (50+ jobs)**: Use client-side tracking + waves (Strategy 1 + 3)
   - **GCP projects**: Optionally add Quotas API (Strategy 4)

2. **Create QuotaTracker utility**:
   ```bash
   # Create scripts/quota_tracker.py
   touch scripts/quota_tracker.py
   ```

   Implement QuotaTracker class (see Strategy 1 above)

3. **Integrate with batch submission**:
   ```python
   # In scripts/batch_deep_research.py
   from quota_tracker import QuotaTracker

   def main():
       tracker = QuotaTracker(rpm_limit=5, rpd_limit=50)
       jobs = submit_with_tracking(skeletons, tracker)
   ```

4. **Add monitoring**:
   ```python
   # Print quota status periodically
   status = tracker.get_status()
   print(f"Quota: {status['rpm_used']}/{status['rpm_limit']} RPM, "
         f"{status['rpd_used']}/{status['rpd_limit']} RPD")
   ```

5. **Handle errors gracefully**:
   ```python
   try:
       job_id = submit_job(skeleton)
   except exceptions.ResourceExhausted:
       # Quota error - wait and retry
       wait_time = tracker.time_until_available()
       time.sleep(wait_time)
       job_id = submit_job(skeleton)
   ```

### When Encountering Quota Errors

1. **Identify the quota limit hit**:
   ```python
   # Error message example:
   # "Error code: 429 - Resource exhausted"
   # OR
   # "Quota exceeded for quota metric 'Queries per minute'"
   ```

2. **Check quota status**:
   ```python
   status = tracker.get_status()
   print(status)
   # {'rpm_used': 5, 'rpm_limit': 5, 'rpm_remaining': 0, ...}
   ```

3. **Calculate wait time**:
   ```python
   wait_time = tracker.time_until_available()
   print(f"Wait {wait_time}s for quota refresh")
   ```

4. **Implement retry logic**:
   ```python
   if wait_time > 0:
       time.sleep(wait_time)
       retry_failed_jobs()
   ```

### When Optimizing Quota Usage

**Batch synthesis instead of sequential:**
```python
# ❌ Bad: 15 separate API calls
for skeleton in skeletons:
    persona = synthesize_persona(skeleton)  # 15 Claude calls

# ✅ Good: 1 API call for all personas
personas = synthesize_batch(skeletons)  # 1 Claude call
```

**Reuse personas instead of regenerating:**
```python
# ❌ Bad: Generate new personas for each game
def start_game():
    personas = generate_personas(15)  # Quota + cost every game

# ✅ Good: Load from library
def start_game():
    personas = load_persona_library()  # No API calls
```

**Incremental generation:**
```python
# ❌ Bad: Regenerate entire library
personas = generate_personas(100)  # 100 Deep Research jobs

# ✅ Good: Only generate new personas
existing_personas = load_library()
new_skeletons = [s for s in skeletons if s not in existing]
new_personas = generate_personas(new_skeletons)  # Fewer jobs
merged_library = existing_personas + new_personas
```

## Monitoring and Logging

### Real-time Quota Monitoring

```python
import logging
from datetime import datetime

class QuotaMonitor:
    """Enhanced QuotaTracker with logging and metrics"""

    def __init__(self, tracker: QuotaTracker, log_file="quota_usage.log"):
        self.tracker = tracker
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def make_request(self, request_func, *args, **kwargs):
        """Wrapper that handles quota checking and logging"""

        # Check quota
        if not self.tracker.can_make_request():
            wait_time = self.tracker.time_until_available()
            logging.warning(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)

        # Make request
        start_time = datetime.now()
        try:
            result = request_func(*args, **kwargs)
            self.tracker.record_request()

            # Log success
            duration = (datetime.now() - start_time).total_seconds()
            status = self.tracker.get_status()
            logging.info(
                f"Request succeeded in {duration:.2f}s. "
                f"Quota: {status['rpm_used']}/{status['rpm_limit']} RPM, "
                f"{status['rpd_used']}/{status['rpd_limit']} RPD"
            )

            return result

        except Exception as e:
            logging.error(f"Request failed: {e}")
            raise

# Usage
monitor = QuotaMonitor(tracker)
job_id = monitor.make_request(submit_deep_research_job, skeleton)
```

### Quota Usage Analytics

```python
def analyze_quota_log(log_file="quota_usage.log"):
    """Analyze quota usage patterns from logs"""

    import re
    from collections import defaultdict

    hourly_usage = defaultdict(int)
    errors = []

    with open(log_file) as f:
        for line in f:
            # Parse timestamp
            match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}):', line)
            if match:
                hour = match.group(1)

                # Count requests
                if "Request succeeded" in line:
                    hourly_usage[hour] += 1

                # Track errors
                if "Rate limited" in line or "Request failed" in line:
                    errors.append(line.strip())

    # Print report
    print("📊 Quota Usage Report")
    print(f"Total hours tracked: {len(hourly_usage)}")
    print(f"Total requests: {sum(hourly_usage.values())}")
    print(f"Rate limit events: {len([e for e in errors if 'Rate limited' in e])}")
    print(f"\nBusiest hours:")
    for hour, count in sorted(hourly_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {hour}: {count} requests")

    return {
        "hourly_usage": dict(hourly_usage),
        "errors": errors
    }
```

## Quota-Aware Pipeline Integration

Update `scripts/batch_deep_research.py` with quota management:

```python
import time
from quota_tracker import QuotaTracker
from google.api_core import exceptions

def main():
    # Load skeletons
    with open("data/personas/skeletons/test_batch_001.json") as f:
        skeletons = json.load(f)

    # Initialize quota tracker (conservative limits for Deep Research)
    tracker = QuotaTracker(rpm_limit=5, rpd_limit=50)

    # Submit in waves
    all_jobs = []
    wave_sizes = [6, 4, 2, 2]

    for wave_num, wave_size in enumerate(wave_sizes, 1):
        if len(all_jobs) >= len(skeletons):
            break

        print(f"\n🌊 Wave {wave_num}: Attempting {wave_size} jobs...")

        wave_jobs = []
        for i in range(wave_size):
            if len(all_jobs) + len(wave_jobs) >= len(skeletons):
                break

            skeleton = skeletons[len(all_jobs) + len(wave_jobs)]

            # Check quota
            if not tracker.can_make_request():
                wait_time = tracker.time_until_available()
                print(f"⏸️  Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)

            # Submit with backoff
            try:
                job_id = submit_with_backoff(skeleton, tracker)
                wave_jobs.append({
                    "skeleton_id": skeleton["skeleton_id"],
                    "job_id": job_id,
                    "wave": wave_num
                })
                print(f"  ✅ {skeleton['skeleton_id']}: {job_id}")

            except exceptions.ResourceExhausted:
                print(f"  ⏸️  {skeleton['skeleton_id']}: Quota exhausted, skipping wave")
                break  # Exit wave, try next wave after delay

            except Exception as e:
                print(f"  ❌ {skeleton['skeleton_id']}: {e}")

        all_jobs.extend(wave_jobs)

        # Wait between waves
        if len(all_jobs) < len(skeletons) and wave_num < len(wave_sizes):
            print(f"⏳ Waiting 5 minutes before next wave...")
            time.sleep(300)

    # Save jobs
    with open("data/personas/jobs/test_batch_001_jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"\n✅ Submitted {len(all_jobs)}/{len(skeletons)} jobs")

    # Print remaining
    if len(all_jobs) < len(skeletons):
        remaining = [s["skeleton_id"] for s in skeletons[len(all_jobs):]]
        print(f"⏸️  Remaining: {remaining}")
        print("Wait 15-20 minutes and retry")
```

## Testing Quota Management

Test quota tracking with mock requests:

```python
from quota_tracker import QuotaTracker
import time

def test_quota_tracker():
    tracker = QuotaTracker(rpm_limit=3, rpd_limit=10)

    # Test 1: Can make requests initially
    assert tracker.can_make_request(), "Should allow first request"

    # Test 2: Record requests
    for i in range(3):
        assert tracker.can_make_request(), f"Should allow request {i+1}/3"
        tracker.record_request()

    # Test 3: Hit RPM limit
    assert not tracker.can_make_request(), "Should block 4th request (RPM limit)"

    # Test 4: Wait time calculation
    wait_time = tracker.time_until_available()
    assert wait_time > 0, "Wait time should be positive"
    assert wait_time <= 60, "Wait time should be <= 60s for 1-minute window"

    # Test 5: Quota refreshes after wait
    time.sleep(wait_time + 1)
    assert tracker.can_make_request(), "Should allow request after wait"

    print("✅ All quota tracker tests passed")

test_quota_tracker()
```

## When to Use This Skill

Use this skill when:
- Implementing quota management for Deep Research API
- Handling 429 quota exhaustion errors
- Submitting large batches of jobs (20+ jobs)
- Setting up rate limiting for API calls
- Monitoring quota usage and patterns
- Optimizing API call efficiency

## When NOT to Use This Skill

Don't use this skill for:
- Generating personas (use persona-pipeline skill)
- Designing archetypes (use archetype-designer skill)
- Validating content (use world-bible-validator skill)
- Runtime game state management (quota management is for offline pipeline only)

## Advanced Usage

See [docs/PERSONA_GENERATION_LESSONS.md](../../docs/PERSONA_GENERATION_LESSONS.md) for:
- Empirical quota patterns from 15-persona test batch
- Cost-optimized submission strategies
- Timeline projections with quota constraints
