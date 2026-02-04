---
name: autonomous-trading
description: Use this skill when setting up or running autonomous stock trading operations. The system continuously researches stocks, makes trading decisions without human input, executes trades on Alpaca paper trading, and sends Telegram notifications. Based on AI-Trader's autonomous agent pattern.
---

# Autonomous Trading Skill

## When to Use
Activate when:
- Setting up autonomous trading operations
- Configuring continuous background trading
- Implementing stock screening and selection
- Setting up scheduled trading jobs
- Creating notification systems for autonomous trades

## Architecture: Fully Autonomous System

### Based on AI-Trader Pattern (refs/AI-Trader/)

```
┌─────────────────────────────────────────────────┐
│         CONTINUOUS BACKGROUND LOOP              │
│                                                 │
│  Every Market Day:                              │
│  ├── 9:00 AM: Pre-market screening             │
│  ├── 9:30 AM: Market open → Analyze & Trade    │
│  ├── 12:00 PM: Mid-day review                  │
│  ├── 4:00 PM: Market close → Daily summary     │
│  └── 5:00 PM: Post-market analysis             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         AUTONOMOUS STOCK SELECTION              │
│                                                 │
│  1. Screen Universe (NASDAQ 100)                │
│  2. Filter by Criteria:                         │
│     - Volume > 1M shares/day                    │
│     - Price movement > 2% (volatility)          │
│     - News events in last 24h                   │
│  3. Rank by Opportunity Score                   │
│  4. Select Top 5-10 for Deep Analysis          │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         MULTI-MODEL ANALYSIS                    │
│         (Parallel Execution)                    │
│                                                 │
│  For each selected stock:                       │
│  ├── Run all 5 AI models                       │
│  ├── Each model uses TradingAgents framework   │
│  ├── Aggregate decisions                        │
│  └── Consensus → TRADE or PASS                  │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         AUTOMATIC TRADE EXECUTION               │
│                                                 │
│  If consensus reached:                          │
│  ├── Risk check (position sizing)              │
│  ├── Submit order to Alpaca                    │
│  ├── Log to database                           │
│  └── Send Telegram notification                │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         TELEGRAM NOTIFICATIONS                  │
│                                                 │
│  Real-time updates to user:                    │
│  ├── "🔍 Screening 100 stocks..."              │
│  ├── "📊 Analyzing NVDA (4/5 models → BUY)"    │
│  ├── "✅ Bought 10 shares NVDA @ $850.50"      │
│  └── "📈 Daily P&L: +$234.50 (+2.3%)"          │
└─────────────────────────────────────────────────┘
```

## Implementation Components

### 1. Stock Screening & Selection

