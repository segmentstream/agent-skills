# Dimensions and Metrics Reference

Business context, example values, and interpretation guidance for SegmentStream report dimensions and metrics. The `get_report_table` tool schema is the authoritative source for allowed field names, filter operators, and parameter structure -- this reference explains what each field means and when to use it.

---

## Dimensions

### Campaign Hierarchy

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `campaign_name` | Name of the advertising campaign | "Brand - US", "Summer Sale 2026" | Campaign-level performance breakdown, identifying top/bottom performers |
| `campaign_id` | Platform-assigned campaign ID | "12345678" | Joining with external data, deduplication when names change |
| `campaign_type` | Type of campaign (platform-specific) | "Search", "Performance Max", "Display" | Comparing performance across campaign types |
| `ad_group_name` | Name of the ad group within a campaign | "Exact Match - Brand Terms" | Ad group-level optimization |
| `ad_group_id` | Platform-assigned ad group ID | "111222333" | Precise identification when names are reused |
| `ad_name` | Name of the individual ad creative | "RSA - Summer Offer v2" | Creative-level performance analysis |
| `ad_id` | Platform-assigned ad ID | "444555666" | Creative-level tracking |
| `account_name` | Advertising account name | "Brand US - Google Ads" | Multi-account performance comparison |
| `account_id` | Advertising account ID | "123-456-7890" | Account-level aggregation |

### Traffic Source

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `ad_platform` | Advertising platform name | "google", "facebook", "bing", "tiktok" | Platform-level performance comparison |
| `source_medium` | Combined source and medium | "google / cpc", "facebook / paid_social", "direct / none" | Channel-level analysis, the most common breakdown for marketing reports |
| `utm_source` | UTM source parameter | "google", "newsletter", "partner_site" | Tracking specific traffic sources |
| `utm_medium` | UTM medium parameter | "cpc", "email", "referral" | Grouping by traffic type |
| `utm_campaign` | UTM campaign parameter | "summer_sale_2026", "brand_awareness" | Campaign tracking across platforms |
| `utm_content` | UTM content parameter | "banner_v1", "text_link" | Creative or placement variant analysis |
| `utm_term` | UTM term parameter (keyword) | "running shoes", "best crm software" | Keyword-level analysis for search campaigns |

**`source_medium` values have specific meanings:**

| Value | Meaning |
|-------|---------|
| `google / cpc`, `facebook / paid_social`, etc. | Attributed to that source and medium |
| `direct / none` | Direct traffic -- user typed URL, used a bookmark, or clicked an app link. This is a real attributed channel, not "unknown". |
| `(not attributed)` | The attribution engine could not determine the source. This is truly unattributed traffic. |

### Geography

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `country` | Country name | "United States", "Germany", "Japan" | Geographic performance analysis, market comparison |
| `region` | Region or state within a country | "California", "Bavaria", "England" | Regional targeting optimization |
| `city` | City name | "New York", "London", "Berlin" | City-level performance (useful for local campaigns) |

### Technology

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `device` | Device type | "desktop", "mobile", "tablet" | Device-level performance comparison, bid adjustments |
| `device_brand` | Device manufacturer | "Apple", "Samsung", "Google" | Audience device preference analysis |

### Content

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `landing_page` | Full landing page URL | "https://example.com/products/shoes" | Landing page performance analysis |
| `landing_page_path` | Landing page path (without domain) | "/products/shoes" | Landing page analysis grouped across domains |
| `domain` | Website domain | "example.com", "shop.example.com" | Multi-domain performance comparison |

### Time

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `date` | Calendar date | "2026-03-01" | Daily trends, identifying specific date anomalies |

Note: For weekly or monthly aggregation, use `get_report_chart` with the `granularity` parameter set to `"week"` or `"month"` instead of using `date` as a dimension.

### Targeting

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `targeting_name` | Name of the targeting criterion | "In-Market: Running Shoes" | Audience targeting performance |
| `targeting_id` | Targeting criterion ID | "12345" | Precise targeting identification |

### Identity

| Dimension | Description | Example values | Common use cases |
|-----------|-------------|----------------|------------------|
| `user_id` | Known user identifier | "user_abc123" | User-level journey analysis (requires identity resolution) |
| `anonymous_id` | Anonymous visitor identifier | "anon_xyz789" | Session-level analysis |
| `data_source_id` | Data source that provided the record | "ds_001" | Debugging data ingestion issues |

### Custom Dimensions

Custom dimensions are project-specific and must be discovered using `list_custom_dimensions(projectId)`. They use IDs in the format `custom_dimension_xxx` (e.g., `custom_dimension_bfb66a28`).

Common examples of custom dimensions:
- **Channel grouping** -- custom rules that classify traffic into business-specific channel categories
- **Product category** -- groups landing pages or conversions by product line
- **Brand vs Non-Brand** -- separates brand search from generic search

Use `get_report_dimension_values(projectId, customDimensionKey: "custom_dimension_xxx")` to see available values for a custom dimension.

---

## Metrics

### Attribution Metrics (Traffic and Cost Data)

