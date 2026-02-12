#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import sys
import os
import time

# ==============================================================================
# GPTZERO PREMIUM SCANNER (Termux/Ubuntu) - FULLY FIXED v2
#
# Fixes applied:
#   1. AI Scan      -> Human-readable verdict with per-sentence breakdown
#   2. Plagiarism   -> Polls for results instead of just returning poll URL
#   3. Hallucinations -> Properly handles SSE streams with :dummy keep-alive
#   4. Writing Feedback -> Properly parses SSE/streaming responses
#   5. AI Reviewer  -> Fixed payload (removed invalid template ID)
# ==============================================================================

COOKIE = "_ca_device_id=ca_2d26b340-94a6-410f-8b9e-b605ab42fca2; _gcl_au=1.1.2113670099.1770888129; AMP_MKTG_8f1ede8e9c=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; _fbp=fb.1.1770888130058.552936954255985546; _hjSession_3701535=eyJpZCI6ImFjN2JkNDdhLTI3Y2QtNDIzOC1hNGRjLTA3OGE2YmVlNDE1YSIsImMiOjE3NzA4ODgxMzAyNzcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; hubspotutk=319ed4e4fc725e3e8a38082735d0443c; _ga=GA1.1.1299419126.1770888135; _hjSessionUser_3701535=eyJpZCI6IjFjMWI3MjdlLWI4MWYtNTdmNC1iNGE2LTkxY2M3YzQ2ZjNiZCIsImNyZWF0ZWQiOjE3NzA4ODgxMzAyNzAsImV4aXN0aW5nIjp0cnVlfQ==; accessToken4=eyJhbGciOiJIUzI1NiIsImtpZCI6IkxQUGtRbDRKRlQvcmY5VkoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2x5ZHFoZ2R6aHZzcWxjb2JkZnhpLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJkY2VjNjYyNC01ZDAwLTQ3MzUtODAyZC1iZGFjOWY1MjMxYWMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzcxNDkzMDg1LCJpYXQiOjE3NzA4ODgzMTgsImVtYWlsIjoiYWlkZXRlY3RvcjkxMkBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6Imdvb2dsZSIsInByb3ZpZGVycyI6WyJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0ppd1o2eUtIdVdfMFM0RnZHUS16aF9xZDY2UUZDaUtuYllYb3NSbDY2OVlhSTFNdz1zOTYtYyIsImVtYWlsIjoiYWlkZXRlY3RvcjkxMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiQUkgRGV0ZWN0b3IiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYW1lIjoiQUkgRGV0ZWN0b3IiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKaXdaNnlLSHVXXzBTNEZ2R1EtemhfcWQ2NlFGQ2lLbmJZWG9zUmw2NjlZYUkxTXc9czk2LWMiLCJwcm92aWRlcl9pZCI6IjEwMjgyNTI5NjEwMzAwNjkwMjAyNSIsInN1YiI6IjEwMjgyNTI5NjEwMzAwNjkwMjAyNSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6Im9hdXRoIiwidGltZXN0YW1wIjoxNzcwODg4MzE4fV0sInNlc3Npb25faWQiOiI1OTUxZmI1NS0zZDVkLTRhY2EtOWQ5OS1mNjEwNmMyOWFiODEiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.WCrHS4d-wRcPdNS5RpUOlCMP2rBaGFgeYFLdiW89Rnk; plan=Premium; __hstc=72891980.319ed4e4fc725e3e8a38082735d0443c.1770888131569.1770888131569.1770891687678.2; __hssrc=1; _ga_Z6QQHT52V9=GS2.1.s1770888135$o1$g1$t1770895380$j60$l0$h0; __hssc=72891980.12.1770891687678; AMP_8f1ede8e9c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJudWxsJTIyJTJDJTIydXNlcklkJTIyJTNBJTIyZGNlYzY2MjQtNWQwMC00NzM1LTgwMmQtYmRhYzlmNTIzMWFjJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc3MDg4ODEyOTg2NSUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NzA4OTU0MTI1NzElMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTEzMyUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMjglN0Q="

HEADERS = {
    "authority": "api.gptzero.me",
    "accept": "*/*",
    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "cookie": COOKIE,
    "origin": "https://app.gptzero.me",
    "referer": "https://app.gptzero.me/",
    "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "x-gptzero-platform": "webapp"
}