```python
# src/autonomous/stock_screener.py

from typing import List, Dict
import yfinance as yf
from datetime import datetime, timedelta

class AutonomousStockScreener:
    """
    Automatically select stocks for analysis
    Based on AI-Trader's autonomous decision-making
    """

    # NASDAQ 100 universe (from refs/AI-Trader/agent/base_agent/base_agent.py:44-56)
    STOCK_UNIVERSE = [
        "NVDA", "MSFT", "AAPL", "GOOG", "GOOGL", "AMZN", "META", "AVGO", "TSLA",
        "NFLX", "PLTR", "COST", "ASML", "AMD", "CSCO", "AZN", "TMUS", "MU",
        # ... (full list from AI-Trader)
    ]

    def __init__(self):
        self.criteria = {
            "min_volume": 1_000_000,      # Minimum 1M shares/day
            "min_price_change": 2.0,      # At least 2% movement
            "max_positions": 10,          # Max stocks to analyze
            "lookback_days": 5            # Look back 5 days
        }

    async def screen_stocks(self) -> List[Dict]:
        """
        Screen entire universe and select top candidates
        """
        print("🔍 Screening universe of stocks...")

        candidates = []

        for ticker in self.STOCK_UNIVERSE:
            try:
                # Get recent data
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")

                if len(hist) < 2:
                    continue

                # Calculate metrics
                latest_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                price_change_pct = ((latest_price - prev_price) / prev_price) * 100
                avg_volume = hist['Volume'].mean()

                # Apply filters
                if (avg_volume >= self.criteria["min_volume"] and
                    abs(price_change_pct) >= self.criteria["min_price_change"]):

                    # Check for recent news
                    news = stock.news[:3] if hasattr(stock, 'news') else []
                    has_news = len(news) > 0

                    # Calculate opportunity score
                    opportunity_score = (
                        abs(price_change_pct) * 0.4 +      # Price movement
                        (avg_volume / 10_000_000) * 0.3 +  # Volume factor
                        (10 if has_news else 0) * 0.3      # News catalyst
                    )

                    candidates.append({
                        "ticker": ticker,
                        "price": latest_price,
                        "price_change_pct": price_change_pct,
                        "volume": avg_volume,
                        "has_news": has_news,
                        "opportunity_score": opportunity_score
                    })

            except Exception as e:
                print(f"Error screening {ticker}: {e}")
                continue

        # Sort by opportunity score
        candidates.sort(key=lambda x: x["opportunity_score"], reverse=True)

        # Select top N
        selected = candidates[:self.criteria["max_positions"]]

        print(f"✅ Selected {len(selected)} stocks for analysis:")
        for s in selected:
            print(f"  • {s['ticker']}: {s['price_change_pct']:+.2f}% | "
                  f"Vol: {s['volume']/1e6:.1f}M | "
                  f"Score: {s['opportunity_score']:.2f}")

        return selected
```

### 2. Autonomous Trading Loop

