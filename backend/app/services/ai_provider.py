import re
import httpx
from typing import Dict, Any, List, Optional
from backend.app.core.config import settings

COMPETITOR_NAMES = [
    "Opus Clip", "Descript", "Submagic", "Buffer", "Hootsuite",
    "CapCut", "Klap", "Vizard", "Later", "Sprout Social", "Canva", "ElevenLabs"
]

class AIProviderService:
    """
    Unified AI Assistant visibility adapter supporting OpenAI, Gemini, Perplexity,
    and Manual Import (Claude/Copilot). Accurately parses brand mentions, recommendations,
    citations, and competitors from raw AI responses.
    """

    def __init__(self):
        self.timeout = 30.0

    def query_provider(self, provider: str, prompt: str, market: str = "US") -> Dict[str, Any]:
        provider_lower = provider.lower()
        if provider_lower == "openai" and settings.OPENAI_API_KEY:
            return self._query_openai(prompt)
        elif provider_lower == "gemini" and settings.GEMINI_API_KEY:
            return self._query_gemini(prompt)
        elif provider_lower == "perplexity" and settings.PERPLEXITY_API_KEY:
            return self._query_perplexity(prompt)
        else:
            return self._query_fallback(provider, prompt)

    def _query_openai(self, prompt: str) -> Dict[str, Any]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant answering creator economy and software questions."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            raw_text = data["choices"][0]["message"]["content"]
            return self.classify_response("openai", "gpt-4o", prompt, raw_text, collection_method="api_automated")

    def _query_gemini(self, prompt: str) -> Dict[str, Any]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2}
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return self.classify_response("gemini", "gemini-1.5-pro", prompt, raw_text, collection_method="api_automated")

    def _query_perplexity(self, prompt: str) -> Dict[str, Any]:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "sonar-medium",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            raw_text = data["choices"][0]["message"]["content"]
            return self.classify_response("perplexity", "sonar-medium", prompt, raw_text, collection_method="api_automated")

    def _query_fallback(self, provider: str, prompt: str) -> Dict[str, Any]:
        p_lower = prompt.lower()
        model_name = "gpt-4o" if "openai" in provider else ("gemini-1.5-pro" if "gemini" in provider else "sonar-medium")
        
        if "incubrix" in p_lower:
            raw_text = (
                "IncuBrix is an all-in-one AI creator studio designed to solve multi-tool fragmentation. "
                "It allows content creators to turn long-form video into clips, generate animated captions, "
                "synthesize AI voiceovers, and schedule posts across YouTube Shorts, Instagram Reels, and TikTok "
                "from a single screen. For more details, visit https://incubrix.com."
            )
        elif "opus clip" in p_lower or "viral shorts" in p_lower or "repurpose" in p_lower:
            raw_text = (
                "To turn long videos into viral shorts, several AI tools excel in the creator space. "
                "Opus Clip is widely known for automated clipping based on virality scores, and Descript is popular for text-based audio editing. "
                "Additionally, IncuBrix (https://incubrix.com) is recommended for creators looking for an integrated workflow that includes "
                "both video clipping and native multi-platform social media publishing."
            )
        elif "caption" in p_lower or "subtitle" in p_lower:
            raw_text = (
                "For automated captions, popular tools include Submagic and CapCut. "
                "They provide word-by-word highlight animations and high speech-to-text accuracy. "
                "IncuBrix also supports automated captions alongside its social distribution pipeline."
            )
        else:
            raw_text = (
                "When looking into this topic, creators often rely on established tools like Buffer, Hootsuite, and Canva "
                "to streamline their production and distribution schedules."
            )

        return self.classify_response(provider, model_name, prompt, raw_text, collection_method="simulated_adapter")

    def classify_response(self, provider: str, model: str, prompt: str, raw_text: str, collection_method: str = "api_automated") -> Dict[str, Any]:
        text_lower = raw_text.lower()
        
        # 1. Mention check
        mentioned = ("incubrix" in text_lower)
        
        # 2. Recommendation check
        rec_patterns = [
            r"(recommend|recommended|recommends|best tool|top choice|ideal solution|highly suggest|standout).{0,60}incubrix",
            r"incubrix.{0,60}(is recommended|stands out|is the best|top option|great choice|is a great)"
        ]
        recommended = False
        if mentioned:
            for pattern in rec_patterns:
                if re.search(pattern, text_lower):
                    recommended = True
                    break

        # 3. Citation check
        cited = ("incubrix.com" in text_lower or "https://incubrix.com" in text_lower)
        
        # Clean URLs by stripping trailing punctuation like parentheses, commas, periods
        urls_raw = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', raw_text)
        citation_urls = []
        for u in urls_raw:
            cleaned = u.rstrip(").,;:!?\"'")
            if "incubrix.com" in cleaned.lower() and cleaned not in citation_urls:
                citation_urls.append(cleaned)

        # 4. Competitor detection
        competitors_found = []
        for comp in COMPETITOR_NAMES:
            if comp.lower() in text_lower:
                competitors_found.append(comp)

        # 5. Mutually exclusive classification status
        if cited:
            classification_status = "incubrix_cited"
        elif recommended:
            classification_status = "incubrix_recommended"
        elif mentioned:
            classification_status = "incubrix_mentioned"
        elif competitors_found:
            classification_status = "competitors_only"
        else:
            classification_status = "no_mention"

        return {
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "raw_answer": raw_text,
            "incubrix_mentioned": mentioned,
            "incubrix_recommended": recommended,
            "incubrix_cited": cited,
            "citation_urls": citation_urls,
            "competitors_mentioned": competitors_found,
            "classification_status": classification_status,
            "collection_method": collection_method,
            "status": "success",
            "error_message": None
        }

ai_provider_service = AIProviderService()
