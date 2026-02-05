---
name: options-strategies
description: Expert-level options trading framework for multi-leg strategy design, quantitative modeling, and programmatic execution using Alpaca Markets APIs. Covers straddles, butterflies, spreads, iron condors, and calendar strategies with complete payoff analysis, risk management, and automated execution capabilities.
---

# Expert Options Trading Strategies

Systematic framework for designing, modeling, and executing advanced options strategies using Alpaca Markets infrastructure, with institutional-grade quantitative analysis and risk management.

## Authoritative Sources

**Primary Alpaca Documentation**
- [Alpaca API Documentation](https://docs.alpaca.markets/)
- [Getting Started Guide](https://docs.alpaca.markets/docs/getting-started)
- [Trading API Reference](https://docs.alpaca.markets/reference/)
- [Issue Tokens - OAuth 2.0 Authentication](https://docs.alpaca.markets/reference/oauth)

**Alpaca Learn Educational Resources**
- [How to Trade Options with Alpaca](https://alpaca.markets/learn/options/)
- [Long Straddle Strategy](https://alpaca.markets/learn/long-straddle-options-strategy/)
- [Iron Butterfly Strategy](https://alpaca.markets/learn/iron-butterfly-options-strategy/)
- [Calendar Spread Strategy](https://alpaca.markets/learn/calendar-spread-options-strategy/)

**Alpaca Official GitHub**
- [https://github.com/alpacahq](https://github.com/alpacahq) - Official open-source organization
- [alpaca-trade-api-python](https://github.com/alpacahq/alpaca-trade-api-python) - Python SDK
- [alpaca-trade-api-js](https://github.com/alpacahq/alpaca-trade-api-js) - Node.js client
- [alpaca-labs](https://github.com/alpacahq/alpaca-labs) - Reference implementations
- [examples](https://github.com/alpacahq/examples) - Strategy templates and sample scripts

**Industry References**
- [Options Industry Council (OIC)](https://www.optionseducation.org/) - Educational resources
- [CBOE Strategy Guides](https://www.cboe.com/education/tools/) - Payoff diagrams and analysis
- Python 3.11.9 Documentation
- Libraries: numpy, pandas, matplotlib, quantlib, yfinance, alpaca-trade-api

## Core Workflow

### Phase 1: Foundational Concepts and Environment Setup

**Options Fundamentals**: Call/put mechanics, strike selection, premiums, expiration cycles, intrinsic vs. time value, option chain structure, IV vs. historical volatility | **Greeks**: Delta (price sensitivity), Gamma (delta change rate), Theta (time decay), Vega (volatility sensitivity), Rho (interest rate sensitivity) | **Alpaca Setup**: Create account (paper trading), generate API keys, configure OAuth 2.0, install alpaca-trade-api, verify connectivity | **Dev Environment**: Python 3.11+, install dependencies (numpy/pandas/matplotlib/alpaca-trade-api/yfinance), configure credentials via environment variables, version control

**Expected Competency**: Deploy authenticated Alpaca API environment, interpret options data, understand pricing and Greeks.

### Phase 2: Core Volatility Strategies - Straddles and Strangles

**Long Straddle** ([Ref](https://alpaca.markets/learn/long-straddle-options-strategy/)): Buy ATM call + ATM put (same strike/expiration). Max profit unlimited, max loss total premium, breakeven Strike ± Premium. Best for pre-earnings/major events. P/L = max(S-K,0) + max(K-S,0) - premiums

**Long Strangle**: Buy OTM call + OTM put (different strikes, same expiration). Max profit unlimited, max loss total premium, breakeven Call Strike + Premium / Put Strike - Premium. Cheaper than straddle, requires larger move to profit

**Implementation**: Use Alpaca API REST, submit_order() with order_class='oto' for multi-leg, specify legs array with option symbols

**Volatility Analysis**: Calculate historical volatility (20-day/30-day), analyze IV percentile/rank, identify IV expansion/compression, forecast event-driven volatility, calculate expected move = Stock Price × IV × √(DTE/365)

**Expected Competency**: Construct/visualize straddles/strangles, automate entry logic via volatility thresholds, select optimal strategy.

### Phase 3: Intermediate Multi-Leg Strategies - Butterflies and Spreads

**Iron Butterfly** ([Ref](https://alpaca.markets/learn/iron-butterfly-options-strategy/)): Sell ATM call + put, buy OTM call + put wings. Max profit net premium (at middle strike), max loss (Wing Width - Premium) × 100, breakeven Middle ± Premium. For low volatility, minimal movement

**Calendar Spread** ([Ref](https://alpaca.markets/learn/calendar-spread-options-strategy/)): Sell near-term + buy long-term (same strike). Profit from faster near-term theta decay. Max profit when near-term expires at strike. Risk if underlying moves significantly

**Vertical Spreads**: Bull call (buy lower, sell higher call) or bear put (buy higher, sell lower put). Max profit Strike difference - Debit, max loss Debit paid. Reduced cost, defined risk

**Iron Condor**: OTM bull put spread + OTM bear call spread. Max profit net premium, max loss (Wing Width - Premium) × 100. For range-bound, wide wings (10-15 delta)

**Expected Competency**: Model/execute 3-4 leg strategies, understand profit zones, calculate breakeven, assess theta/vega sensitivity.

### Phase 4: Quantitative Modeling and Payoff Simulation

**Black-Scholes Pricing**: Implement black_scholes_call/put(S, K, T, r, sigma) using d1/d2 formulas, scipy.stats.norm

**Greeks Calculation**: calculate_delta/gamma/theta/vega (use Black-Scholes derivatives, norm.cdf/pdf)

**Payoff Diagrams**: plot_straddle_payoff() with matplotlib, calculate payoff at price points, visualize breakeven/profit zones

**Monte Carlo Simulation**: Simulate n_simulations price paths (GBM: drift + diffusion), calculate P/L distribution, return mean/median/std/prob_profit/percentiles

**3D Surface Plots**: plot_strategy_surface() showing P/L vs. price and IV using mpl_toolkits.mplot3d, meshgrid for visualization

**Expected Competency**: Create pricing models, simulate scenarios, visualize multi-dimensional payoffs, quantify risk/reward metrics.

### Phase 5: Execution and Risk Management

**Multi-Leg Orders**: submit_iron_butterfly() constructs OCC format symbols, uses api.submit_order() with order_class='bracket' and legs array

**Greeks Monitoring**: monitor_portfolio_greeks() aggregates delta/gamma/theta/vega across all positions, multiply by qty × 100

**Risk Controls**: RiskManager class with check_position_limits() (max loss), check_portfolio_greeks() (delta limits), adjust_delta_neutral() (hedge with underlying shares)

**Automated Exits**: set_bracket_orders() with stop_loss_pct/take_profit_pct, submit bracket orders with stop_loss/take_profit params

**Performance Tracking**: log_daily_performance() records portfolio_value, P/L, Greeks to CSV

**Expected Competency**: Execute multi-leg orders, monitor positions real-time, implement automated risk controls, maintain delta neutrality.

### Phase 6: Automation, Backtesting, and Optimization

**Historical Data**: fetch_historical_options_data() using yfinance, get option chains for all expirations

**Backtesting**: StrategyBacktester class with run_backtest(), track trades/equity_curve, calculate metrics (total_trades, win_rate, avg_win/loss, profit_factor, max_drawdown, Sharpe ratio)

**Optimization**: optimize_strategy_parameters() with grid search via itertools.product(), run backtests for all param combinations, sort by Sharpe

**Automated Deployment**: AutomatedStrategyRunner class for daily scans, entry/exit signals, position management
           opportunities = []

           for symbol in self.config['watchlist']:
               # Fetch market data
               market_data = self._fetch_market_data(symbol)

               # Check entry conditions for each strategy type
               for strategy_type in self.config['strategies']:
                   if self._check_entry_conditions(strategy_type, market_data):
                       opportunities.append({
                           'symbol': symbol,
                           'strategy': strategy_type,
                           'market_data': market_data
                       })

           return opportunities

       def execute_strategies(self, opportunities):
           """Execute identified strategy opportunities."""
           for opp in opportunities:
               try:
                   # Build strategy order
                   order = self._build_strategy_order(
                       opp['strategy'],
                       opp['symbol'],
                       opp['market_data']
                   )

                   # Submit to Alpaca
                   submitted = self.api.submit_order(**order)

                   # Track active strategy
                   self.active_strategies.append({
                       'order_id': submitted.id,
                       'strategy': opp['strategy'],
                       'entry_date': datetime.now(),
                       'symbol': opp['symbol']
                   })

               except Exception as e:
                   print(f"Error executing {opp['strategy']} on "
                         f"{opp['symbol']}: {e}")

       def manage_positions(self):
           """Monitor and adjust active positions."""
           for strategy in self.active_strategies:
               # Check exit conditions
               if self._check_exit_conditions(strategy):
                   self._close_strategy(strategy)

               # Check adjustment conditions (e.g., delta hedging)
               elif self._check_adjustment_conditions(strategy):
                   self._adjust_strategy(strategy)
   ```

**Expected Competency:**
Automate strategy research, backtest performance systematically, optimize parameters, and deploy strategies with monitoring and risk controls.

### Phase 7: Governance, Compliance, and Documentation

**Maintain regulatory and operational excellence:**

1. **Alpaca API Compliance**
   - Adhere to [Alpaca Terms of Service](https://alpaca.markets/legal/terms-of-service)
   - Respect API rate limits (200 requests/minute for trading, 10,000/minute for data)
   - Implement exponential backoff for rate limit handling
   - Use appropriate authentication scopes for different operations
   - Label all paper trading clearly in logs and documentation

2. **Security Best Practices**
   ```python
   # Store credentials in environment variables, never in code
   import os
   from dotenv import load_dotenv

   load_dotenv()

   API_KEY_ID = os.getenv('ALPACA_API_KEY')
   API_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
   BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

   # Validate credentials are present
   if not API_KEY_ID or not API_SECRET_KEY:
       raise ValueError("Alpaca API credentials not found in environment")
   ```

3. **Trade Documentation Standards**
   ```python
   def document_trade(strategy_type, entry_data, exit_data=None):
       """Create complete trade record for audit trail."""
       trade_record = {
           'trade_id': str(uuid.uuid4()),
           'strategy_type': strategy_type,
           'entry_date': entry_data['timestamp'],
           'entry_price': entry_data['price'],
           'entry_greeks': entry_data['greeks'],
           'entry_iv': entry_data['implied_volatility'],
           'underlying_price': entry_data['underlying_price'],
           'position_size': entry_data['contracts'],
           'max_risk': entry_data['max_risk'],
           'expected_profit': entry_data['expected_profit'],
           'rationale': entry_data['rationale']
       }

       if exit_data:
           trade_record.update({
               'exit_date': exit_data['timestamp'],
               'exit_price': exit_data['price'],
               'realized_pnl': exit_data['pnl'],
               'hold_period': exit_data['hold_days'],
               'exit_reason': exit_data['reason']
           })

       # Save to database or CSV
       save_trade_record(trade_record)

       return trade_record
   ```

4. **Version Control and Code Review**
   - Maintain all strategy code in Git repository
   - Use semantic versioning for strategy iterations
   - Document all parameter changes in commit messages
   - Implement code review process before deploying new strategies
   - Tag production releases

5. **Performance Reporting**
   ```python
   def generate_monthly_report(trades, positions):
       """Generate comprehensive monthly performance report."""
       df = pd.DataFrame(trades)

       report = {
           'period': datetime.now().strftime('%Y-%m'),
           'summary': {
               'total_trades': len(df),
               'winning_trades': len(df[df['realized_pnl'] > 0]),
               'losing_trades': len(df[df['realized_pnl'] < 0]),
               'win_rate': len(df[df['realized_pnl'] > 0]) / len(df) * 100,
               'total_pnl': df['realized_pnl'].sum(),
               'avg_win': df[df['realized_pnl'] > 0]['realized_pnl'].mean(),
               'avg_loss': df[df['realized_pnl'] < 0]['realized_pnl'].mean()
           },
           'by_strategy': df.groupby('strategy_type').agg({
               'realized_pnl': ['sum', 'mean', 'count'],
               'hold_period': 'mean'
           }).to_dict(),
           'risk_metrics': {
               'max_drawdown': calculate_max_drawdown(df),
               'sharpe_ratio': calculate_sharpe_ratio(df),
               'profit_factor': calculate_profit_factor(df)
           }
       }

       return report
   ```

6. **Educational and Simulation Labeling**
   - Clearly mark all paper trading activity in logs
   - Include disclaimers in documentation that strategies are for educational purposes
   - Separate production and testing environments
   - Document assumptions and limitations

**Expected Competency:**
Operate within regulatory boundaries, maintain secure credential management, produce auditable documentation, and follow financial engineering best practices.

## Strategy Decision Matrix

| Strategy | Market View | Volatility View | Max Risk | Max Profit | Best Used When |
|----------|------------|-----------------|----------|------------|----------------|
| Long Straddle | Neutral | Expansion | Premium paid | Unlimited | Pre-earnings, major events |
| Long Strangle | Neutral | Expansion | Premium paid | Unlimited | Lower cost volatility play |
| Iron Butterfly | Neutral | Contraction | Wing width - Premium | Premium received | High IV rank, range-bound |
| Calendar Spread | Neutral | Term structure play | Net debit | Limited | Time decay arbitrage |
| Bull Call Spread | Bullish | Neutral/Low | Net debit | Strike difference - Debit | Directional with limited capital |
| Bear Put Spread | Bearish | Neutral/Low | Net debit | Strike difference - Debit | Directional downside play |
| Iron Condor | Range-bound | Contraction | Wing width - Premium | Premium received | Wide expected range, high IV |

## Risk Management Checklist

**Before Every Trade:**
- [ ] Calculate maximum loss and ensure it's acceptable
- [ ] Verify sufficient buying power/margin
- [ ] Confirm expiration date and time decay profile
- [ ] Check implied volatility rank/percentile
- [ ] Review upcoming earnings or events
- [ ] Calculate breakeven points
- [ ] Set profit target and stop-loss levels

**During Trade Management:**
- [ ] Monitor aggregate portfolio Greeks daily
- [ ] Track P/L against maximum loss
- [ ] Adjust delta if exceeds neutrality threshold
- [ ] Roll positions if approaching expiration
- [ ] Document all adjustments with rationale

**Post-Trade Review:**
- [ ] Record actual P/L vs. expected
- [ ] Analyze what worked and what didn't
- [ ] Update strategy parameters if needed
- [ ] Document lessons learned

## Common Pitfalls and Mitigations

**Pitfall**: Over-leveraging with undefined risk strategies
**Mitigation**: Always use defined-risk strategies or maintain adequate margin buffer

**Pitfall**: Ignoring volatility regime changes
**Mitigation**: Monitor IV rank and adjust strategy selection accordingly

**Pitfall**: Holding through expiration without management plan
**Mitigation**: Set calendar reminders for 7 days, 3 days, and 1 day before expiration

**Pitfall**: Chasing losses with larger position sizes
**Mitigation**: Implement strict position sizing rules (e.g., max 2% of capital per trade)

**Pitfall**: Neglecting transaction costs
**Mitigation**: Include commissions and slippage in backtests and profit calculations

## Integration with Existing Ordinis-1 Components

**Portfolio Management Integration:**
- Import positions from portfolio-management skill
- Track options positions alongside equity holdings
- Aggregate Greeks with overall portfolio delta
- Include options P/L in performance analytics

**Due Diligence Integration:**
- Research underlying companies before opening positions
- Analyze earnings history and volatility patterns
- Assess sector and market conditions
- Document strategy rationale using due-diligence framework

**Benchmarking Integration:**
- Compare strategy returns against VIX or CBOE indices
- Benchmark risk-adjusted returns (Sharpe, Sortino)
- Evaluate performance across market conditions

## Advanced Topics (Future Enhancements)

**Volatility Surface Modeling:**
- Build term structure and skew analysis
- Identify mispriced options
- Construct delta-neutral volatility arbitrage

**Machine Learning Integration:**
- Predict optimal entry/exit timing
- Forecast volatility regime changes
- Automate parameter optimization

**Multi-Asset Strategies:**
- Pairs trading with options
- Sector rotation using options leverage
- Cross-asset volatility strategies

## References and Further Study

**Alpaca Official Resources:**
- [Alpaca API Documentation](https://docs.alpaca.markets/)
- [Alpaca GitHub Organization](https://github.com/alpacahq)
- [Alpaca Learn Center](https://alpaca.markets/learn/)

**Industry Education:**
- [Options Industry Council](https://www.optionseducation.org/)
- [CBOE Education](https://www.cboe.com/education/)

**Quantitative Finance:**
- "Options, Futures, and Other Derivatives" by John Hull
- "Option Volatility and Pricing" by Sheldon Natenberg
- "Dynamic Hedging" by Nassim Taleb

**Python Libraries:**
- [QuantLib Python](https://www.quantlib.org/docs.shtml)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/)

## Support and Community

**Alpaca Community:**
- [Alpaca Community Forum](https://forum.alpaca.markets/)
- [Alpaca Slack](https://alpaca.markets/slack)
- [GitHub Issues](https://github.com/alpacahq)

**Options Trading Communities:**
- r/options (Reddit)
- r/thetagang (Reddit - options selling strategies)
- Elite Trader (options forum)

---

*This skill is designed for educational and research purposes. All examples use Alpaca's paper trading environment. Live trading involves substantial risk and requires appropriate risk management, capital allocation, and regulatory compliance.*
