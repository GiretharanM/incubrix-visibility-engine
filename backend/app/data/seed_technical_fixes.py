TECHNICAL_ISSUES_DATA = [
    {
        "affected_url": "https://incubrix.com/llms.txt",
        "category": "crawlability",
        "severity": "critical",
        "issue_title": "Missing llms.txt File for Generative AI Engine Optimization (AEO)",
        "observed_problem": "HTTP GET to https://incubrix.com/llms.txt returns 404 NOT_FOUND. AI search engines (Perplexity, ChatGPT Search, Claude) cannot efficiently parse the product capabilities, pricing, and architecture.",
        "evidence": "HTTP 404 response on https://incubrix.com/llms.txt with Cloudflare/Vercel error header.",
        "recommended_solution": "Deploy a standardized /llms.txt markdown file at the root domain detailing IncuBrix Creator Studio capabilities, pricing, and canonical URLs.",
        "ready_to_paste_code": """# IncuBrix Creator Studio

> Create With Purpose. Publish Without Limits.

IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform — then publishes and tracks it all from one screen.

## Core Capabilities
- **AI Video Repurposing**: Converts long-form YouTube videos and podcasts into 9:16 vertical shorts.
- **Dynamic Captions**: Generates synchronized, word-level highlighted subtitles.
- **AI Voiceovers**: Studio-grade multi-lingual voice synthesis.
- **Multi-Platform Publishing**: Direct one-screen scheduling to TikTok, Instagram Reels, and YouTube Shorts.
- **Unified Analytics**: Cross-network performance tracking.

## Pricing Tiers
- Free Starter Tier: Basic clipping and caption generation.
- Pro Creator Tier: Unlimited multi-platform scheduling and AI voiceovers.

## Canonical Documentation
- Overview: https://incubrix.com/
- How it Works: https://incubrix.com/how-it-works
- Pricing: https://incubrix.com/pricing
- FAQ: https://incubrix.com/faq
""",
        "validation_method": "HTTP GET request to https://incubrix.com/llms.txt expecting HTTP 200 with text/markdown",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "structured_data",
        "severity": "critical",
        "issue_title": "Missing Organization & SoftwareApplication JSON-LD Schema on Homepage",
        "observed_problem": "The homepage does not emit structured application/ld+json for the Organization or SoftwareApplication entities, preventing Google Knowledge Graph and AI search engines from recognizing IncuBrix as a verified software provider.",
        "evidence": "0 script tags with type application/ld+json found on homepage document.",
        "recommended_solution": "Add valid JSON-LD schema defining IncuBrix as an Organization and SoftwareApplication.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://incubrix.com/#organization",
      "name": "IncuBrix",
      "url": "https://incubrix.com",
      "logo": "https://incubrix.com/logo.png",
      "description": "Creator studio unifying AI video repurposing, captions, scheduling, and analytics.",
      "sameAs": [
        "https://twitter.com/incubrix",
        "https://linkedin.com/company/incubrix",
        "https://youtube.com/@incubrix"
      ]
    },
    {
      "@type": "SoftwareApplication",
      "@id": "https://incubrix.com/#software",
      "name": "IncuBrix Creator Studio",
      "applicationCategory": "MultimediaApplication",
      "operatingSystem": "All modern web browsers",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }
    }
  ]
}
</script>""",
        "validation_method": "Validate via Google Rich Results Test API & Schema Validator",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/faq",
        "category": "structured_data",
        "severity": "high",
        "issue_title": "Missing FAQPage Schema Markup on FAQ URL",
        "observed_problem": "The FAQ page contains valuable answers to common creator questions, but lacks FAQPage schema markup, preventing rich accordion snippets in Google search results.",
        "evidence": "No @type: FAQPage schema detected in page source.",
        "recommended_solution": "Inject FAQPage JSON-LD schema matching the visible questions and answers.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How does IncuBrix help content creators?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "IncuBrix turns one piece of content into clips, captions, voiceovers, and posts for every platform, and allows you to publish and track them all from one screen."
      }
    },
    {
      "@type": "Question",
      "name": "Does IncuBrix support automated social media publishing?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, IncuBrix integrates directly with YouTube, TikTok, Instagram, and LinkedIn so you can schedule and publish directly without downloading files."
      }
    }
  ]
}
</script>""",
        "validation_method": "Google Rich Results Test inspection on /faq",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/pricing",
        "category": "metadata",
        "severity": "high",
        "issue_title": "Pricing Page Meta Description Missing Clear Pricing Thresholds",
        "observed_problem": "The meta description on /pricing is generic and does not inform search engine users about whether there is a free tier or what the entry cost is, suppressing CTR.",
        "evidence": "Meta description lacks price anchors and clear value proposition.",
        "recommended_solution": "Update the meta description to include free start tier and clear target audience callout.",
        "ready_to_paste_code": """<meta name="description" content="Explore IncuBrix Creator Studio plans and pricing. Start free to turn videos into clips, captions, and posts, or upgrade for unlimited multi-platform publishing.">""",
        "validation_method": "SERP snippet simulator and SERP CTR tracking",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/how-it-works",
        "category": "structured_data",
        "severity": "high",
        "issue_title": "Missing HowTo Structured Data on Workflow Explanation Page",
        "observed_problem": "The /how-it-works page describes a sequential step-by-step process (Record, Clip, Caption, Publish) but lacks schema.org/HowTo schema.",
        "evidence": "No HowTo schema elements found in DOM.",
        "recommended_solution": "Add HowTo JSON-LD schema with clear step names and text.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How IncuBrix Works: From Idea to Multi-Platform Impact",
  "description": "The four-step automated workflow to turn one video into dozens of social posts.",
  "step": [
    {"@type": "HowToStep", "name": "Upload Media", "text": "Upload raw podcast, webinar, or long-form video."},
    {"@type": "HowToStep", "name": "AI Clipping & Captions", "text": "AI extracts viral moments and adds word-level subtitles."},
    {"@type": "HowToStep", "name": "Review & Customize", "text": "Adjust aspect ratios, branding, and voiceovers."},
    {"@type": "HowToStep", "name": "One-Screen Publishing", "text": "Schedule directly to Shorts, TikTok, and Reels."}
  ]
}
</script>""",
        "validation_method": "Schema.org validator on /how-it-works",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "metadata",
        "severity": "medium",
        "issue_title": "Open Graph Image Missing Explicit Width and Height Dimensions",
        "observed_problem": "og:image is specified but lacks og:image:width, og:image:height, and og:image:alt, causing social media preview rendering delays on WhatsApp and LinkedIn.",
        "evidence": "Missing og:image:width and og:image:height tags in head.",
        "recommended_solution": "Include standard 1200x630 dimensions and descriptive alt text.",
        "ready_to_paste_code": """<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="IncuBrix Creator Studio - Turn One Content into Clips, Captions, and Posts">""",
        "validation_method": "Facebook Sharing Debugger & LinkedIn Post Inspector",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "metadata",
        "severity": "medium",
        "issue_title": "Twitter Card Tags Lack Summary_Large_Image Declaration",
        "observed_problem": "Homepage uses default small summary card or incomplete Twitter tags, resulting in low click-through rates on X/Twitter feeds.",
        "evidence": "twitter:card is either missing or set to summary instead of summary_large_image.",
        "recommended_solution": "Deploy twitter:card as summary_large_image with twitter:site and twitter:creator.",
        "ready_to_paste_code": """<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@incubrix">