# GET headers (no content-type needed)
GET_HEADERS = {k: v for k, v in HEADERS.items() if k != "content-type"}


# ==============================================================================
# RESPONSE PARSING
# ==============================================================================

def parse_api_response(resp_text):
    """
    Robust parser that handles:
    - Regular JSON
    - SSE with data: prefix lines
    - SSE with :comment keep-alive lines (like :dummy)
    - NDJSON (newline-delimited JSON)
    - JSON with BOM or leading whitespace
    """
    text = resp_text.strip()

    # Remove BOM if present
    if text.startswith('\ufeff'):
        text = text[1:]

    # Remove null bytes
    text = text.replace('\x00', '')

    # Try plain JSON first
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass

    # Parse as SSE (handles :dummy comments and data: lines)
    collected = []
    has_sse_markers = False
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith(':'):
            has_sse_markers = True
            continue  # SSE comment (:dummy keep-alive, etc.)
        if line.startswith('data:'):
            has_sse_markers = True
            data_str = line[5:].strip()
            if data_str and data_str != '[DONE]':
                try:
                    collected.append(json.loads(data_str))
                except (json.JSONDecodeError, ValueError):
                    pass

    if collected:
        return collected if len(collected) > 1 else collected[0]

    # Try NDJSON (multiple JSON objects separated by newlines)
    for line in text.split('\n'):
        line = line.strip()
        if line:
            try:
                collected.append(json.loads(line))
            except (json.JSONDecodeError, ValueError):
                pass

    if collected:
        return collected if len(collected) > 1 else collected[0]

    # Try finding JSON object in the text (might have prefix/suffix junk)
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(text[first_brace:last_brace + 1])
        except (json.JSONDecodeError, ValueError):
            pass

    return {"raw_response": text[:2000]}


# ==============================================================================
# API CALL FUNCTIONS
# ==============================================================================

def api_call(endpoint, payload):
    """Standard POST request with robust response parsing"""
    url = f"https://api.gptzero.me{endpoint}"
    data_bytes = json.dumps(payload).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data_bytes, headers=HEADERS, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            resp_text = response.read().decode('utf-8')
            return parse_api_response(resp_text)

    except urllib.error.HTTPError as e:
        print(f"\n[!] HTTP Error: {e.code} on {endpoint}")
        try:
            print(f"    Details: {e.read().decode('utf-8')[:500]}")
        except:
            pass
        return None
    except Exception as e:
        print(f"\n[!] Connection Error on {endpoint}: {e}")
        return None


def api_get(url):
    """GET request for polling endpoints"""
    try:
        req = urllib.request.Request(url, headers=GET_HEADERS, method='GET')
        with urllib.request.urlopen(req, timeout=30) as response:
            resp_text = response.read().decode('utf-8')
            return parse_api_response(resp_text)
    except urllib.error.HTTPError as e:
        print(f"\n[!] HTTP Error: {e.code} on GET")
        try:
            print(f"    Details: {e.read().decode('utf-8')[:500]}")
        except:
            pass
        return None
    except Exception as e:
        print(f"\n[!] Connection Error: {e}")
        return None


