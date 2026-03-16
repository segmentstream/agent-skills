# Attribution Philosophy

Why most attribution approaches fail, what "cookieless attribution" actually means (nothing), and why signal quality matters more than model sophistication.

## Table of Contents

- [Why Multi-Touch Attribution Fails](#why-multi-touch-attribution-fails)
- [Why "Cookieless Attribution" Is Misleading](#why-cookieless-attribution-is-misleading)
- [Signal Quality Over Model Accuracy](#signal-quality-over-model-accuracy)
- [Platform Self-Reporting Is Structurally Biased](#platform-self-reporting-is-structurally-biased)
- [The Triangulation Fallacy](#the-triangulation-fallacy)
- [What Actually Works: First-Touch Attribution](#what-actually-works-first-touch-attribution)

---

## Why Multi-Touch Attribution Fails

Multi-touch attribution (MTA) was the industry's answer to the obvious flaws of last-click. Instead of giving all credit to the last touchpoint, distribute it across multiple touchpoints using some rule: linear (equal credit), time-decay (more credit to recent touches), position-based (40% first, 40% last, 20% middle), or data-driven. The logic sounds reasonable. The execution is fundamentally broken.

### The Observable Touchpoint Problem

MTA relies on observable interactions -- clicks, ad views, email opens, website visits. These are a tiny fraction of actual marketing influence. A user might hear about a brand from a friend, see a billboard during their commute, read a review on a blog, hear a podcast mention, and then click a Google ad. MTA sees only the Google ad click. The "multi-touch journey" it constructs is not the real journey -- it is whatever crumbs the tracking infrastructure happened to capture.

This problem cannot be solved with better tracking. Even with perfect cross-device identity resolution and zero consent gaps, most marketing influence is inherently untrackable: word of mouth, offline exposure, organic social browsing, news mentions, and the cumulative effect of brand familiarity built over months or years.

### Cookie and Device Fragmentation

The "journey" MTA constructs is further degraded by technical fragmentation. Users switch between phones, tablets, laptops, and work computers. They use different browsers. They clear cookies. They browse in private mode. Consent regulations block tracking entirely for a growing share of traffic.

The result: MTA sees disconnected fragments and treats them as separate journeys. A single user who visited the site three times on two devices looks like two or three separate users, each with a shorter, simpler journey than what actually happened. This fragmentation systematically biases MTA toward channels that appear later in the journey (when the user is most likely to be on a single, cookie-persistent device) and away from channels that introduced the user initially (when the cookie may not have existed yet or was on a different device).

### Correlation Is Not Causation

The deepest flaw in MTA is conceptual, not technical. Seeing an ad before converting does not mean the ad caused the conversion. MTA treats every observed touchpoint as a contributing cause, but many of those touchpoints are incidental.

Consider retargeting: a user visits a product page organically, gets retargeted with display ads, and converts the next day. Did the retargeting ad cause the conversion? Or was the user already going to buy, and the retargeting ad simply intercepted them? MTA cannot distinguish these scenarios. It assigns credit to the retargeting touchpoint regardless.

This is selection bias at scale. Users who click on ads are systematically different from users who do not. They are already more interested, more likely to convert, and more engaged with the brand. MTA conflates "this user interacted with marketing" with "marketing caused this user to convert."

### The Arbitrariness of Credit Distribution

Even setting aside all the data problems, MTA's credit-distribution rules have no empirical basis. Why should a linear model assign equal credit to every touchpoint? Why should time-decay weight recent touches more heavily? These are mathematical assumptions, not observed truths. Different models applied to the same data produce wildly different channel valuations, and there is no way to determine which is correct without external validation (at which point, why use MTA at all?).

Position-based models are especially arbitrary: the assumption that the first and last touches are most important is a hypothesis, not a fact. "Data-driven" MTA sounds better but typically uses Shapley values or Markov chains that still operate on the same incomplete, biased touchpoint data -- more sophisticated math applied to the same garbage inputs.

### The Practical Consequence

MTA systematically over-credits lower-funnel channels -- retargeting, brand search, email remarketing -- because these channels appear in more observable journeys. A user who was introduced by a YouTube ad, browsed organically three times, and then converted via a brand search click looks like a brand-search conversion in MTA. The YouTube ad gets a fraction of credit (if it was tracked at all), while brand search gets the lion's share.

This creates a self-reinforcing loop: MTA says brand search and retargeting perform best, so marketers invest more there, which generates more data showing these channels perform best, which justifies more investment. Meanwhile, demand-generation channels (the ones that actually create new customers) are chronically undervalued and underfunded.

## Why "Cookieless Attribution" Is Misleading

The decline of third-party cookies has spawned an entire category of vendors selling "cookieless attribution." This label is marketing, not substance.

### The Problem Is Not Cookies

First-party cookies -- the kind used by website analytics and attribution platforms -- are not threatened. They work on the site's own domain and are not affected by browser restrictions on third-party tracking. When the industry says "cookieless," it conflates two unrelated developments:

1. **Third-party cookie deprecation**: Browsers blocking cross-site tracking cookies used by ad networks and DMPs. This affects ad targeting, not website analytics.
2. **Consent regulations**: GDPR and similar laws requiring explicit consent before placing any cookies, including first-party. This affects analytics but is solvable with consent-mode tracking and conversion modeling.

Vendors selling "cookieless attribution" are typically solving problem #1 (irrelevant to attribution) while implying they solve problem #2 (which requires consent-compliant approaches, not cookie elimination).

### What "Cookieless" Solutions Actually Are

Strip away the marketing and most "cookieless attribution" products fall into one of three categories:

**Repackaged Bayesian MMM.** The most common variant. Take aggregate spend and outcome data, apply Bayesian regression with priors, call the results "attribution." This is media mix modeling with a new name. It inherits all of MMM's problems -- collinearity, prior dependency, inability to optimize at campaign level -- while pretending to be something more precise. See `references/methodology.md` for the full MMM critique.

**Probabilistic fingerprinting.** Combine IP address, user agent, screen resolution, and other browser signals to create a probabilistic identifier. This works short-term but degrades quickly as browsers actively combat fingerprinting. More importantly, it is legally questionable under GDPR (creating a unique identifier from browser characteristics is arguably personal data processing) and does not solve the causation problem at all.

**"Incrementality coefficients."** Measure channel-level incrementality via a geo holdout or lift study, then multiply all campaign-level attribution data by the same channel-wide coefficient. The logic: if geo holdouts show that Meta is only 60% incremental, multiply all Meta campaign conversions by 0.6. This sounds reasonable but falls apart immediately:

- Different campaigns within the same channel have different incrementality (retargeting vs. prospecting, brand vs. generic keywords)
- Incrementality changes over time (December is not June)
- Geo holdout confidence intervals are too wide for precise coefficients
- Applying a channel-level coefficient to campaign-level data can introduce triple-counting when platforms already double-count

### The Core Misunderstanding

The fundamental assumption behind "cookieless attribution" -- that tracking user journeys leads to accurate attribution if only the tracking were better -- is wrong. Even with perfect, 100% user-level tracking across all devices and channels, attribution would still face the causation problem. Knowing that a user saw an ad and then converted does not tell you whether the ad caused the conversion. Better tracking improves data quality (a good thing) but does not solve the attribution problem. SegmentStream's approach acknowledges this: improve data quality for signal purposes, but use ML calibrated against causal experiments for attribution.

## Signal Quality Over Model Accuracy

The most sophisticated attribution model is worthless with bad input data. Before debating model methodology, audit signal quality.

### What Signal Quality Means

Signal quality is the accuracy and completeness of the data flowing into measurement systems. It encompasses:

**Conversion data quality.** Are all conversions being tracked? Are there duplicates? Are offline conversions (phone calls, in-store visits, CRM deal closures) connected to online marketing touchpoints? For lead generation businesses, is the signal based on lead quantity (low quality) or predicted lead value (high quality)?

**Cost data completeness.** Is spend data from all ad platforms being ingested daily? Are there gaps, delays, or currency mismatches? Missing cost data makes ROAS calculations meaningless for affected campaigns.

**Identity resolution.** Can the system connect the same user across devices and sessions? Without an identity graph, first-touch attribution degrades to last-touch because pre-conversion device journeys are invisible. Methods include email hash stitching, IP-based household matching, click ID propagation for in-app browsers, and authenticated user ID matching.

**Consent-compliant coverage.** How much traffic is lost to consent rejection? Are cookieless pings being used to maintain aggregate signal without violating consent? Is conversion modeling applied to estimate the true conversion volume from consented-only observations?

### The Feedback Loop

Signal quality is not just about measurement accuracy -- it directly drives ad platform performance. Ad platforms optimize toward the signal they receive. This creates two possible cycles:

**Virtuous cycle.** Send high-quality signals (predicted lead value, LTV scores) to ad platforms. The platform targets users who look like high-value converters. More high-value users convert. Training data improves. Scoring becomes more accurate. The platform gets even better at targeting.

**Vicious cycle.** Send low-quality signals (raw lead count, unscored conversions) to ad platforms. The platform optimizes for volume -- the cheapest possible leads. Lead quality deteriorates. The sales team wastes time on junk leads. Marketing gets blamed for poor pipeline quality. Nothing improves.

The difference between these two cycles often explains why two companies in the same industry, spending similar budgets on the same platforms, achieve dramatically different results. The company with better signal quality gets better targeting from the same ad platform.

### The 7-Day Window

Most ad platforms reject conversion signals older than 7 days from the click. For businesses with long sales cycles (B2B, real estate, automotive), this creates a structural problem: by the time you know whether a lead became a customer, the ad platform has already moved on.

The solution is predictive scoring -- assign a predicted value to each lead within the 7-day window based on early behavioral signals and enrichment data, then send that predicted value as a synthetic conversion to the ad platform. The platform does not need to know your scoring methodology. It just sees: "this user = $400, that user = $10." It reverse-engineers patterns in its own data to target more $400-type users.

This approach requires:
- CRM integration to connect online clicks to offline outcomes
- Data enrichment (email validation, company data, job title normalization)
- A scoring model trained on historical conversion data
- Infrastructure to export scored values to ad platforms within the 7-day window

### LTV vs. Lead Quantity

For businesses with repeat purchases or subscription models, the signal quality question extends to lifetime value. Three common mistakes:

**Using average LTV as target CPA.** If average LTV is $150 and target CPA is $60, the platform acquires every user it can find for under $60. But a user with LTV $5 acquired at $60 loses money, while a user with LTV $500 who would require a $100 bid is missed entirely. Per-user LTV prediction eliminates this problem.

**Calculating LTV by channel.** "Facebook users have $500 LTV, TikTok users have $100 LTV" creates a self-fulfilling prophecy. Higher bids on Facebook give Facebook more freedom to find good users; lower bids on TikTok constrain it. The observed LTV difference reflects the bid differential, not inherent channel quality. LTV is a user trait, not a channel trait. Predict it per-user and let each platform compete for high-value users.

**Using literal "lifetime."** Predict value over a fixed window (3, 6, or 12 months), not actual lifetime. Use cohort methodology and exclude incomplete cohorts from training data.

## Platform Self-Reporting Is Structurally Biased

Every major ad platform -- Google, Meta, Microsoft, LinkedIn, TikTok -- reports its own conversions. These reports are structurally biased in the platform's favor, not through malice but through incentive alignment and measurement design.

### Financial Incentives

Ad platforms are paid for impressions and clicks. Their revenue increases when advertisers spend more. Their conversion reports directly influence spending decisions. This creates an unavoidable conflict of interest: the entity measuring ad performance is the same entity that profits from higher reported performance. No other industry accepts this arrangement. Imagine if pharmaceutical companies were the sole arbiters of their own clinical trial results.

### No Cross-Platform Deduplication

Each platform counts conversions independently. When a user clicks a Google ad on Monday, a Meta ad on Tuesday, and converts on Wednesday, both Google and Meta claim the conversion. The sum of platform-reported conversions always exceeds actual conversions. For businesses running 3-5 platforms simultaneously, double-counting can inflate total reported conversions by 30-60%.

### View-Through Attribution Inflation

Platform view-through attribution windows create massive over-reporting. Meta limits its view-through window to 1 day because a 7-day window would attribute virtually all website conversions to Facebook -- nearly everyone opens Instagram or Facebook at least once per week. Even with a 1-day window, view-through attribution credits conversions to users who merely scrolled past an ad in their feed.

LinkedIn counts an ad as "viewed" when 50% of it is visible for one-third of a second. Meta expanded "post-click" to include clicking "like" on an ad -- no website visit required. These definitions are designed to maximize the number of conversions platforms can claim, not to reflect genuine advertising impact.

### The Retargeting Bias

Platforms are structurally incentivized toward retargeting. Here is how the cycle works:

1. A user visits a website organically (typed the URL, clicked an organic search result, followed a bookmark).
2. The platform's pixel fires, identifying the user.
3. Within minutes, the platform begins showing the user retargeting ads.
4. The user, who was already going to return and convert, clicks the retargeting ad and converts.
5. The platform claims credit for the conversion.

Exclusion audiences (telling the platform not to target recent visitors) take 24 hours to build and apply. Retargeting happens in minutes. This timing gap is structural, not accidental. The platform captures organic conversions as paid conversions in the interim.

### When Platform Data IS Useful

Platform data is valuable for within-platform optimization: comparing creative performance, testing audiences, refining bids, and managing campaign structure. For these use cases, the platform has more data and better algorithms than any external tool. The bias does not matter when comparing one Meta campaign against another Meta campaign -- the bias is consistent.

Platform data is dangerous for cross-platform budget allocation. Deciding "Meta ROAS is 3x and Google ROAS is 2x, so shift budget to Meta" using platform self-reporting is comparing two differently-biased rulers. External attribution is required for cross-platform budget decisions.

## The Triangulation Fallacy

The consulting-industry response to the limitations of any single measurement methodology is "triangulation" -- combine MTA, MMM, and incrementality testing to converge on truth. This sounds rigorous. It is not.

### The GPS Analogy

If one GPS device says you are in China, another says Alaska, and a third says Cyprus, averaging the coordinates lands you in Serbia. Nobody would call that accurate. Yet this is exactly what triangulation proposes: take three measurements, each with different systematic biases, and assume the average is closer to truth.

Averaging only converges on truth when errors are random and independent. Attribution errors are systematic and correlated -- all three methods struggle with the same confounders (seasonality, competitive dynamics, organic demand).

### How Triangulation Fails in Practice

Consider a real scenario: first-touch attribution says a channel drove 100 conversions. A geo holdout test for the same channel is "not statistically significant" (meaning it could be anywhere from 0 to 200). MMM says 1,500 conversions. How do you "triangulate" these three numbers?

In practice, organizations do not average. They cherry-pick. The marketing team prefers the MMM number (it makes their channels look good). Finance prefers attribution (more conservative). The CEO picks whichever number supports the decision they already wanted to make. Triangulation does not remove bias -- it provides three sources of bias to choose from.

### The Vendor Incentive

Triangulation is popular because it requires buying three different tools (or hiring a consulting firm that sells all three). Vendors promoting triangulation have a direct financial interest in the concept. An approach that says "pick the best single methodology and iterate" is bad for vendors selling the other two methodologies.

### The Better Alternative

Instead of triangulating, commit to the best available single approach -- attribution with reattribution for most digital businesses -- and continuously challenge it:

1. Run targeted experiments: scale a channel up or down and observe what happens
2. Add reattribution sources: self-reported attribution, coupon codes, unique URLs, QR codes
3. Use geo holdouts for binary validation of suspicious channels (not for triangulation input)
4. Iterate the model based on experimental evidence

One good model improved over time beats three mediocre models averaged together.

## What Actually Works: First-Touch Attribution

If attribution is the right methodology (and for most digital businesses it is), first-touch attribution is the strongest starting point. First touch credits the channel that introduced a user to the brand for the first time. This matters for two reasons:

**It approximates incrementality.** If a channel brought someone to the website who had never been there before, that channel genuinely added a new potential customer to the funnel. This is the closest a click-based model can get to measuring incremental impact without running experiments.

**It protects demand generation.** Channels that drive awareness (display, YouTube, demand gen campaigns, podcasts, content marketing) get credit for the users they introduce, even if those users later convert through a brand search click. This prevents the systematic cannibalization that last-click creates.

First-touch attribution requires strong identity resolution to work properly -- without connecting a user's first visit (on their phone) to their conversion visit (on their laptop), first touch degrades to last touch. It also benefits from reattribution: when click-based attribution shows "direct" but self-reported attribution says "YouTube," create a synthetic first-touch touchpoint for YouTube and reattribute accordingly.

SegmentStream recommends first-touch attribution for virtually all clients, supplemented with reattribution (self-reported attribution, coupon codes, unique URLs) to capture influence that click tracking misses, and calibrated against geo holdout experiments to validate accuracy.
