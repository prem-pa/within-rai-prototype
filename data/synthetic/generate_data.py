"""
Generate synthetic transcripts and Slack messages for 3 clients:
Casper, Nike, Hugo Boss.

Run: python data/synthetic/generate_data.py
Outputs: data/synthetic/transcripts.json, data/synthetic/slack_messages.json
"""

import json
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# TRANSCRIPTS
# ---------------------------------------------------------------------------

TRANSCRIPTS = [
    # ── CASPER ──────────────────────────────────────────────────────────────
    {
        "transcript_id": "t_casper_001",
        "client": "Casper",
        "meeting_name": "Weekly Performance Review",
        "date": "2026-04-07",
        "participants": ["Sarah (AM)", "Jake (Client)"],
        "text": """Sarah: Good morning Jake. Let's jump into the numbers for last week.

Jake: Sure, go ahead.

Sarah: So looking at Google Ads first — our Sleep Collection campaign saw a CTR drop of 12% week-over-week, from 4.8% down to 4.2%. CPC held steady at $1.34. Impressions were actually up 8%, so the volume is there but clicks aren't converting as well.

Jake: What's your read on the CTR drop? Audience fatigue?

Sarah: Probably. The creative set has been running for six weeks. I'd recommend we rotate in the new lifestyle images we got approved last month. On the Facebook side, things looked better — the Retargeting — Cart Abandoners campaign had a 3.1x ROAS, up from 2.7x the week before. Spend was $18,400 for the week.

Jake: That's solid. What about the TikTok test we kicked off?

Sarah: TikTok is still in the learning phase. We've spent $4,200 of the $15,000 test budget. CPM is running at $9.80 which is competitive. The pillow-in-use UGC content is outperforming the studio shots — 22% higher engagement rate. I'd give it two more weeks before drawing conclusions.

Jake: Agreed. Let's plan to refresh the Google creative this week and keep TikTok running. What's total spend for April so far?

Sarah: We're at $62,500 of the $210,000 monthly budget. Pacing looks fine through end of month.""",
    },
    {
        "transcript_id": "t_casper_002",
        "client": "Casper",
        "meeting_name": "Q2 Budget Planning Call",
        "date": "2026-04-02",
        "participants": ["Sarah (AM)", "Marcus (AM)", "Jake (Client)", "Dana (Client)"],
        "text": """Marcus: Thanks everyone for joining. We want to walk through Q2 budget allocation and get sign-off.

Dana: We've got $620,000 total for Q2. How are you thinking about splitting it?

Sarah: Our recommendation is: Google Search 35%, Facebook/Instagram 30%, TikTok 15%, Programmatic Display 12%, and we'd hold 8% as a flex reserve for opportunities or tests.

Jake: What's the rationale for bumping TikTok from Q1's 8% to 15%?

Marcus: Two things. First, Q1 TikTok ROAS came in at 2.4x despite still being in testing — that's ahead of where Facebook was at the same stage. Second, the 25-34 demo we're trying to reach on TikTok has 60% lower CPM than Facebook right now.

Dana: Makes sense. What about Search — any changes to campaign structure there?

Sarah: Yes, we're proposing to consolidate from 9 ad groups down to 6. We've had budget fragmentation issues where the smaller ad groups aren't getting enough data to optimize properly. Consolidating around the core product lines — Original, Wave, Snow, and accessories — should help Quality Score and lower CPC.

Jake: I like it. Dana, any concerns?

Dana: No, the consolidation makes sense. Let's go with the recommended split. Can you send the revised media plan by Friday?

Marcus: Absolutely, I'll have it over by EOD Thursday.""",
    },
    {
        "transcript_id": "t_casper_003",
        "client": "Casper",
        "meeting_name": "Creative Strategy Review",
        "date": "2026-03-25",
        "participants": ["Sarah (AM)", "Jake (Client)"],
        "text": """Sarah: I wanted to go through the creative performance data from Q1 and get your input on Q2 direction.

Jake: Sure, what stood out?

Sarah: The lifestyle photography — people actually using the mattress in realistic bedroom settings — outperformed studio product shots by 34% on CTR across both Google Display and Facebook. The 'sleep science' angle we tested in February had strong engagement but lower conversion. People clicked and read but didn't buy.

Jake: That tracks with what we hear internally. The science content is good for brand but not for direct response.

Sarah: Exactly. So for Q2, my recommendation is to lean into lifestyle for direct response campaigns and reserve the educational content for top-of-funnel awareness placements where we're not optimizing for conversions.

Jake: What about video? We've been hesitant to invest there.

Sarah: I'd suggest a modest test — maybe two 15-second UGC-style videos shot on iPhone for TikTok and Instagram Reels. Low production cost, authentic feel. The bedding brands that are winning on TikTok right now are mostly using this format.

Jake: What would that cost to produce?

Sarah: If we work with one of our creator partners, probably $3,000-$5,000 for a package of 4-6 clips. We'd want to test against the static ads before scaling.

Jake: Let's do it. Put it in the Q2 plan.""",
    },
    {
        "transcript_id": "t_casper_004",
        "client": "Casper",
        "meeting_name": "Monthly Business Review",
        "date": "2026-03-31",
        "participants": ["Sarah (AM)", "Marcus (AM)", "Jake (Client)", "Dana (Client)", "VP Marketing (Client)"],
        "text": """Marcus: Let's start with the March topline. Total ad spend was $198,400 against a $200,000 budget — 99.2% pacing. Overall blended ROAS came in at 3.1x, versus the 2.8x target.

VP Marketing: Good. What drove the outperformance?

Sarah: Three things. Facebook Retargeting continued to over-index — 4.2x ROAS on $52,000 spend. Our Google Shopping campaigns benefited from a competitor pulling back in mid-March, so we captured incremental share at lower CPCs. And the Spring Sale campaign we ran March 22-28 delivered 3.8x on $28,000 spend.

Dana: The Spring Sale was really successful. What's our read on why it worked so well?

Sarah: The 20%-off offer was stronger than anything we'd run since Black Friday. We also launched the sale on a Tuesday and front-loaded spend on Tuesday-Wednesday, which historically sees less competition. Creative was fresh — the 'Better Sleep Starts Tonight' messaging tested well in our pre-launch polls.

VP Marketing: I want to make sure we replicate those conditions for the Memorial Day campaign. Can you put together a brief on what made Spring Sale work?

Marcus: Yes, I'll put that together this week. Should be useful context for the May planning session.

Jake: One thing I want to flag — our review volume on Google dropped in March. Not sure if it's related to ads but wanted to mention it.

Sarah: Worth monitoring. I don't think paid is a direct driver of review volume but it could be an indirect signal. I'll add review velocity to our KPI dashboard so we can track it going forward.""",
    },

    # ── NIKE ─────────────────────────────────────────────────────────────────
    {
        "transcript_id": "t_nike_001",
        "client": "Nike",
        "meeting_name": "Running Category Weekly",
        "date": "2026-04-08",
        "participants": ["Tom (AM)", "Priya (Client)"],
        "text": """Tom: Priya, let's go through running category performance for the week of March 30 through April 5.

Priya: Go ahead.

Tom: Pegasus 41 launch campaign is performing well. Google Search CTR is 6.2% against a 4.5% benchmark. We're seeing strong branded search volume — 'Pegasus 41 release date' and 'Pegasus 41 vs 40' are the top organic assists. Paid CPC for non-branded running terms is $2.18, down from $2.67 last week as quality score improved.

Priya: What's driving the quality score improvement?

Tom: We reorganized the ad groups to match intent more tightly — separating 'running shoes for marathon' from 'everyday running shoes' queries. Each ad group now has dedicated copy. The marathon-intent group has a 7.8% CTR, which is exceptional.

Priya: That's great. What about Facebook and Instagram?

Tom: Meta is delivering strong reach on the video assets — the 'Run Your World' 30-second spot has 4.2M impressions at a $6.40 CPM. Video completion rate is 68% for the :15 cut and 51% for the :30, both above category benchmarks. Retargeting off the video viewers is converting at 2.9x ROAS.

Priya: The :15 cut — is that the one with the track footage or the street running?

Tom: Street running. It's outperforming the track version by about 15% on completion rate. The street running feels more accessible to the core buyer.

Priya: Makes sense. Any concerns heading into next week?

Tom: TikTok spend is a bit behind pace — we've spent $41,000 of the $180,000 monthly budget through day 8. I'd recommend increasing the daily budget cap by 20% this week to make sure we're not under-delivering.""",
    },
    {
        "transcript_id": "t_nike_002",
        "client": "Nike",
        "meeting_name": "Back to School Planning",
        "date": "2026-04-01",
        "participants": ["Tom (AM)", "Lisa (AM)", "Priya (Client)", "Ryan (Client)"],
        "text": """Lisa: Thanks for joining. We want to lock in the Back to School strategy early so we have enough lead time on creative development.

Ryan: What's the proposed timeline?

Tom: We're thinking a three-phase approach. Phase 1: Awareness, July 14 - July 28. Phase 2: Consideration, July 29 - August 11. Phase 3: Conversion push, August 12 - August 31.

Priya: What's the total budget you're working with?

Lisa: Nike approved $3.2M for the BTS push across all digital channels. We're recommending: Google 40%, Meta 35%, TikTok 15%, YouTube 10%.

Ryan: YouTube feels light at 10%. BTS is big for our Jordan line and YouTube has historically been strong for Jordan storytelling content.

Tom: Fair point. We could shift 5% from Meta to YouTube and land at Google 40%, Meta 30%, TikTok 15%, YouTube 15%. That gives YouTube $480K which is enough for a real presence.

Priya: What's the creative strategy for each phase?

Lisa: Phase 1 focuses on brand — 'Ready for Anything' campaign. Phase 2 shifts to product — specific Jordan and Air Max SKUs for BTS. Phase 3 goes hard on promotions and urgency. We'd want 10-12 video assets for YouTube, 6-8 TikTok-native videos, and a full static set for Google and Meta.

Ryan: We should brief the creative team by April 15 to stay on schedule.

Lisa: Agreed. I'll coordinate with your team to get on their calendar this week.""",
    },
    {
        "transcript_id": "t_nike_003",
        "client": "Nike",
        "meeting_name": "Women's Category Review",
        "date": "2026-03-24",
        "participants": ["Tom (AM)", "Priya (Client)"],
        "text": """Tom: I want to walk through the women's category performance in Q1 and talk about where we see opportunity in Q2.

Priya: Please.

Tom: Women's running drove 28% of total digital revenue in Q1 despite representing 22% of ad spend — so it's punching above its weight. The Invincible 3 in the women's colorway drove the most revenue, but the Vomero 17 women's launch in February was our highest-ROAS launch of the quarter at 4.1x.

Priya: What was different about Vomero 17's launch?

Tom: A few things. We had 90 days lead time instead of the usual 45, so we could build an audience pipeline through email capture and retargeting pools before launch day. We also partnered with six female running creators on TikTok — their content generated 2.4M organic views in the two weeks before launch, which gave us warm audiences to target.

Priya: That creator strategy is something we want to replicate. Who were the creators?

Tom: I'll get you the full list. They ranged from 50K to 800K followers — mid-tier mostly. The authenticity comes through better with mid-tier creators, and the cost is much lower than macro influencers.

Priya: For Q2 — we have the Air Zoom Pegasus 41 women's and the new React Infinity Run. Which do you think we should push harder?

Tom: Pegasus 41 has the broader appeal and the men's launch has already seeded awareness. I'd make Pegasus 41 women's the hero campaign and position React Infinity as the specialist choice for injury-prone runners — that's a passionate niche that converts well.""",
    },

    # ── HUGO BOSS ────────────────────────────────────────────────────────────
    {
        "transcript_id": "t_hugoboss_001",
        "client": "Hugo Boss",
        "meeting_name": "Spring Collection Launch Review",
        "date": "2026-04-06",
        "participants": ["Emma (AM)", "Klaus (Client)"],
        "text": """Emma: Klaus, let's review the Spring/Summer 2026 collection launch performance — we're now two weeks in.

Klaus: How are we tracking against targets?

Emma: Overall spend through April 5 is €94,200 against a €420,000 Q2 budget — pacing looks appropriate for the early phase. Revenue attribution from paid digital is €312,000, giving us a blended ROAS of 3.3x against a 2.5x target.

Klaus: That's strong. Which channels are leading?

Emma: Google Shopping is the standout — 4.8x ROAS on €28,000 spend. The BOSS suits and the HUGO casualwear are both performing well. On Meta, the video carousel format featuring the Spring lookbook is outperforming single-image ads by 40% on CTR. We're seeing €2.4 CPCs on branded terms, which is in line with last year.

Klaus: What about the new markets we're testing — the Netherlands and Belgium?

Emma: Netherlands is surprisingly strong — CPC 18% below Germany, similar conversion rate. Audience there has high purchase intent. Belgium is more mixed — French-speaking regions underperform Dutch-speaking regions meaningfully. We may want to run separate campaigns by language.

Klaus: Good catch on Belgium. Let's split those out. What's your read on the TikTok push for Spring?

Emma: TikTok is a different story. BOSS has strong organic presence — 890K followers — but converting that to paid performance has been harder. The polished content we normally run doesn't land as well on TikTok. I'd recommend producing 3-4 pieces of more native-feeling content before we scale spend there.

Klaus: We have a shoot in Milan next week. I can brief the photographer on capturing some TikTok-style footage.""",
    },
    {
        "transcript_id": "t_hugoboss_002",
        "client": "Hugo Boss",
        "meeting_name": "Digital Strategy Quarterly",
        "date": "2026-04-03",
        "participants": ["Emma (AM)", "Daniel (AM)", "Klaus (Client)", "Ingrid (Client)"],
        "text": """Daniel: Thanks for making time, Klaus and Ingrid. We want to align on digital strategy priorities for the rest of 2026.

Ingrid: We're particularly focused on the BOSS vs HUGO brand split — we want to make sure the positioning is distinct in paid channels.

Emma: That's something we've been working on. BOSS paid ads now skew 65% toward 35-54 age range targeting with premium lifestyle creative. HUGO is running younger — 22-34 — with a more streetwear/casual aesthetic. The performance data is validating the split. BOSS average order value from paid is €340 vs €195 for HUGO, which tracks with the positioning.

Daniel: We're also recommending a bigger investment in YouTube for the second half. Hugo Boss has incredible runway video content that's being underutilized. We're seeing competitor fashion brands achieve 3-4x ROAS on YouTube with long-form brand content.

Klaus: What does a YouTube-focused campaign look like operationally?

Emma: You'd need 2-3 hero videos (60-90 seconds) per brand per season, plus shorter cuts. We'd run TrueView campaigns targeting fashion enthusiasts and competitor brand audiences. We'd also deploy the content on YouTube Shorts in edited-down format to hit the mobile audience.

Ingrid: What's the minimum budget to do YouTube properly?

Daniel: We'd recommend at least €80,000 per brand per season for YouTube to see meaningful results — that's €160K total. Right now you're spending essentially nothing there.

Klaus: Let's model out a scenario where we shift 10% of Meta spend to YouTube and see what the projected impact looks like. Can you put that together?

Emma: Absolutely, I'll have a modeling doc to you by end of week.""",
    },
    {
        "transcript_id": "t_hugoboss_003",
        "client": "Hugo Boss",
        "meeting_name": "Performance Deep Dive",
        "date": "2026-03-20",
        "participants": ["Emma (AM)", "Klaus (Client)"],
        "text": """Emma: Klaus, I wanted to do a deeper dive into March performance before we close the month.

Klaus: Good timing, go ahead.

Emma: March was a strong month. Total digital revenue attributed to paid: €1.1M. Total spend: €310,000. ROAS: 3.55x. That's the best month we've had since November.

Klaus: What's driving that relative to February?

Emma: Three factors. First, the spring creative refresh landed well — higher CTRs across the board, especially on Facebook where the lookbook carousel format drove a 28% CTR improvement. Second, the Google Shopping feed update we did in late February — adding fabric and care instructions to the product titles — improved impression share by 15%. Third, we caught a good week in late March where competitor CPMs were elevated due to a Zara campaign, so our relative position improved.

Klaus: The feed update is interesting. That was a low-lift change that moved the needle.

Emma: Exactly. We have a few more feed optimizations queued up — structured sizing data, more specific color descriptions, better category taxonomy. I'd estimate another 8-12% impression share improvement from the remaining optimizations.

Klaus: Let's prioritize those. What's your view on where we're leaving money on the table?

Emma: Honestly, retargeting. Our retargeting pools are large — we have 180,000 users who visited product pages in the last 30 days — but we're only spending €12,000/month targeting them. The ROAS on retargeting when we've tested it properly is 5-6x. I'd recommend doubling retargeting budget in April.""",
    },
]