def api_call_stream(endpoint, payload, timeout=120):
    """
    POST request that reads SSE stream incrementally.
    Handles :dummy keep-alive lines and waits for actual data: events.
    Used for hallucinations and other streaming endpoints.
    """
    url = f"https://api.gptzero.me{endpoint}"
    data_bytes = json.dumps(payload).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data_bytes, headers=HEADERS, method='POST')
        response = urllib.request.urlopen(req, timeout=timeout)

        collected_data = []
        buffer = ""
        dots_printed = 0

        while True:
            chunk = response.read(4096)
            if not chunk:
                break
            buffer += chunk.decode('utf-8', errors='replace')

            # Process complete lines from buffer
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()

                if not line:
                    continue

                # SSE comment (keep-alive like :dummy)
                if line.startswith(':'):
                    dots_printed += 1
                    if dots_printed % 5 == 1:
                        print(".", end="", flush=True)
                    continue

                if line.startswith('data:'):
                    data_str = line[5:].strip()
                    if data_str == '[DONE]':
                        if dots_printed:
                            print()  # newline after dots
                        response.close()
                        if not collected_data:
                            return None
                        return collected_data if len(collected_data) > 1 else collected_data[0]
                    if data_str:
                        try:
                            collected_data.append(json.loads(data_str))
                        except (json.JSONDecodeError, ValueError):
                            pass

        response.close()

        if dots_printed:
            print()  # newline after dots

        # Process any remaining buffer
        for line in buffer.split('\n'):
            line = line.strip()
            if line.startswith('data:'):
                data_str = line[5:].strip()
                if data_str and data_str != '[DONE]':
                    try:
                        collected_data.append(json.loads(data_str))
                    except (json.JSONDecodeError, ValueError):
                        pass

        if collected_data:
            return collected_data if len(collected_data) > 1 else collected_data[0]

        return None

    except urllib.error.HTTPError as e:
        print(f"\n[!] HTTP Error: {e.code} on {endpoint}")
        try:
            print(f"    Details: {e.read().decode('utf-8')[:500]}")
        except:
            pass
        return None
    except Exception as e:
        print(f"\n[!] Stream Error on {endpoint}: {e}")
        return None


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def get_id_from_response(res):
    """Extract scan/task ID from various response formats"""
    if not res or not isinstance(res, dict):
        return None

    # Check nested inside 'data' object
    if 'data' in res and isinstance(res['data'], dict):
        scan_id = res['data'].get('id') or res['data'].get('scanId') or res['data'].get('scan_id')
        if scan_id:
            return scan_id

    # Direct/top-level check
    return res.get('id') or res.get('scanId') or res.get('scan_id')


def register_scan_on_server(text):
    """Register document on server and get a scan ID"""
    print("\n[*] Registering Document on Server (Getting Scan ID)...")
    title_excerpt = text[:100].replace('\n', ' ')
    if len(text) > 100:
        title_excerpt += "..."

    payload = {
        "author": "AI Detector",
        "source": "dashboard",
        "title": title_excerpt
    }

    res = api_call("/v3/scan", payload)
    scan_id = get_id_from_response(res)

    if scan_id:
        print(f"[+] Scan ID: {scan_id}")
        return scan_id

    print("[-] Failed to get Scan ID. Response:", res)
    return None


# ==============================================================================
# DISPLAY FUNCTIONS - Human Readable Output
# ==============================================================================

def display_ai_scan(res):
    """Display AI detection results in a clear, human-readable format"""
    if not res or not isinstance(res, dict) or 'documents' not in res:
        print("[!] Could not parse AI scan results.")
        if res:
            print(json.dumps(res, indent=2)[:1500])
        return

    doc = res['documents'][0]
    verdict = doc.get('predicted_class', 'unknown').upper()
    confidence = doc.get('confidence_score', 0) * 100
    confidence_cat = doc.get('confidence_category', 'unknown').upper()
    ai_prob = doc.get('completely_generated_prob', 0) * 100
    avg_prob = doc.get('average_generated_prob', 0) * 100

    print("\n" + "=" * 55)
    print("            AI DETECTION RESULTS")
    print("=" * 55)

    if verdict == 'AI':
        print(f"\n  VERDICT:  >>> AI GENERATED <<<")
    elif verdict == 'HUMAN':
        print(f"\n  VERDICT:  >>> HUMAN WRITTEN <<<")
    else:
        print(f"\n  VERDICT:  >>> MIXED (AI + Human) <<<")

    print(f"\n  AI Probability:      {ai_prob:.1f}%")
    print(f"  Avg Generated Prob:  {avg_prob:.1f}%")
    print(f"  Confidence Score:    {confidence:.1f}%  ({confidence_cat})")

    # Simple explanation
    print(f"\n  WHAT THIS MEANS:")
    if ai_prob > 90:
        print(f"  This text is almost certainly written by AI.")
        print(f"  {ai_prob:.1f}% of the content matches AI writing patterns.")
    elif ai_prob > 50:
        print(f"  This text is likely a mix of AI and human writing.")
        print(f"  {ai_prob:.1f}% appears AI-generated.")
    else:
        print(f"  This text appears to be mostly human-written.")
        print(f"  Only {ai_prob:.1f}% matches AI patterns.")

    # Per-sentence breakdown
    sentences = doc.get('sentences', [])
    if sentences:
        print(f"\n  {'─' * 51}")
        print(f"  SENTENCE-BY-SENTENCE BREAKDOWN ({len(sentences)} sentences):")
        print(f"  {'─' * 51}")

        for i, s in enumerate(sentences):
            cp = s.get('class_probabilities', {})
            ai_p = cp.get('ai', 0) * 100
            human_p = cp.get('human', 0) * 100
            text_preview = s.get('sentence', '')

            # Determine label and indicator
            if ai_p > 80:
                label = "AI"
                bar = "####"
            elif ai_p > 50:
                label = "MIXED"
                bar = "##--"
            else:
                label = "HUMAN"
                bar = "----"

            # Truncate long sentences for display
            if len(text_preview) > 70:
                text_preview = text_preview[:67] + "..."

            print(f"\n  [{i+1}] [{bar}] {label}  (AI: {ai_p:.0f}% | Human: {human_p:.0f}%)")
            print(f"      \"{text_preview}\"")

    # Interpretability scores
    interp_sentences = [s for s in sentences if 'interpretability_value' in s]
    if interp_sentences:
        avg_interp = sum(s['interpretability_value'] for s in interp_sentences) / len(interp_sentences)
        print(f"\n  Avg Interpretability Score: {avg_interp:.4f}")
        print(f"  (Lower = more AI-like, Higher = more human-like)")

    print(f"\n{'=' * 55}")