<meta name="twitter:title" content="IncuBrix | Create With Purpose. Publish Without Limits.">
<meta name="twitter:description" content="IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform | then publishes and tracks it all from one screen.">
<meta name="twitter:image" content="https://incubrix.com/og-image.jpg">""",
        "validation_method": "Twitter/X Card Validator inspection",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/sitemap.xml",
        "category": "crawlability",
        "severity": "medium",
        "issue_title": "Sitemap Missing lastmod Timestamps on Core URLs",
        "observed_problem": "The 13 URLs listed in /sitemap.xml only include <loc> and <changefreq> but omit <lastmod>, which search engines rely on to prioritize crawling updated content.",
        "evidence": "/sitemap.xml inspection shows missing <lastmod> nodes across all entries.",
        "recommended_solution": "Add ISO 8601 UTC date timestamps (<lastmod>2026-10-21</lastmod>) to all URLs in sitemap generator.",
        "ready_to_paste_code": """<url>
  <loc>https://incubrix.com/</loc>
  <lastmod>2026-10-21T00:00:00Z</lastmod>
  <changefreq>weekly</changefreq>
  <priority>1.0</priority>
</url>""",
        "validation_method": "XML parser validation of sitemap.xml",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/about",
        "category": "structured_data",
        "severity": "medium",
        "issue_title": "Missing AboutPage Schema and Founder Entity Linking",
        "observed_problem": "The /about page lacks AboutPage schema and does not link founders to Wikidata or LinkedIn profiles, weakening Google E-E-A-T signals.",
        "evidence": "No AboutPage schema found.",
        "recommended_solution": "Implement AboutPage schema linking to corporate mission and leadership profiles.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "mainEntity": {
    "@type": "Organization",
    "name": "IncuBrix",
    "url": "https://incubrix.com",
    "foundingLocation": "United States"
  }
}
</script>""",
        "validation_method": "Schema.org validator",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "content",
        "severity": "medium",
        "issue_title": "Missing Descriptive Alt Text on Product Feature Screenshots",
        "observed_problem": "Multiple image tags across the homepage and feature previews omit descriptive alt attributes, impairing accessibility and Google Image search visibility.",
        "evidence": "Images with empty or missing alt attributes identified.",
        "recommended_solution": "Provide keyword-rich, descriptive alt text for all interface screenshots.",
        "ready_to_paste_code": """<!-- Before -->
<img src="/img/dashboard-preview.png">

<!-- After -->
<img src="/img/dashboard-preview.png" alt="IncuBrix Creator Studio multi-platform scheduling dashboard interface">""",
        "validation_method": "HTML accessibility linter & DOM tree audit",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/pricing",
        "category": "structured_data",
        "severity": "high",
        "issue_title": "Missing Product and Offer Structured Data on Pricing Page",
        "observed_problem": "Search engines cannot display pricing ranges or currency information in SERPs because the /pricing page does not define schema.org/Product with Offer catalog.",
        "evidence": "No Product or Offer JSON-LD schema on /pricing.",
        "recommended_solution": "Deploy Product schema with AggregateOffer or distinct plan tiers.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "IncuBrix Creator Studio",
  "description": "All-in-one AI video repurposing and multi-platform publishing platform.",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "0",
    "highPrice": "49",
    "priceCurrency": "USD",
    "offerCount": "3"
  }
}
</script>""",
        "validation_method": "Rich Results Test for Product Rich Snippets",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "performance",
        "severity": "medium",
        "issue_title": "Missing Preconnect Resource Hints for Web Fonts and CDN Assets",
        "observed_problem": "Web fonts and external CDN scripts are loaded without <link rel='preconnect'>, adding 150-250ms of DNS resolution latency on initial mobile page loads.",
        "evidence": "Waterfall analysis reveals sequential DNS resolution for external font origins.",
        "recommended_solution": "Add preconnect link headers in the <head> block.",
        "ready_to_paste_code": """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>""",
        "validation_method": "Lighthouse Performance audit preconnect check",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/waitlist",
        "category": "metadata",
        "severity": "medium",
        "issue_title": "Waitlist Page Title Missing Primary Brand Benefit",
        "observed_problem": "Page title on /waitlist is simply 'Waitlist | IncuBrix', failing to convey what the user is signing up for in search snippets.",
        "evidence": "Page title: 'Waitlist | IncuBrix'.",
        "recommended_solution": "Update title to include product benefit: 'Join the IncuBrix Creator Studio Waitlist | Early Access'.",
        "ready_to_paste_code": """<title>Join the IncuBrix Creator Studio Waitlist | Early Access</title>""",
        "validation_method": "Live HTML inspection",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/manifesto",
        "category": "crawlability",
        "severity": "low",
        "issue_title": "Manifesto Page Lacks Clear Internal Navigation Links to Core Product",
        "observed_problem": "The /manifesto page contains engaging storytelling but has limited internal links pointing to /how-it-works and /pricing, trapping internal link equity.",
        "evidence": "Only navigation bar links exist; body text has 0 internal contextual links.",
        "recommended_solution": "Add contextual anchor links to /how-it-works and /pricing in the manifesto conclusion.",
        "ready_to_paste_code": """<p class="mt-8 text-center">
  Ready to create with purpose? Discover <a href="/how-it-works" class="underline text-blue-600 font-semibold">how IncuBrix works</a> or <a href="/pricing" class="underline text-blue-600 font-semibold">explore our creator plans</a>.