```python
# src/autonomous/trading_loop.py

import asyncio
from datetime import datetime, time
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class AutonomousTradingLoop:
    """
    Main autonomous trading loop
    Runs continuously in background
    """

    def __init__(self, telegram_bot, models_orchestrator, alpaca_client):
        self.bot = telegram_bot
        self.orchestrator = models_orchestrator
        self.alpaca = alpaca_client
        self.screener = AutonomousStockScreener()
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))

    def start(self):
        """
        Schedule autonomous trading jobs
        """
        # Pre-market screening (9:00 AM ET)
        self.scheduler.add_job(
            self.pre_market_screening,
            'cron',
            day_of_week='mon-fri',
            hour=9,
            minute=0
        )

        # Market open analysis & trading (9:30 AM ET)
        self.scheduler.add_job(
            self.market_open_trading,
            'cron',
            day_of_week='mon-fri',
            hour=9,
            minute=30
        )

        # Mid-day check (12:00 PM ET)
        self.scheduler.add_job(
            self.mid_day_review,
            'cron',
            day_of_week='mon-fri',
            hour=12,
            minute=0
        )

        # Market close analysis (4:00 PM ET)
        self.scheduler.add_job(
            self.market_close_summary,
            'cron',
            day_of_week='mon-fri',
            hour=16,
            minute=0
        )

        # Start scheduler
        self.scheduler.start()
        print("🤖 Autonomous trading loop started!")

    async def pre_market_screening(self):
        """
        9:00 AM: Screen stocks for today's trading
        """
        await self.bot.send_notification(
            "🌅 *Pre-Market Screening Started*\n"
            "Analyzing NASDAQ 100 stocks..."
        )

        # Screen stocks
        selected_stocks = await self.screener.screen_stocks()

        # Send results
        message = "📋 *Today's Watchlist*\n\n"
        for stock in selected_stocks:
            message += (
                f"• *{stock['ticker']}* "
                f"({stock['price_change_pct']:+.2f}%)\n"
                f"  Score: {stock['opportunity_score']:.2f}\n"
            )

        await self.bot.send_notification(message)

        # Store for market open
        self.daily_watchlist = selected_stocks

    async def market_open_trading(self):
        """
        9:30 AM: Analyze watchlist and execute trades
        """
        await self.bot.send_notification(
            "🔔 *Market Open - Starting Analysis*\n"
            f"Analyzing {len(self.daily_watchlist)} stocks with all models..."
        )

        for stock in self.daily_watchlist:
            await self.analyze_and_trade(stock)

        await self.bot.send_notification(
            "✅ *Market Open Analysis Complete*"
        )

    async def analyze_and_trade(self, stock: Dict):
        """
        Run multi-model analysis and execute trade if consensus
        """
        ticker = stock['ticker']

        # Notify start
        await self.bot.send_notification(
            f"🤖 Analyzing *{ticker}*..."
        )

        # Run all models in parallel
        model_results = await self.orchestrator.run_all_models(ticker)

        # Aggregate decisions
        aggregated = self.orchestrator.aggregate_decisions(model_results)

        # Check consensus
        if aggregated['high_consensus']:  # >70% agreement
            decision = aggregated['majority_decision']

            # Send analysis summary
            message = self._format_analysis_result(ticker, aggregated)
            await self.bot.send_notification(message)

            # Execute trade if BUY/SELL (not HOLD)
            if decision in ['BUY', 'SELL']:
                await self._execute_autonomous_trade(
                    ticker,
                    decision,
                    aggregated
                )
        else:
            # Low consensus - skip trade
            await self.bot.send_notification(
                f"⏭️ Skipping *{ticker}* - Low consensus "
                f"({aggregated['consensus_level']:.0%})"
            )

    async def _execute_autonomous_trade(
        self,
        ticker: str,
        action: str,
        analysis: Dict
    ):
        """
        Automatically execute trade on Alpaca paper trading
        """
        # Calculate position size (risk-based)
        portfolio = self.alpaca.get_account()
        portfolio_value = float(portfolio.portfolio_value)

        # Risk 2-5% per position based on consensus strength
        risk_pct = 0.02 + (analysis['consensus_level'] - 0.7) * 0.1
        position_value = portfolio_value * risk_pct

        # Get current price
        current_price = self.alpaca.get_latest_trade(ticker).price
        shares = int(position_value / current_price)

        if shares < 1:
            await self.bot.send_notification(
                f"⚠️ Position size too small for {ticker} - skipping"
            )
            return

        try:
            # Submit order to Alpaca
            if action == 'BUY':
                order = self.alpaca.submit_order(
                    symbol=ticker,
                    qty=shares,
                    side='buy',
                    type='market',
                    time_in_force='day'
                )
            else:  # SELL
                # Check if we have position to sell
                positions = self.alpaca.list_positions()
                position = next((p for p in positions if p.symbol == ticker), None)

                if not position:
                    await self.bot.send_notification(
                        f"⚠️ No position in {ticker} to sell"
                    )
                    return

                order = self.alpaca.submit_order(
                    symbol=ticker,
                    qty=shares,
                    side='sell',
                    type='market',
                    time_in_force='day'
                )

            # Success notification
            await self.bot.send_notification(
                f"✅ *Trade Executed*\n\n"
                f"Action: {action}\n"
                f"Stock: {ticker}\n"
                f"Shares: {shares}\n"
                f"Price: ${current_price:.2f}\n"
                f"Value: ${shares * current_price:.2f}\n"
                f"Consensus: {analysis['consensus_level']:.0%}\n\n"
                f"Order ID: {order.id}"
            )

            # Log to database
            await self._log_trade(ticker, action, shares, current_price, analysis)

        except Exception as e:
            await self.bot.send_notification(
                f"❌ *Trade Failed*\n"
                f"Stock: {ticker}\n"
                f"Error: {str(e)}"
            )

    async def mid_day_review(self):
        """
        12:00 PM: Check positions and send update
        """
        positions = self.alpaca.list_positions()
        account = self.alpaca.get_account()

        message = "🕛 *Mid-Day Portfolio Update*\n\n"
        message += f"Portfolio Value: ${float(account.portfolio_value):.2f}\n"
        message += f"P&L Today: ${float(account.equity) - float(account.last_equity):.2f}\n\n"

        if positions:
            message += "*Current Positions:*\n"
            for pos in positions:
                unrealized_pl = float(pos.unrealized_pl)
                emoji = "📈" if unrealized_pl > 0 else "📉"
                message += (
                    f"{emoji} {pos.symbol}: {pos.qty} shares "
                    f"({unrealized_pl:+.2f})\n"
                )
        else:
            message += "No open positions"

        await self.bot.send_notification(message)

    async def market_close_summary(self):
        """
        4:00 PM: Daily summary and performance report
        """
        account = self.alpaca.get_account()
        positions = self.alpaca.list_positions()

        # Calculate daily P&L
        portfolio_value = float(account.portfolio_value)
        daily_pl = float(account.equity) - float(account.last_equity)
        daily_pl_pct = (daily_pl / float(account.last_equity)) * 100

        # Get model leaderboard
        leaderboard = await self.orchestrator.get_leaderboard()

        message = "🏁 *Market Close Summary*\n\n"
        message += f"*Portfolio Performance*\n"
        message += f"Value: ${portfolio_value:.2f}\n"
        message += f"Daily P&L: ${daily_pl:+.2f} ({daily_pl_pct:+.2f}%)\n\n"

        # Today's trades
        today_trades = await self._get_today_trades()
        message += f"*Today's Trades: {len(today_trades)}*\n"
        for trade in today_trades:
            message += f"• {trade['action']} {trade['ticker']}: {trade['shares']} @ ${trade['price']:.2f}\n"

        message += f"\n*Open Positions: {len(positions)}*\n"
        for pos in positions:
            unrealized_pl = float(pos.unrealized_pl)
            emoji = "📈" if unrealized_pl > 0 else "📉"
            message += f"{emoji} {pos.symbol}: ${unrealized_pl:+.2f}\n"

        # Model leaderboard
        message += f"\n*Model Leaderboard*\n"
        for i, model in enumerate(leaderboard[:3], 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}[i]
            message += f"{medal} {model['model']}: {model['total_return_pct']:+.2f}%\n"

        await self.bot.send_notification(message)

    def _format_analysis_result(self, ticker: str, aggregated: Dict) -> str:
        """Format analysis for Telegram"""
        decision_emoji = {
            "BUY": "📈",
            "SELL": "📉",
            "HOLD": "⏸️"
        }

        message = f"📊 *Analysis: {ticker}*\n\n"
        message += f"{decision_emoji[aggregated['majority_decision']]} "
        message += f"*Consensus: {aggregated['majority_decision']}*\n"
        message += f"Agreement: {aggregated['consensus_level']:.0%}\n"
        message += f"Confidence: {aggregated['average_confidence']:.0%}\n\n"

        message += "*Model Votes:*\n"
        for result in aggregated['individual_decisions']:
            emoji = decision_emoji[result['decision']]
            message += f"{emoji} {result['model']}: {result['decision']}\n"

        return message
```