def display_plagiarism(res):
    """Display plagiarism check results in a clear format"""
    if not res:
        print("[!] No plagiarism data received.")
        return

    data = res.get('data', res)
    plag_docs = data.get('plagiarism_document', [])

    print("\n" + "=" * 55)
    print("          PLAGIARISM CHECK RESULTS")
    print("=" * 55)

    if not plag_docs:
        print("\n  No plagiarism data found in response.")
        # Show raw if available
        if isinstance(res, dict):
            for k, v in res.items():
                if k != 'raw_response':
                    print(f"  {k}: {str(v)[:200]}")
        return

    for doc in plag_docs:
        output = doc.get('outputJson', {})
        sources = output.get('sources', [])
        input_text = doc.get('inputText', '')

        if not sources:
            print("\n  RESULT: NO PLAGIARISM DETECTED")
            print("  Your text appears to be original!")
            print(f"\n{'=' * 55}")
            return

        # Calculate overall stats
        total_matches = sum(len(s.get('matches', [])) for s in sources)
        max_score = 0
        for s in sources:
            for m in s.get('matches', []):
                score = m.get('score', 0)
                if score > max_score:
                    max_score = score

        print(f"\n  RESULT: PLAGIARISM FOUND")
        print(f"  Matched Sources:  {len(sources)}")
        print(f"  Total Matches:    {total_matches}")
        print(f"  Highest Score:    {max_score}%")

        print(f"\n  {'─' * 51}")
        print(f"  MATCHED SOURCES:")
        print(f"  {'─' * 51}")

        for i, source in enumerate(sources):
            url = source.get('url', 'N/A')
            title = source.get('title', 'N/A')
            matches = source.get('matches', [])

            # Clean up title (remove concatenated junk from scraped pages)
            if len(title) > 60:
                title = title[:57] + "..."

            print(f"\n  SOURCE {i+1}: {title}")
            print(f"  URL: {url}")

            for match in matches:
                score = match.get('score', 0)
                match_text = match.get('matchText', '')
                input_start = match.get('inputStart', 0)
                input_end = match.get('inputEnd', 0)

                # Truncate long match text
                display_text = match_text
                if len(display_text) > 100:
                    display_text = display_text[:97] + "..."

                print(f"    Match Score: {score}%")
                print(f"    Matched Text: \"{display_text}\"")
                print(f"    Position: chars {input_start}-{input_end}")

    print(f"\n{'=' * 55}")