# ---------------------------------------------------------------------------
# SLACK MESSAGES
# ---------------------------------------------------------------------------

SLACK_MESSAGES = [
    # ── CASPER #casper-account ───────────────────────────────────────────────
    {"message_id": "m_casper_001", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-08T09:15:00", "text": "Morning team — quick heads up, Casper's Google CTR is showing improvement today. Looks like the new creative rotation is working."},
    {"message_id": "m_casper_002", "client": "Casper", "channel": "casper-account", "user": "marcus_am", "timestamp": "2026-04-08T09:22:00", "text": "Nice. What's the new CTR vs last week?"},
    {"message_id": "m_casper_003", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-08T09:28:00", "text": "4.6% vs 4.2% last Tuesday. Still below the 4.8% we had before the drop but trending right direction."},
    {"message_id": "m_casper_004", "client": "Casper", "channel": "casper-account", "user": "marcus_am", "timestamp": "2026-04-08T10:05:00", "text": "Jake just messaged — he wants to discuss increasing the TikTok budget by $5K for the rest of April. Says they've been happy with the early signals."},
    {"message_id": "m_casper_005", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-08T10:12:00", "text": "That works. We have room in the flex reserve. I'll put together a brief reallocation note for the weekly report."},
    {"message_id": "m_casper_006", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-07T16:30:00", "text": "End of day update: Facebook retargeting ROAS hit 3.4x today. Cart abandoner segment is really performing. Spend was $3,200 for the day."},
    {"message_id": "m_casper_007", "client": "Casper", "channel": "casper-account", "user": "ops_bot", "timestamp": "2026-04-07T17:00:00", "text": "[AUTOMATED] Daily spend report: Casper total $14,850. Google $6,200, Facebook $5,400, TikTok $2,100, Programmatic $1,150."},
    {"message_id": "m_casper_008", "client": "Casper", "channel": "casper-account", "user": "marcus_am", "timestamp": "2026-04-06T11:30:00", "text": "Heads up — Casper's main competitor Purple is running a heavy promo this week (25% off sitewide). We might see some CPC pressure on non-branded terms."},
    {"message_id": "m_casper_009", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-06T11:45:00", "text": "Good catch. I'm going to temporarily increase bids on the 'best mattress' and 'mattress reviews' terms by 15% to hold position."},
    {"message_id": "m_casper_010", "client": "Casper", "channel": "casper-account", "user": "marcus_am", "timestamp": "2026-04-06T11:50:00", "text": "Good call. Also worth adding a callout extension mentioning free returns — that's something Purple doesn't offer."},
    {"message_id": "m_casper_011", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-05T14:20:00", "text": "Weekly pacing check: $55,200 spent through end of day Sunday. $210K monthly budget. We're at 26.3% through day 5 of April — slightly ahead of pace but within normal range."},
    {"message_id": "m_casper_012", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-04T09:00:00", "text": "FYI — new creative assets approved by Casper yesterday. Uploading to Google and Facebook today. The lifestyle bedroom shots look really good."},
    {"message_id": "m_casper_013", "client": "Casper", "channel": "casper-account", "user": "ops_bot", "timestamp": "2026-04-03T17:00:00", "text": "[AUTOMATED] Weekly summary (Mar 31 - Apr 6): Casper impressions 4.2M, clicks 186K, avg CTR 4.4%, total spend $62,500, revenue $198,400, ROAS 3.17x."},
    {"message_id": "m_casper_014", "client": "Casper", "channel": "casper-account", "user": "marcus_am", "timestamp": "2026-04-02T15:00:00", "text": "Just off the Q2 budget call with Jake and Dana. They approved the recommended media split. I'll send the updated media plan by Thursday."},
    {"message_id": "m_casper_015", "client": "Casper", "channel": "casper-account", "user": "sarah_am", "timestamp": "2026-04-02T15:10:00", "text": "Great. TikTok going to 15% of budget is a real vote of confidence given how early we are. Let's not let them down."},

    # ── NIKE #nike-performance ───────────────────────────────────────────────
    {"message_id": "m_nike_001", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-08T08:45:00", "text": "Pegasus 41 launch is off to a strong start. Google Search CTR hit 6.2% overnight — that's way above our 4.5% benchmark."},
    {"message_id": "m_nike_002", "client": "Nike", "channel": "nike-performance", "user": "lisa_am", "timestamp": "2026-04-08T08:52:00", "text": "Nice. Priya is going to be happy. What's the CPC looking like?"},
    {"message_id": "m_nike_003", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-08T08:58:00", "text": "$2.18. Was $2.67 last week before the ad group restructure. Quality Score improvement is real."},
    {"message_id": "m_nike_004", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-08T13:30:00", "text": "TikTok is running behind pace. $41K spent of $180K budget through day 8. That's 22.8% vs the 25.8% we should be at. Recommend bumping daily cap 20%."},
    {"message_id": "m_nike_005", "client": "Nike", "channel": "nike-performance", "user": "lisa_am", "timestamp": "2026-04-08T13:38:00", "text": "Agreed. I'll make the change now. Ryan already approved any pacing adjustments under $10K/day in the SOW."},
    {"message_id": "m_nike_006", "client": "Nike", "channel": "nike-performance", "user": "ops_bot", "timestamp": "2026-04-08T17:00:00", "text": "[AUTOMATED] Daily spend report: Nike total $124,300. Google $52,100, Facebook/IG $43,800, TikTok $18,900, YouTube $9,500."},
    {"message_id": "m_nike_007", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-07T10:00:00", "text": "The 'Run Your World' :15 video is beating the :30 on completion rate — 68% vs 51%. Makes sense, the street running footage is more scroll-stopping. Should we allocate more budget to the shorter cut?"},
    {"message_id": "m_nike_008", "client": "Nike", "channel": "nike-performance", "user": "lisa_am", "timestamp": "2026-04-07T10:15:00", "text": "Yes. Let's shift to 70/30 in favor of :15. Keep the :30 running for YouTube where longer content is expected."},
    {"message_id": "m_nike_009", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-05T16:00:00", "text": "BTS planning call with Ryan and Priya confirmed for April 1. Preparing deck on three-phase approach — Awareness, Consideration, Conversion. $3.2M total budget up for discussion."},
    {"message_id": "m_nike_010", "client": "Nike", "channel": "nike-performance", "user": "lisa_am", "timestamp": "2026-04-05T16:10:00", "text": "One thing to flag in that call — Ryan mentioned YouTube for Jordan storytelling. We should have a counter-proposal ready if they want to move budget from Meta to YouTube."},
    {"message_id": "m_nike_011", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-04T11:00:00", "text": "Women's category ROAS is tracking at 3.6x for Q2 so far. The Pegasus 41 women's launch plan is looking solid — creator outreach done, 6 confirmed partnerships."},
    {"message_id": "m_nike_012", "client": "Nike", "channel": "nike-performance", "user": "lisa_am", "timestamp": "2026-04-03T09:30:00", "text": "Reminder: Priya wants the creator list for the Vomero 17 women's launch by Friday. Tom, can you compile that?"},
    {"message_id": "m_nike_013", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-03T09:45:00", "text": "On it. Will have by Thursday EOD."},
    {"message_id": "m_nike_014", "client": "Nike", "channel": "nike-performance", "user": "ops_bot", "timestamp": "2026-04-03T17:00:00", "text": "[AUTOMATED] Weekly summary (Mar 31 - Apr 6): Nike impressions 18.4M, clicks 612K, avg CTR 3.3%, total spend $412,000, revenue $1.24M, blended ROAS 3.0x."},
    {"message_id": "m_nike_015", "client": "Nike", "channel": "nike-performance", "user": "tom_am", "timestamp": "2026-04-02T14:00:00", "text": "Quick note: non-branded running terms CPC dropped from $2.67 to $2.18 after ad group restructure. That's a meaningful efficiency gain. Good call on the reorganization, Lisa."},

    # ── HUGO BOSS #hugoboss-digital ──────────────────────────────────────────
    {"message_id": "m_hugoboss_001", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-08T09:00:00", "text": "Spring collection campaign entering week 3. Google Shopping ROAS held at 4.8x yesterday. BOSS suits continue to drive the most revenue volume."},
    {"message_id": "m_hugoboss_002", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-08T09:10:00", "text": "Netherlands performance continues to impress — CPC 18% below Germany. Klaus is going to ask about expanding budget there, I'm sure."},
    {"message_id": "m_hugoboss_003", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-08T09:18:00", "text": "Agreed. Let's have a Netherlands expansion brief ready for the next call. Also need to split Belgium by language — French vs Dutch is showing different performance."},
    {"message_id": "m_hugoboss_004", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-07T15:30:00", "text": "Klaus wants a YouTube scenario model — what if we shift 10% of Meta to YouTube? Need to show projected impact. Emma can you take this?"},
    {"message_id": "m_hugoboss_005", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-07T15:40:00", "text": "Yes, will have by Friday. Will model out ROAS assumptions based on competitive fashion brand benchmarks and our own YouTube test data from Q4."},
    {"message_id": "m_hugoboss_006", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "ops_bot", "timestamp": "2026-04-07T17:00:00", "text": "[AUTOMATED] Daily spend report: Hugo Boss total €29,400. Google Shopping €11,200, Facebook/IG €10,800, Programmatic €4,900, YouTube €2,500."},
    {"message_id": "m_hugoboss_007", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-06T11:00:00", "text": "Klaus confirmed there's a Milan shoot next week — he's briefing the photographer on capturing TikTok-style footage. This is great, it'll give us more native content to test."},
    {"message_id": "m_hugoboss_008", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-06T11:15:00", "text": "Good. BOSS organic TikTok has 890K followers — we should be able to drive serious reach once we have content that actually works in the format."},
    {"message_id": "m_hugoboss_009", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-05T14:00:00", "text": "Q2 pacing update: €94,200 spent against €420K budget through April 5. ROAS tracking at 3.3x vs 2.5x target. Very healthy start to the quarter."},
    {"message_id": "m_hugoboss_010", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-05T14:10:00", "text": "3.3x vs 2.5x target is great. The spring lookbook creative is clearly working. Video carousel is up 40% CTR vs single image."},
    {"message_id": "m_hugoboss_011", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-04T10:00:00", "text": "Retargeting proposal sent to Klaus — recommending double the budget from €12K to €24K/month. We have 180K product page visitors in the 30-day window and we're barely touching them."},
    {"message_id": "m_hugoboss_012", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-04T10:15:00", "text": "5-6x ROAS on retargeting is hard to argue with. I expect Klaus to approve this pretty quickly."},
    {"message_id": "m_hugoboss_013", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "ops_bot", "timestamp": "2026-04-03T17:00:00", "text": "[AUTOMATED] Weekly summary (Mar 31 - Apr 6): Hugo Boss impressions 6.1M, clicks 198K, avg CTR 3.2%, total spend €94,200, revenue €310,400, ROAS 3.3x."},
    {"message_id": "m_hugoboss_014", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-02T09:00:00", "text": "March final numbers in: €1.1M digital revenue, €310K spend, 3.55x ROAS. Best month since November. Spring creative refresh and feed optimization both contributed."},
    {"message_id": "m_hugoboss_015", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-02T09:10:00", "text": "3.55x is excellent. The remaining feed optimizations Emma has queued up could add another 8-12% impression share. Good Q2 setup."},
    {"message_id": "m_hugoboss_016", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "emma_am", "timestamp": "2026-04-01T16:00:00", "text": "Reminder: BOSS vs HUGO brand split is working well in paid — BOSS targeting 35-54, AOV €340. HUGO targeting 22-34, AOV €195. Keeping ad creative and audiences separate is key."},
    {"message_id": "m_hugoboss_017", "client": "Hugo Boss", "channel": "hugoboss-digital", "user": "daniel_am", "timestamp": "2026-04-01T16:15:00", "text": "Ingrid specifically mentioned she wants the brand split to be maintained. Let's make sure that's called out clearly in the quarterly review deck."},
]


def main():
    out_transcripts = OUT_DIR / "transcripts.json"
    out_slack = OUT_DIR / "slack_messages.json"

    with open(out_transcripts, "w") as f:
        json.dump(TRANSCRIPTS, f, indent=2)
    print(f"Wrote {len(TRANSCRIPTS)} transcripts to {out_transcripts}")

    with open(out_slack, "w") as f:
        json.dump(SLACK_MESSAGES, f, indent=2)
    print(f"Wrote {len(SLACK_MESSAGES)} slack messages to {out_slack}")


if __name__ == "__main__":
    main()