These metrics come from ad platform imports and website tracking. They do not require a conversion or attribution model selection.

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| `cost` | Total advertising spend | Primary budget metric. Compare across channels to see spend distribution. |
| `impressions` | Number of times ads were shown | Measures reach. High impressions with low clicks may indicate poor ad relevance. |
| `clicks` | Number of ad clicks | Measures interest. Compare with sessions to detect click fraud or tracking gaps. |
| `sessions` | Website sessions from this source | SegmentStream-tracked sessions. May differ from ad platform click counts due to tracking methodology. |
| `users` | Unique users from this source | Deduplicated visitor count. Lower than sessions when users visit multiple times. |
| `cpc` | Cost per click (cost / clicks) | Efficiency metric. Lower CPC means cheaper traffic, but always evaluate alongside conversion metrics. |
| `cpm` | Cost per thousand impressions (cost / impressions * 1000) | Awareness campaign efficiency. Useful for display and video campaigns. |
| `ctr` | Click-through rate (clicks / impressions) | Ad engagement metric. Higher CTR generally indicates better ad relevance. |
| `avg_session_duration` | Average session duration in seconds | Engagement quality signal. Very short sessions may indicate poor landing page experience. |
| `time_on_site` | Total time on site | Aggregate engagement metric. |
| `video_views` | Number of video views | Video campaign performance metric. |
| `video_view_rate` | Video view rate | Percentage of impressions that resulted in a video view. |

### Conversion Metrics (Attribution-Dependent)

These metrics require selecting a conversion definition and attribution model. They measure business outcomes attributed to marketing channels.

#### Event-Time Metrics

Attribute the conversion to the **date the conversion occurred**.

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| `conversions` | Number of attributed conversions | Primary conversion volume metric. Compare across channels to see which drives the most conversions. |
| `conversion_value` | Revenue from attributed conversions | Total revenue attributed to a channel/campaign. Use for revenue-focused optimization. |
| `converted_users` | Unique users who converted | Deduplicated converter count. Lower than conversions when users convert multiple times. |
| `conversion_rate` | Conversion rate | Percentage of sessions that result in a conversion. Higher is better, but consider traffic quality. |
| `aov` | Average order value (conversion_value / conversions) | Revenue per conversion. Useful for identifying high-value channels vs high-volume channels. |
| `cpa` | Cost per acquisition (cost / conversions) | How much it costs to acquire one conversion. Lower is better. Compare across channels to find the most efficient ones. |
| `roas` | Return on ad spend (conversion_value / cost) | Revenue generated per unit of ad spend. A ROAS of 5.0 means $5 revenue for every $1 spent. What's "good" depends on profit margins. |

#### Conversion-Time Metrics

Attribute the conversion to the **date of the converting session** (not when the original touchpoint occurred). Useful for evaluating campaign launch performance and understanding delayed conversion effects. Metric names follow the pattern `*_by_conv_time` (e.g., `conversions_by_conv_time`, `conversion_value_by_conv_time`). See the tool schema for the full list.

#### Projected Metrics

Include modeled projections for conversions that have not yet been fully attributed (useful for recent dates where the attribution window has not closed). These combine actual observed data with projected values. Metric names follow the pattern `*_incl_projected` (e.g., `conversions_incl_projected`, `roas_incl_projected`). See the tool schema for the full list.

---

## Common Dimension x Metric Combinations

These combinations answer the most frequently asked marketing questions.

### Channel Performance Overview

**Dimension:** `channel`
**Metrics:** `cost`, `conversions`, `roas`, `cpa`
**Question answered:** "Which channels are driving the best results for my budget?"

### Campaign Deep-Dive

**Dimension:** `campaign_name`
**Metrics:** `cost`, `clicks`, `conversions`, `roas`, `cpa`
**Filter:** `ad_platform` equals a specific platform
**Question answered:** "Which campaigns within Google Ads are performing best?"

### Geographic Analysis

**Dimension:** `country` or `region`
**Metrics:** `cost`, `conversions`, `conversion_value`, `roas`
**Question answered:** "Which markets are most profitable?" or "Should we increase spend in Germany?"

### Time Trend Analysis

**Tool:** `get_report_chart` with granularity `"day"` or `"week"`
**Metrics:** `cost`, `conversions`, `roas`
**Question answered:** "How has our ROAS trended over the past month?" or "Did our spend drop last week?"

### Device Performance

**Dimension:** `device`
**Metrics:** `cost`, `sessions`, `conversions`, `cpa`, `roas`
**Question answered:** "Are mobile campaigns converting as well as desktop?"

### Campaign Type Comparison

**Dimension:** `campaign_type`
**Metrics:** `cost`, `impressions`, `clicks`, `conversions`, `roas`
**Question answered:** "How does Performance Max compare to Search campaigns?"

### Landing Page Analysis

**Dimension:** `landing_page_path`
**Metrics:** `sessions`, `conversions`, `conversion_rate`
**Question answered:** "Which landing pages have the best conversion rate?"

### Ad Creative Analysis

**Dimensions:** `ad_name` (filtered to a specific campaign)
**Metrics:** `impressions`, `clicks`, `ctr`, `conversions`, `cpa`
**Question answered:** "Which ad creatives are driving the most efficient conversions?"

### Cost Monitoring (No Conversion Data Needed)

**Dimension:** `ad_platform` or `campaign_name`
**Metrics:** `cost`, `clicks`, `impressions`, `cpc`, `ctr`
**Note:** No conversion or attribution model selection required for cost-only queries.
**Question answered:** "How much did we spend on each platform this month?" or "What's our CPC trend?"