def display_hallucinations(res):
    """Display hallucination check results"""
    if not res:
        print("[!] No hallucination data received.")
        print("    (The server may have timed out or returned no data)")
        return

    print("\n" + "=" * 55)
    print("        AI HALLUCINATION CHECK RESULTS")
    print("=" * 55)

    items = res if isinstance(res, list) else [res]

    for item in items:
        if not isinstance(item, dict):
            print(f"  {str(item)[:500]}")
            continue

        if 'raw_response' in item:
            print("\n  [!] Could not fully parse response.")
            print(f"  Raw: {item['raw_response'][:500]}")
            continue

        # Try to display common hallucination response fields
        # The structure varies, so we handle multiple formats

        # Format 1: claims-based
        claims = item.get('claims', [])
        if claims:
            print(f"\n  Found {len(claims)} claim(s) to verify:\n")
            for j, claim in enumerate(claims):
                text = claim.get('text', claim.get('claim', str(claim)[:100]))
                verified = claim.get('verified', claim.get('is_verified', None))
                sources = claim.get('sources', [])
                score = claim.get('score', claim.get('confidence', None))

                if verified is True:
                    status = "VERIFIED"
                elif verified is False:
                    status = "UNVERIFIED / POTENTIAL HALLUCINATION"
                else:
                    status = "UNKNOWN"

                print(f"  [{j+1}] {status}")
                if score is not None:
                    print(f"      Confidence: {score}")
                print(f"      \"{text[:150]}\"")

                for src in sources:
                    if isinstance(src, dict):
                        src_url = src.get('url', src.get('link', ''))
                        src_title = src.get('title', '')
                        if src_url:
                            print(f"      Source: {src_title[:50]} - {src_url}")
                    elif isinstance(src, str):
                        print(f"      Source: {src[:100]}")
            continue

        # Format 2: bibliography/citation check
        bib = item.get('bibliography', item.get('citations', []))
        if bib:
            print(f"\n  Bibliography/Citation Check ({len(bib)} items):\n")
            for j, entry in enumerate(bib):
                if isinstance(entry, dict):
                    title = entry.get('title', entry.get('text', ''))
                    found = entry.get('found', entry.get('verified', None))
                    url = entry.get('url', '')
                    status = "Found" if found else "NOT FOUND" if found is False else "?"
                    print(f"  [{j+1}] [{status}] {title[:80]}")
                    if url:
                        print(f"      URL: {url}")
            continue

        # Format 3: sentences with hallucination scores
        sentences = item.get('sentences', [])
        if sentences:
            print(f"\n  Sentence-level analysis ({len(sentences)} sentences):\n")
            for j, sent in enumerate(sentences):
                text = sent.get('text', sent.get('sentence', ''))
                score = sent.get('hallucination_score', sent.get('score', None))
                is_hallucinated = sent.get('is_hallucinated', None)

                if is_hallucinated is True:
                    label = "HALLUCINATED"
                elif is_hallucinated is False:
                    label = "OK"
                elif score is not None:
                    label = f"Score: {score}"
                else:
                    label = "?"

                print(f"  [{j+1}] [{label}] \"{text[:100]}\"")
            continue

        # Format 4: overall result
        result = item.get('result', item.get('status', item.get('message', None)))
        if result:
            print(f"\n  Result: {result}")
            continue

        # Fallback: pretty-print whatever we got
        print(f"\n  Response data:")
        formatted = json.dumps(item, indent=2)
        # Print with reasonable limit
        if len(formatted) > 2000:
            print(formatted[:2000] + "\n  ... (truncated)")
        else:
            print(formatted)

    print(f"\n{'=' * 55}")