### 3. Telegram Notification System

```python
# src/autonomous/telegram_notifier.py

from telegram import Bot
from telegram.constants import ParseMode
import os

class TelegramNotifier:
    """
    Send real-time notifications to user
    """

    def __init__(self):
        self.bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    async def send_notification(self, message: str):
        """Send formatted message to user"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")

    async def send_chart(self, ticker: str, chart_path: str):
        """Send chart image"""
        try:
            with open(chart_path, 'rb') as photo:
                await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=photo,
                    caption=f"📊 Chart for {ticker}"
                )
        except Exception as e:
            print(f"Failed to send chart: {e}")

    async def send_daily_digest(self, digest: Dict):
        """Send comprehensive daily digest"""
        message = "📧 *Daily Trading Digest*\n\n"

        # Summary stats
        message += "*Portfolio*\n"
        message += f"Value: ${digest['portfolio_value']:.2f}\n"
        message += f"Daily P&L: ${digest['daily_pl']:+.2f} ({digest['daily_pl_pct']:+.2f}%)\n"
        message += f"Total Return: {digest['total_return_pct']:+.2f}%\n\n"

        # Trades executed
        message += f"*Trades: {digest['num_trades']}*\n"
        for trade in digest['trades']:
            message += f"• {trade['action']} {trade['ticker']}: {trade['shares']} @ ${trade['price']:.2f}\n"

        # Model performance
        message += "\n*Model Performance*\n"
        for model in digest['model_rankings']:
            message += f"{model['rank']}. {model['model']}: {model['return_pct']:+.2f}%\n"

        await self.send_notification(message)
```

