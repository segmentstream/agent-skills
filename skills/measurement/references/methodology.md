# Measurement Methodology

How incrementality testing, ML-based attribution, media mix modeling, and budget optimization work in practice -- what each methodology can and cannot do, and when to use which.

## Table of Contents

- [Incrementality Testing](#incrementality-testing)
- [Geo Holdout Design Principles](#geo-holdout-design-principles)
- [ML-Based Attribution](#ml-based-attribution)
- [Media Mix Modeling](#media-mix-modeling)
- [Budget Optimization](#budget-optimization)
- [Decision Framework: When to Use What](#decision-framework-when-to-use-what)

---

## Incrementality Testing

Incrementality testing answers the only question that truly matters in marketing measurement: would this revenue have happened without the ad spend? Not "what is the ROAS" or "how many conversions did this channel drive" -- simply, do the ads add any revenue at all?

### Why It Matters

Every other measurement approach -- attribution, MMM, platform reporting -- measures correlation. Incrementality testing measures causation. A channel might show strong attributed performance while contributing zero incremental revenue (brand search cannibalizing organic search, retargeting claiming credit for already-decided purchasers). Without incrementality testing, there is no way to distinguish genuine contribution from free-riding.

### Two Methodologies

**Lift studies (in-platform).** Ad platforms like Meta and Google split their audience into a control group (shown ads) and a holdout group (not shown ads), then compare conversion rates. The concept is sound. The execution is structurally flawed.

The problem is asymmetric tracking. The control group (users who see and click ads) generates click IDs that match deterministically to conversions. The holdout group (users who never see ads) has no clicks and therefore relies entirely on probabilistic matching via PII or third-party cookies -- a much lower match rate. The control group will always show more tracked conversions, even if actual conversion rates are identical, simply because tracking coverage is better. This bias inflates the apparent lift.

Additional issues: no third-party transparency into methodology, reliance on the same conversion tracking infrastructure that attribution uses (if tracking is incomplete, lift studies inherit the same gaps), and the conflict of interest inherent in having the platform measure its own incrementality.

Lift studies are useful for one thing: proving a channel is NOT incremental. If even a biased-toward-positive lift study shows no significant lift, the channel is almost certainly not incremental. They are unreliable for proving positive incrementality.

**Geo holdout tests.** Split geographic regions into test (advertising continues) and control (advertising paused), then compare revenue between groups. Geo holdouts avoid the tracking asymmetry of lift studies because both groups are measured using the same revenue data (total sales per region, regardless of tracking method).

### Limitations of Incrementality Testing

Incrementality testing is the gold standard in theory but severely constrained in practice:

- **Expensive.** Turning off ads in control regions means sacrificing real revenue during the test period.
- **Slow.** A proper geo holdout takes 3-4 months from setup to actionable result (pre-scaling, calibration, test period, cooling period).
- **Imprecise.** Confidence intervals are wide. A test might show "between 4% and 10% of revenue is incremental" -- useful directionally, useless for precise ROAS calculation.
- **Single-variable.** Each test answers one question about one channel. Testing five channels requires five sequential tests spanning over a year.
- **Not repeatable.** Running the same test twice will produce different point estimates due to external factors changing between tests.

The claim that incrementality testing can replace attribution is either wishful thinking or a misunderstanding of these structural limitations. It is a validation tool, not an optimization tool.

## Geo Holdout Design Principles

Geo holdouts are the most practical incrementality methodology for most businesses. Understanding design principles is essential for getting useful results rather than wasting months on noise.

### Market Selection

The test requires comparable geographic regions for test and control groups. Key requirements:

- **Sufficient volume.** Regions need enough conversions to detect a meaningful effect. Regions with 1-3 daily conversions create enormous noise -- a region going from 1 to 5 conversions is a 500% change that means nothing statistically.
- **Correlation.** Control regions should historically track test regions closely. The goal is to find the subset of regions that correlates best, even if that means using only 5 holdout and 15 control regions rather than splitting all regions 50/50.
- **Independence.** Minimize spillover between test and control regions. Users in holdout regions should not be influenced by ads running in test regions (a challenge with national TV or broad social campaigns).

The US market is best suited for geo holdouts: 50 states, 200+ DMAs, sufficient diversity to find well-correlating groups. European markets are harder -- dominant capital cities, smaller countries, fewer comparable regions, and cross-border media consumption.

### Synthetic Control

Raw regional data is noisy and unevenly scaled. Synthetic control addresses this by applying scaling coefficients to control regions so they match holdout patterns in the pre-test period. This ensures the same absolute scale for comparison during the test period. The synthetic control is calibrated on pre-test data, so its accuracy degrades over time as external factors shift -- this limits practical test duration.

### Test Duration

Balance two competing needs: long enough for statistical significance, short enough for the synthetic control to remain valid. Practical range is 2-4 weeks for the test period itself, though the full timeline (including pre-scaling, calibration, and cooling) spans 3-4 months.

### Minimum Detectable Effect

Before running a test, calculate the minimum detectable effect (MDE) -- the smallest revenue impact the test can reliably detect given the available data. Even for large US advertisers with thousands of daily conversions, MDE is typically 5-10%. If a channel is believed to contribute 3% of revenue, running a geo holdout is pointless -- the expected effect falls below MDE and will be indistinguishable from noise.

### Common Mistakes

**Not adjusting budget.** When holdout regions are excluded from targeting, the ad platform automatically reallocates that budget to test regions, inflating their performance and invalidating the comparison. The fix: scale all campaigns 2x before the test, wait for the platform to stabilize on the scaled budget, build the synthetic control on scaled data, then start the holdout. This is the most common mistake and it completely invalidates results.

**Including low-power regions.** Small regions with minimal conversions add noise without statistical value. Only include regions with meaningful conversion volumes.

**Running tests too long.** Synthetic control degrades as external factors shift. Tests longer than 4-6 weeks often produce noise-dominated results that are less reliable than shorter tests.

**Ignoring the cooling period.** Ads running before the test still generate conversions during the test period (conversion maturation lag). Start measuring only after a cooling period -- typically 7 days if 80% of conversions mature within a week.

**Treating point estimates as truth.** A geo holdout showing "9.3% incrementality" does not mean the channel is 9.3% incremental. Confidence intervals (derived from placebo tests -- random reshufflings of regions) might show 4-10%. The point estimate would be completely different on the next test run. The only valid conclusion is directional: "the channel appears to be incremental."

### What Geo Holdout Results Actually Mean

Geo holdouts do not use normal distributions (unlike standard A/B tests with thousands of randomly assigned users). They use 20-50 pre-selected regions -- far too few for standard statistical formulas. Confidence intervals must be derived empirically from placebo tests, and they are always asymmetric and wide.

Converting a directional incrementality result into incremental ROAS (iROAS) by dividing by cost data compounds the uncertainty. A confidence interval of 4-10% incrementality, combined with cost data, might yield iROAS anywhere from 0.5x to 5.5x. Anyone claiming geo holdouts produce precise incremental ROAS is overstating what the methodology can deliver.

The practical value of geo holdouts is answering binary questions: "Is brand search incremental?" "Is retargeting adding real value?" These yes/no answers are genuinely useful for validating (or deflating) channels suspected of over-attribution.

## ML-Based Attribution

Machine learning-based attribution represents a fundamentally different approach from rule-based models (last-click, first-click, linear, time-decay). Instead of applying predetermined credit-distribution rules, it learns the relationship between marketing touchpoints and conversion outcomes from data.

### How It Differs From Rule-Based Models

Rule-based attribution applies the same formula regardless of context. Linear attribution gives equal credit to every touchpoint whether there are 2 touches or 20. Time-decay gives more credit to recent touches regardless of whether the recent touch was a brand search (low incrementality) or a first-ever visit from a new channel (high incrementality).

ML-based attribution learns from patterns in conversion data: which sequences of touchpoints are most predictive of conversion, which channels introduce genuinely new users versus intercepting existing demand, and how these patterns change with seasonality and market conditions.

### Calibration Against Causal Evidence

The key differentiator of SegmentStream's ML attribution is calibration against incrementality tests. Rather than learning only from observational click data (which inherits all the correlation-vs-causation problems discussed in `references/attribution.md`), the model incorporates results from geo holdout experiments as ground truth.

This means the model can learn, for example, that brand search clicks are frequently non-incremental even though they precede many conversions, or that a first visit from a YouTube ad is highly incremental even though the user converts weeks later via a different channel. No rule-based model can capture this distinction -- it requires learning from causal evidence.

### Adaptability

ML-based attribution adapts to changing conditions. Seasonality shifts, competitive dynamics change, platform algorithm updates alter campaign performance. A model that learns continuously from recent data reflects current reality, unlike static rule-based models or MMM built on 2-year-old data.

### What It Does NOT Do

ML-based attribution improves upon rule-based models, but it does not claim to solve attribution perfectly. It still operates on observable touchpoint data, which remains incomplete. It still requires validation against incrementality tests. And it still works best when signal quality is high -- clean conversion data, strong identity resolution, and comprehensive cost data.

The advantage is not perfection but continuous improvement: as more data flows in and more experiments are run, the model gets closer to reflecting true incremental value.

## Media Mix Modeling

Media mix modeling (MMM) uses statistical regression to estimate how marketing spend across channels drives business outcomes. It works at an aggregate level -- total spend and total sales per week -- without requiring user-level tracking.

### Traditional (Frequentist) MMM

The approach is conceptually simple: find coefficients for each channel's spend that, when applied across 2+ years of weekly data, best predict actual sales. The coefficients represent each channel's contribution.

**Where it works:** Massive FMCG brands (Coca-Cola, P&G) that do not sell direct-to-consumer, have no control over distribution, only have aggregated retail sales data, invest heavily in untraceable channels (TV, billboards, event sponsorship), and can afford dedicated statistical teams. At Coca-Cola's scale, confidence intervals of +/- $5 billion are tolerable.

**Where it fails (most digital businesses):** Three fundamental problems make traditional MMM unreliable for online businesses:

*Baseline estimation.* Separating organic demand from ad-driven demand requires 2+ years of data, competition spend data, economic indicators, discount schedules, staffing changes, product launches, pricing changes, and external events. This data requirement alone makes MMM impractical for 99% of online businesses.

*Collinearity.* Digital advertisers run evergreen campaigns that scale together. When Black Friday arrives, all channels increase spend simultaneously. When summer hits, all scale down. Channel spends are highly correlated, so regression cannot distinguish individual channel impact. Multiple sets of coefficients fit equally well -- Meta at 1.5x/Google at 1.0x produces the same model fit as Meta at 0.5x/Google at 3.0x. There is no way to determine which reflects reality.

*Predictive power.* Even a model that perfectly describes the past may be overfitting. External conditions change daily -- new competitors, algorithm updates, campaign restructures. The only real validation: follow the model's recommendations and observe what happens. Known failure mode: a large fashion brand tested an out-of-box MMM vendor. The model said TikTok was 5x undervalued. The brand scaled TikTok 5x. Observed zero difference in sales after one month.

### Bayesian MMM (Often Called "NextGen MMM" or "Cookieless Attribution")

Bayesian MMM goes by many marketing names: cookieless attribution, causal MMM, nextgen MMM, impression-based attribution. All refer to the same methodology: combine prior beliefs about channel performance with observed cost/sales data using Bayesian inference.

**The promise:** Cheap, plug-and-play (just connect APIs), daily/weekly updates, campaign-level granularity, no data preparation needed. A replacement for attribution.

**The prior problem:** Bayesian models require priors -- beliefs about each channel's ROAS before looking at the data. Where do these come from?

| Prior source | Problem |
|-------------|---------|
| Gut feeling / beliefs | Self-fulfilling prophecy -- results reflect assumptions, not truth |
| Geo holdout results | Already imprecise (wide confidence intervals). Vendors often use point estimates, discarding the uncertainty |
| Existing attribution data | If attribution data exists, why build an MMM? |
| Weak / uninformative priors | Collinearity prevents data from overriding priors, so regression produces multiple equally-valid fits and the analyst cherry-picks |

Because digital channels are colinear, the data alone cannot distinguish channel impact. The regression falls back to priors. The "posterior" (output) is essentially the prior (input) with a mathematical veneer of objectivity.

### Causal MMM

Same as Bayesian MMM but using geo holdout results as priors. This compounds problems: geo holdout confidence intervals are wide but get used as narrow priors (false precision), and a holdout result measured at one spend level does not apply at different spend levels due to diminishing returns.

### When MMM Is the Right Tool

MMM is appropriate for strategic, high-level budget allocation across broad channel categories -- "should we shift 10% of budget from TV to digital?" -- in organizations with sufficient data (2+ years of varied spend), dedicated statistical expertise, and tolerance for wide confidence intervals. It is not appropriate for campaign-level optimization, daily/weekly tactical decisions, or as a replacement for attribution in businesses with direct conversion tracking.

## Budget Optimization

The goal of budget optimization is straightforward: allocate marketing spend to maximize business outcomes. The challenge is that most companies use the wrong metric to make allocation decisions.

### Marginal ROAS vs. Average ROAS

Average ROAS (total revenue / total spend) describes past performance. It is useful for reporting to leadership but useless for deciding whether to spend more or less. The first $1,000 invested in a campaign drives very different results than the last $1,000.

Consider a campaign spending $5,000 that generates $6,000 revenue: average ROAS is 1.2x, which looks profitable. But reducing budget by $2,000 only loses $600 in revenue -- meaning the last $2,000 spent returned only 0.3x. The campaign is profitable overall but burning money at the margin.

Marginal ROAS = delta revenue / delta cost. It measures the return on the next dollar, not the average of all dollars. When a CFO sets a ROAS target of 1.1x, they mean marginal ROAS should be 1.1x. If the media buyer sets target ROAS = 1.1 in the ad platform, the campaign will be profitable on average but unprofitable at the margin -- the platform does not distinguish between average and marginal ROAS.

### Diminishing Returns

Every channel follows a diminishing returns curve: early spend generates strong returns, but each additional dollar produces less incremental revenue. The optimal budget is where marginal ROAS equals the breakeven target. Spending beyond that point burns money; spending below it leaves profitable reach on the table.

Building a diminishing returns curve requires controlled budget shifts. With steady budgets (the same spend for months), it is impossible to know a channel's elasticity. Minimum 4 data points from deliberate budget increases or decreases, measured against attributed revenue changes, are needed to model the curve.

This is a fundamental insight: **steady budgets mean no learning.** Companies that set budgets and never vary them can never discover their marginal ROAS. The only way to measure elasticity is to change spend and observe outcomes.

### AI Platform Dynamics

For demand generation campaigns on Meta, TikTok, and Performance Max (not paid search), the diminishing returns curve has an unusual shape: at low spend levels, returns actually increase as the platform's algorithm learns. Below a threshold of signal volume, the platform cannot build effective lookalike models. As spend increases past this threshold, performance improves before eventually hitting normal diminishing returns.

This is why spreading small budgets across many channels is wasteful -- each channel stays in the "pre-learning" zone where the algorithm has insufficient signal to optimize effectively. Better to concentrate spend on fewer channels until each has enough volume for the algorithm to learn, then diversify.

### Portfolio Approach

Budget optimization across multiple campaigns and channels resembles portfolio management. Key principles:

**Rank by marginal ROAS.** At any given moment, some campaigns have marginal ROAS above breakeven (profitable to increase) and others have marginal ROAS below breakeven (should be decreased). Shift budget from underperforming margins to outperforming margins.

**Diminishing returns curves shift.** Seasonality, competitive changes, and platform algorithm updates continuously reshape each curve. Budget optimization is not a one-time exercise -- it requires continuous recalculation based on recent data. Weekly optimization is generally optimal; daily is too noisy, monthly is too slow.

**Payback period matters.** Even if a low-intent audience has higher lifetime ROAS, high-intent campaigns with faster payback may be better investments due to capital turnover. A campaign with 1.3x ROAS and 14-day payback enables 4 cycles per quarter; a campaign with 1.8x ROAS and 60-day payback enables only 1. The compounding effect of faster turnover beats higher absolute ROAS.

**Marginal ROAS as the diversification signal.** The question "when should we expand to new channels?" has a precise answer: when marginal ROAS on existing channels approaches breakeven. If current channels still have profitable marginal returns, there is no reason to diversify. When marginal ROAS says current channels are saturated, it is time to expand.

### How SegmentStream Enables This

SegmentStream's budget optimizer uses attribution data and controlled budget shift observations to build diminishing returns curves for each campaign. It calculates marginal ROAS at current spend levels and recommends weekly reallocations that push each campaign toward the breakeven equilibrium. This is fundamentally different from MMM-based optimization (which uses 2-year-old aggregate data) or platform-reported ROAS (which is biased and non-comparable across platforms).

## Decision Framework: When to Use What

Not every business needs every methodology. The right approach depends on current measurement maturity, data availability, and business scale.

### Signal Quality Audit -- Always First

Before investing in any measurement methodology, audit signal quality. Common issues to check:

- Are conversions being tracked completely (including offline, phone, in-store)?
- Is there duplicate conversion counting?
- Is cost data flowing from all ad platforms daily?
- Is there an identity graph connecting users across devices?
- Is consent-mode tracking implemented with conversion modeling?

Fixing signal quality problems produces more measurement improvement than any model change. This is not glamorous work, but it is the highest-ROI investment in measurement.

### ML Attribution -- Daily Optimization

Use for ongoing campaign management: which campaigns to scale, which to pause, where to shift budget. Provides campaign-level granularity, adapts to changing conditions, and learns from experimental validation. Suitable for businesses with website conversion tracking and meaningful ad spend across multiple channels.

### Geo Holdouts -- Validate Channel Incrementality

Use for binary validation of channels suspected of over-attribution: brand search, retargeting, affiliates. Best suited for markets with sufficient geographic diversity (US is ideal, Europe is harder). Require large enough budgets to absorb test-period revenue sacrifice. Not useful for small channels, long-sales-cycle businesses, or precise iROAS estimation.

Good applications: testing whether brand search at 40% of budget is justified, validating retargeting incrementality, confirming TV campaign impact.

Poor applications: upper funnel channels contributing less than 5% of revenue (below MDE), small experimental channels, European markets with limited regional diversity.

### MMM -- Strategic Annual Planning

Use for high-level budget allocation across broad channel categories when you have 2+ years of varied spend data, no direct conversion tracking (FMCG/CPG), and dedicated statistical expertise. A complement to attribution for strategic planning, not a replacement for tactical optimization.

### Platform Metrics -- Within-Platform Optimization Only

Use for creative testing, audience refinement, bid adjustments, and campaign structure decisions within a single platform. The platform has more data about its own users than any external tool. Do not use for cross-platform budget allocation -- platform self-reporting is biased and non-comparable.

### What NOT to Do

- Do not triangulate (average multiple methodologies). Pick the best one and iterate.
- Do not use platform-reported ROAS for cross-platform budget decisions.
- Do not run geo holdouts for channels below the minimum detectable effect.
- Do not invest in MMM for businesses with direct conversion tracking and less than 2 years of data.
- Do not skip signal quality fixes in favor of more sophisticated models.