def display_writing_feedback(res):
    """Display writing feedback in a clear, organized format"""
    if not res:
        print("[!] No writing feedback received.")
        return

    print("\n" + "=" * 55)
    print("          WRITING FEEDBACK RESULTS")
    print("=" * 55)

    items = res if isinstance(res, list) else [res]

    for item in items:
        if not isinstance(item, dict):
            print(f"  {str(item)[:500]}")
            continue

        if 'raw_response' in item:
            # Try to extract JSON from raw response
            raw = item['raw_response']
            try:
                first_brace = raw.find('{')
                last_brace = raw.rfind('}')
                if first_brace != -1 and last_brace > first_brace:
                    parsed = json.loads(raw[first_brace:last_brace + 1])
                    item = parsed
                else:
                    print(f"\n  [!] Could not parse. Raw:\n{raw[:1000]}")
                    continue
            except:
                print(f"\n  [!] Could not parse. Raw:\n{raw[:1000]}")
                continue

        # Handle documents array
        docs = item.get('documents', [item])
        if not isinstance(docs, list):
            docs = [docs]

        feedback_count = 0

        for doc in docs:
            if not isinstance(doc, dict):
                continue

            paragraphs = doc.get('paragraphs', [])
            for para in paragraphs:
                if not isinstance(para, dict):
                    continue
                sentences = para.get('sentences', [])
                for sent in sentences:
                    if not isinstance(sent, dict):
                        continue

                    text = sent.get('text', '')
                    feedback_list = sent.get('feedback', [])

                    if not feedback_list:
                        continue

                    if not isinstance(feedback_list, list):
                        feedback_list = [feedback_list]

                    feedback_count += len(feedback_list)

                    # Truncate long text
                    display_text = text[:100] + "..." if len(text) > 100 else text

                    if display_text:
                        print(f"\n  TEXT: \"{display_text}\"")

                    for fb in feedback_list:
                        if isinstance(fb, dict):
                            fb_type = fb.get('type', fb.get('feedbackType', fb.get('category', 'general')))
                            message = fb.get('message', fb.get('feedback', fb.get('description', '')))
                            severity = fb.get('severity', '')
                            suggestion = fb.get('suggestion', fb.get('correction', ''))

                            type_label = fb_type.upper().replace('_', ' ') if fb_type else 'GENERAL'
                            sev_label = f" ({severity})" if severity else ""

                            print(f"    [{type_label}]{sev_label}: {message[:250]}")
                            if suggestion:
                                print(f"    Suggestion: {suggestion[:200]}")
                        elif isinstance(fb, str):
                            print(f"    {fb[:250]}")

            # Check for overall/summary feedback
            overall = doc.get('feedback', doc.get('overall_feedback', doc.get('summary', '')))
            if overall:
                if isinstance(overall, str):
                    print(f"\n  OVERALL: {overall[:500]}")
                elif isinstance(overall, dict):
                    for k, v in overall.items():
                        print(f"\n  {k.upper()}: {str(v)[:300]}")
                elif isinstance(overall, list):
                    for fb_item in overall:
                        print(f"\n  - {str(fb_item)[:300]}")

        if feedback_count == 0:
            # Maybe the structure is different, pretty-print what we have
            print("\n  Feedback data:")
            formatted = json.dumps(item, indent=2)
            if len(formatted) > 2000:
                print(formatted[:2000] + "\n  ... (truncated)")
            else:
                print(formatted)
        else:
            print(f"\n  Total feedback items: {feedback_count}")

    print(f"\n{'=' * 55}")


# ==============================================================================
# PLAGIARISM POLLING
# ==============================================================================

def poll_plagiarism_result(poll_url, max_attempts=30, interval=3):
    """
    Poll the plagiarism result URL until results are ready.
    GPTZero processes plagiarism async - we need to keep checking.
    """
    print(f"[*] Waiting for plagiarism results (polling every {interval}s)...")

    for attempt in range(1, max_attempts + 1):
        print(f"    Attempt {attempt}/{max_attempts}...", end=" ", flush=True)
        res = api_get(poll_url)

        if not res:
            print("no response, retrying...")
            time.sleep(interval)
            continue

        data = res.get('data', res)

        # Check if plagiarism results are ready
        plag_docs = data.get('plagiarism_document', [])

        if plag_docs:
            # Check if any doc has actual outputJson (not just empty)
            has_results = False
            for pd in plag_docs:
                if isinstance(pd, dict) and pd.get('outputJson'):
                    output = pd['outputJson']
                    # outputJson exists and has been populated
                    if isinstance(output, dict) and ('sources' in output or 'error' in output):
                        has_results = True
                        break

            if has_results:
                print("results ready!")
                return res

        print("still processing...")
        time.sleep(interval)

    print(f"\n[!] Timed out after {max_attempts * interval}s. Results may still be processing.")
    print(f"    You can check manually: {poll_url}")
    return None


# ==============================================================================
# AI REVIEWER
# ==============================================================================