</p>""",
        "validation_method": "Internal link crawler equity check",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "security",
        "severity": "high",
        "issue_title": "Content-Security-Policy Missing Explicit frame-ancestors Directive",
        "observed_problem": "The site does not specify frame-ancestors in its Content-Security-Policy header or X-Frame-Options: SAMEORIGIN, exposing the interface to potential clickjacking.",
        "evidence": "Header audit shows absence of frame-ancestors directive.",
        "recommended_solution": "Configure server or Cloudflare/Vercel headers to set Content-Security-Policy: frame-ancestors 'self'.",
        "ready_to_paste_code": """# Vercel vercel.json headers config
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Content-Security-Policy", "value": "frame-ancestors 'self';" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}""",
        "validation_method": "HTTP response headers check",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/terms",
        "category": "metadata",
        "severity": "low",
        "issue_title": "Legal Pages Missing robots noindex Directive Consideration",
        "observed_problem": "Terms and Privacy pages are indexed with default priority, consuming crawl budget on boilerplate legal documents rather than core product landing pages.",
        "evidence": "Both /terms and /privacy have weekly changefreq in sitemap.xml without prioritization flags.",
        "recommended_solution": "Lower priority to 0.2 in sitemap.xml and ensure canonical points to root legal version.",
        "ready_to_paste_code": """<url>
  <loc>https://incubrix.com/terms</loc>
  <changefreq>monthly</changefreq>
  <priority>0.2</priority>
</url>""",
        "validation_method": "Sitemap priority inspection",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "mobile",
        "severity": "medium",
        "issue_title": "Touch Target Sizes Below 48px on Mobile Navigation Elements",
        "observed_problem": "Several footer and submenu links have touch targets smaller than 44x44px, causing minor mobile usability warnings in Google Search Console.",
        "evidence": "Touch target warnings on 3 mobile footer links.",
        "recommended_solution": "Add py-2 and min-h-[44px] padding classes to navigation anchor tags.",
        "ready_to_paste_code": """<!-- Tailwind CSS adjustment -->
<a href="/faq" class="inline-flex items-center min-h-[44px] py-2 px-3 text-sm text-neutral-600 hover:text-neutral-900">FAQ</a>""",
        "validation_method": "Google Mobile-Friendly Test & Chrome DevTools Touch Target Audit",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/team",
        "category": "structured_data",
        "severity": "medium",
        "issue_title": "Missing Person Schema on Leadership Team Profiles",
        "observed_problem": "The team page lists creators and engineers but lacks Person schema with sameAs links to verified author credentials, weakening E-E-A-T entity resolution.",
        "evidence": "No Person schema entities found on /team.",
        "recommended_solution": "Implement Person schema with jobTitle and sameAs links for key team members.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "IncuBrix Team Member",
  "jobTitle": "Co-Founder",
  "worksFor": {
    "@type": "Organization",
    "name": "IncuBrix"
  }
}
</script>""",
        "validation_method": "Schema.org validator on /team",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/",
        "category": "content",
        "severity": "high",
        "issue_title": "Missing Direct Answer Sentence for AEO on Primary Value Proposition",
        "observed_problem": "The hero section uses poetic branding ('Create With Purpose. Publish Without Limits.') but does not immediately provide a clear, factual definition sentence that AI search engines can cite directly.",
        "evidence": "Perplexity and ChatGPT struggle to describe IncuBrix in 1 concise factual sentence.",
        "recommended_solution": "Add an explicit definition sentence directly under the hero headline.",
        "ready_to_paste_code": """<p class="text-xl text-neutral-700 font-medium max-w-3xl mx-auto">
  IncuBrix is an all-in-one AI content platform that automatically repurposes long-form video into clips, captions, and voiceovers, and publishes them across all social platforms from one screen.
</p>""",
        "validation_method": "AI assistant brand mention test on 'What is IncuBrix?'",
        "validation_status": "open"
    },
    {
        "affected_url": "https://incubrix.com/careers",
        "category": "metadata",
        "severity": "low",
        "issue_title": "Careers Page Missing JobPosting Structured Data",
        "observed_problem": "Open roles on /careers are rendered as static text without schema.org/JobPosting markup, preventing them from appearing in Google for Jobs search cards.",
        "evidence": "Missing JobPosting schema.",
        "recommended_solution": "Wrap active roles with JobPosting schema including hiringOrganization and title.",
        "ready_to_paste_code": """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "JobPosting",
  "title": "Growth Engineer",
  "hiringOrganization": {
    "@type": "Organization",
    "name": "IncuBrix",
    "sameAs": "https://incubrix.com"
  },
  "jobLocationType": "TELECOMMUTE"
}
</script>""",
        "validation_method": "Google for Jobs schema test",
        "validation_status": "open"
    }
]