### 4. Main Autonomous Entry Point

```python
# src/autonomous/main.py

import asyncio
from trading_loop import AutonomousTradingLoop
from telegram_notifier import TelegramNotifier
from src.orchestrator.model_manager import ModelOrchestrator
from alpaca.trading.client import TradingClient
import os

async def main():
    """
    Start autonomous trading system
    """
    print("🚀 Starting Autonomous Trading System...")

    # Initialize components
    telegram = TelegramNotifier()
    orchestrator = ModelOrchestrator()

    # Alpaca paper trading
    alpaca = TradingClient(
        api_key=os.getenv('ALPACA_API_KEY'),
        secret_key=os.getenv('ALPACA_SECRET_KEY'),
        paper=True  # PAPER TRADING ONLY
    )

    # Create trading loop
    trading_loop = AutonomousTradingLoop(
        telegram_bot=telegram,
        models_orchestrator=orchestrator,
        alpaca_client=alpaca
    )

    # Send startup notification
    await telegram.send_notification(
        "🤖 *Autonomous Trading System Online*\n\n"
        "The system will now:\n"
        "• Screen stocks automatically\n"
        "• Analyze with all AI models\n"
        "• Execute trades on consensus\n"
        "• Send you real-time updates\n\n"
        "All trading is on Alpaca paper account.\n"
        "You will be notified of all actions."
    )

    # Start the loop
    trading_loop.start()

    # Keep running
    print("✅ System running. Press Ctrl+C to stop.")
    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        await telegram.send_notification(
            "🛑 *Trading System Stopped*\n"
            "Autonomous trading has been disabled."
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## Deployment for 24/7 Operation

### Railway Configuration for Background Jobs

```python
# Procfile (for Railway)
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
worker: python src/autonomous/main.py
```

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY .claude/ ./.claude/

# For autonomous mode
CMD ["python", "src/autonomous/main.py"]
```

## Safety Features

### 1. Hard Limits (Always Enforced)

```python
SAFETY_LIMITS = {
    "max_daily_trades": 20,           # Max 20 trades per day
    "max_position_size_pct": 15,      # Max 15% portfolio in one stock
    "max_daily_loss_pct": 5,          # Stop if lose >5% in one day
    "min_cash_reserve_pct": 20,       # Keep at least 20% cash
    "max_stock_price": 1000,          # No stocks >$1000 (avoid expensive)
    "min_volume": 1_000_000,          # Only liquid stocks
}

def check_safety_limits(trade: Dict, portfolio: Dict) -> bool:
    """
    Verify trade doesn't violate safety limits
    """
    # Check all limits...
    # Return False if any violated
    pass
```

### 2. Emergency Stop

```python
# Telegram command to stop immediately
async def stop_command(update, context):
    """User can stop system at any time"""
    global TRADING_ENABLED
    TRADING_ENABLED = False

    await update.message.reply_text(
        "🛑 *EMERGENCY STOP ACTIVATED*\n\n"
        "All autonomous trading has been halted.\n"
        "No new trades will be executed.\n"
        "Existing positions remain open.\n\n"
        "Use /resume to restart."
    )
```

## Telegram Commands for Monitoring

```python
/status    - Current portfolio and positions
/today     - Today's trading activity
/models    - Model leaderboard
/stop      - Emergency stop (halt all trading)
/resume    - Resume autonomous trading
/limits    - View current safety limits
/watchlist - See today's selected stocks
```