def run_ai_reviewer(scan_id, text):
    """AP English / AI Reviewer workflow"""
    print(">> Creating AI Reviewer Task (AP English)...")

    # Fixed payload: removed hardcoded template ID that was causing 500 error
    ap_template = {
        "title": "Writing Quality Review",
        "task_type": "nexus",
        "template": {
            "title": "Writing Quality Review",
            "description": "Evaluate student writing based on English Language Arts standards",
            "is_public": False,
            "ai_reviewer_criterion": [
                {"type": "grammar_spelling_scan", "name": "Spelling & Grammar"},
                {"type": "ai_scan", "name": "AI Scan"},
                {"type": "custom", "name": "Content & Analysis", "scoring_enabled": True},
                {"type": "custom", "name": "Command of Evidence", "scoring_enabled": True},
                {"type": "custom", "name": "Coherence & Organization", "scoring_enabled": True},
                {"type": "custom", "name": "Language Use & Conventions", "scoring_enabled": True}
            ]
        }
    }

    task_res = api_call("/v3/ai-reviewer/tasks", ap_template)
    task_id = get_id_from_response(task_res)

    if not task_id:
        print("[-] Failed to create AI Reviewer task.")
        if task_res:
            print(f"    Response: {json.dumps(task_res, indent=2)[:500]}")
        print("\n    TIP: If this keeps failing, the AI Reviewer API may have")
        print("    changed. Try updating the template structure.")
        return

    print(f"   [+] Task created: {task_id}")

    print(">> Submitting document for Review...")
    sub_payload = {
        "task_id": task_id,
        "submission_text": text,
        "scan_id": scan_id
    }
    sub_res = api_call("/v3/ai-reviewer/submissions", sub_payload)
    submission_id = get_id_from_response(sub_res)

    if not submission_id:
        print("[-] Failed to submit document for review.")
        if sub_res:
            print(f"    Response: {json.dumps(sub_res, indent=2)[:500]}")
        return

    print(f"   [+] Submission created: {submission_id}")

    print(">> Fetching Review Results...")
    rev_payload = {
        "task_id": task_id,
        "submissions": [{
            "submission_id": submission_id,
            "text": text,
            "scan_id": scan_id
        }],
        "skip_automated_checks": True
    }
    rev_res = api_call("/v3/ai-reviewer/review_documents", rev_payload)

    if rev_res:
        display_ai_reviewer_results(rev_res)
    else:
        print("[-] No review results received.")


def display_ai_reviewer_results(res):
    """Display AI reviewer results in readable format"""
    print("\n" + "=" * 55)
    print("          AI REVIEWER RESULTS")
    print("=" * 55)

    if isinstance(res, dict) and 'raw_response' in res:
        print(f"\n  Raw: {res['raw_response'][:1500]}")
        print(f"\n{'=' * 55}")
        return

    items = res if isinstance(res, list) else [res]

    for item in items:
        if not isinstance(item, dict):
            print(f"  {str(item)[:500]}")
            continue

        # Try common result structures
        criteria = item.get('criteria', item.get('criterion_results', []))
        if isinstance(criteria, list):
            for crit in criteria:
                if isinstance(crit, dict):
                    name = crit.get('name', crit.get('type', 'Unknown'))
                    score = crit.get('score', crit.get('rating', ''))
                    feedback = crit.get('feedback', crit.get('comment', crit.get('description', '')))
                    print(f"\n  {name.upper()}")
                    if score:
                        print(f"    Score: {score}")
                    if feedback:
                        print(f"    Feedback: {feedback[:300]}")

        # Overall score
        overall = item.get('overall_score', item.get('total_score', item.get('grade', None)))
        if overall is not None:
            print(f"\n  OVERALL SCORE: {overall}")

        # Fallback
        if not criteria:
            formatted = json.dumps(item, indent=2)
            if len(formatted) > 2000:
                print(formatted[:2000] + "\n  ... (truncated)")
            else:
                print(formatted)

    print(f"\n{'=' * 55}")


# ==============================================================================
# MAIN MENU
# ==============================================================================

def main():
    opts = {
        "1": {"name": "Advanced AI Scan", "active": True},
        "2": {"name": "Plagiarism Check", "active": False},
        "3": {"name": "AI Hallucinations", "active": False},
        "4": {"name": "Writing Feedback", "active": False},
        "5": {"name": "AP English (AI Reviewer)", "active": False}
    }

    while True:
        clear_screen()
        print("=" * 55)
        print("       GPTZERO PREMIUM SCANNER (TERMUX)")
        print("               [ v2 - FIXED ]")
        print("=" * 55)
        print("Select scan options (toggle ON / OFF):\n")

        for key in sorted(opts.keys()):
            status = "[ ON  ]" if opts[key]["active"] else "[ OFF ]"
            print(f"  {key}. {status} {opts[key]['name']}")

        print(f"\n{'─' * 55}")
        print("  S. START SCAN (paste paragraph)")
        print("  Q. Quit")
        print(f"{'─' * 55}")

        choice = input("\nEnter choice (1-5 to toggle, S to Start, Q to Quit): ").strip().upper()

        if choice == 'Q':
            print("Bye!")
            sys.exit()

        elif choice in opts:
            opts[choice]["active"] = not opts[choice]["active"]

        elif choice == 'S':
            if not any(opt["active"] for opt in opts.values()):
                print("\n[!] Enable at least one scan option first!")
                input("\nPress Enter to continue...")
                continue

            print("\n" + "=" * 55)
            print("  PASTE YOUR TEXT BELOW")
            print("  (Type 'DONE' on a new line when finished)\n")

            lines = []
            while True:
                try:
                    line = input()
                    if line.strip().upper() == "DONE":
                        break
                    lines.append(line)
                except EOFError:
                    break

            text = "\n".join(lines).strip()
            if not text:
                print("\n[!] No text entered.")
                input("\nPress Enter to continue...")
                continue

            # ==========================================
            # STEP 1: Get Scan ID from server
            # ==========================================
            scan_id = register_scan_on_server(text)
            if not scan_id:
                print("\n[!] Server error. Cannot proceed without Scan ID.")
                input("\nPress Enter to return...")
                continue

            print(f"\n[*] Running scans with ID: {scan_id}\n")

            # ==========================================
            # 1. Advanced AI Scan
            # ==========================================
            if opts["1"]["active"]:
                print(">> Running Advanced AI Scan...")
                payload = {
                    "scanId": scan_id,
                    "multilingual": True,
                    "document": text,
                    "interpretability_required": True
                }
                res = api_call("/v3/ai/text", payload)
                if res:
                    display_ai_scan(res)
                else:
                    print("[!] AI Scan returned no data.")
                print("-" * 55)

            # ==========================================
            # 2. Plagiarism Check (with polling)
            # ==========================================
            if opts["2"]["active"]:
                print(">> Running Plagiarism Check...")
                payload = {"scanId": scan_id, "document": text}
                res = api_call("/v2/async/plagiarism/text", payload)

                if res:
                    # Check if we got a poll URL (async processing)
                    poll_url = res.get('pollURL')
                    if poll_url:
                        print(f"[*] Plagiarism scan queued. Polling for results...")
                        poll_res = poll_plagiarism_result(poll_url)
                        if poll_res:
                            display_plagiarism(poll_res)
                        else:
                            print("[!] Could not retrieve plagiarism results.")
                            print(f"    Check manually: {poll_url}")
                    else:
                        # Direct result (rare)
                        display_plagiarism(res)
                else:
                    print("[!] Plagiarism check returned no data.")
                print("-" * 55)

            # ==========================================
            # 3. AI Hallucinations (SSE stream)
            # ==========================================
            if opts["3"]["active"]:
                print(">> Running AI Hallucinations Check...")
                print("   (This uses SSE streaming - may take a moment)")
                payload = {"scanId": scan_id, "document": text}
                # Use streaming reader for SSE endpoint
                res = api_call_stream("/v2/bibliography-scan/text/stream", payload, timeout=120)
                if res:
                    display_hallucinations(res)
                else:
                    print("[!] Hallucination check returned no data.")
                    print("    This can happen if the text has no verifiable claims.")
                print("-" * 55)

            # ==========================================
            # 4. Writing Feedback (may be SSE)
            # ==========================================
            if opts["4"]["active"]:
                print(">> Running Writing Feedback (Content, Clarity, Grammar)...")
                payload = {
                    "document": text,
                    "presetName": "english_essay",
                    "feedbackTypes": ["content", "clarity", "grammar"],
                    "scanId": scan_id,
                    "mlEndpointVersion": "v1",
                    "deduplicate": False
                }
                # Try streaming first since this endpoint may use SSE
                res = api_call_stream(
                    "/v3/writing-feedback/context/get-preset-feedback",
                    payload,
                    timeout=60
                )
                if not res:
                    # Fallback to regular call
                    res = api_call("/v3/writing-feedback/context/get-preset-feedback", payload)

                if res:
                    display_writing_feedback(res)
                else:
                    print("[!] Writing feedback returned no data.")
                print("-" * 55)

            # ==========================================
            # 5. AP English (AI Reviewer)
            # ==========================================
            if opts["5"]["active"]:
                run_ai_reviewer(scan_id, text)
                print("-" * 55)

            print(f"\n{'=' * 55}")
            print("  ALL SELECTED SCANS COMPLETED")
            print(f"{'=' * 55}")
            input("\nPress Enter to return to Main Menu...")


if __name__ == "__main__":
    main()