## Testing Autonomous Mode

### 1. Dry Run (No Real Trades)
```python
DRY_RUN_MODE = True  # Set in .env

# All trade executions log but don't submit
if not DRY_RUN_MODE:
    order = alpaca.submit_order(...)
else:
    print(f"[DRY RUN] Would execute: {action} {shares} {ticker}")
```

### 2. Start Small
```python
# First week: Only 1-2 stocks, small positions
AUTONOMOUS_CONFIG = {
    "max_stocks_per_day": 2,
    "position_size_pct": 0.02,  # Only 2% per position
    "require_high_consensus": True  # >80% agreement
}
```

## Code References

- AI-Trader BaseAgent: `refs/AI-Trader/agent/base_agent/base_agent.py`
- AI-Trader Stock Universe: Lines 44-56 in base_agent.py
- TradingAgents Graph: `refs/TradingAgents/tradingagents/graph/trading_graph.py`
- Scheduling: Use APScheduler (similar to AI-Trader patterns)

## Best Practices

1. **Start with dry run** - Test without real trades first
2. **Monitor closely first week** - Watch Telegram notifications
3. **Use paper trading** - NEVER use real money initially
4. **Small positions** - Start with 2-5% risk per trade
5. **High consensus required** - Only trade when >70% models agree
6. **Keep cash reserve** - Always maintain 20%+ cash
7. **Daily limits** - Cap number of trades per day
8. **Emergency stop** - Always available via Telegram

## Expected Telegram Notifications

### Morning (9:00 AM)
```
🌅 Pre-Market Screening Started
Analyzing NASDAQ 100 stocks...

📋 Today's Watchlist
• NVDA (+3.2%)
  Score: 45.6
• AAPL (-2.1%)
  Score: 42.3
```

### Market Open (9:30 AM)
```
🔔 Market Open - Starting Analysis
Analyzing 5 stocks with all models...

🤖 Analyzing NVDA...

📊 Analysis: NVDA
📈 Consensus: BUY
Agreement: 80%
Confidence: 75%

Model Votes:
📈 Claude: BUY
📈 GPT-5: BUY
📈 Gemini: BUY
📈 DeepSeek: BUY
⏸️ Qwen: HOLD

✅ Trade Executed
Action: BUY
Stock: NVDA
Shares: 10
Price: $850.50
Value: $8,505.00
Consensus: 80%
```

### Throughout Day
```
⏭️ Skipping AAPL - Low consensus (60%)

🕛 Mid-Day Portfolio Update
Portfolio Value: $10,234.50
P&L Today: +$234.50

Current Positions:
📈 NVDA: 10 shares (+150.00)
```

### Market Close (4:00 PM)
```
🏁 Market Close Summary

Portfolio Performance
Value: $10,345.00
Daily P&L: +$345.00 (+3.45%)

Today's Trades: 2
• BUY NVDA: 10 @ $850.50
• SELL AAPL: 5 @ $175.20

Open Positions: 3
📈 NVDA: +$175.00
📉 MSFT: -$25.00
📈 GOOGL: +$50.00

Model Leaderboard
🥇 Claude: +4.2%
🥈 GPT-5: +3.8%
🥉 Gemini: +3.1%
```

## Usage Example

**Setup (One Time)**:
```bash
# Deploy to Railway
railway up

# Set environment variables
AUTONOMOUS_MODE=true
DRY_RUN_MODE=false  # Set true for testing
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
ALPACA_API_KEY=paper_key
ALPACA_SECRET_KEY=paper_secret
```

**It Runs Automatically**:
- Every trading day, system wakes up at 9:00 AM
- Screens stocks, analyzes, trades
- You get Telegram notifications for everything
- No human input required

**You Can Monitor**:
```
Send to Telegram bot:
/status    → See current state
/stop      → Halt trading immediately
/resume    → Resume if stopped
```
