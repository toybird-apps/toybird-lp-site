#!/usr/bin/env python3
import base64, hashlib, json, os, subprocess, sys, time, urllib.request, wave, zipfile
from pathlib import Path

PROJECT = "chromatic-hue-495709-c4"
VOICE = "ja-JP-Chirp3-HD-Zephyr"
LANG = "ja-JP"
API = "https://texttospeech.googleapis.com/v1/text:synthesize"
OUT = Path.home() / "ai_study_tts_20261102"
OUT.mkdir(parents=True, exist_ok=True)

VIDEOS = {
  "01": [
    ("hook", 0.98, "カバン、もう閉まらない。", 0.22),
    ("problem", 1.02, "受験の教材、全部持ち歩くのは大変。", 0.20),
    ("feature1", 1.05, "復習したいページは、AI赤シートに取り込むだけ。", 0.18),
    ("feature2", 1.05, "英語も日本史も、教材をまたいでランダムに復習できます。", 0.22),
    ("studyplus", 0.98, "終わった学習時間は、Studyplusに自動記録。", 0.24),
    ("benefit", 1.00, "重い教材は置いていこう。", 0.20),
    ("cta", 1.02, "AI赤シート、App Storeで無料で試せます。", 0.00),
  ],
  "02": [
    ("hook", 0.98, "電車まで、あと3分。", 0.20),
    ("problem", 1.04, "参考書を開くほどじゃない。でも、何もしないのはもったいない。", 0.20),
    ("feature1", 1.06, "AI赤シートなら、取り込んだ教材ですぐ復習できます。", 0.18),
    ("feature2", 1.07, "古文も英語も、短い時間でサッと確認。", 0.22),
    ("studyplus", 0.98, "終われば、その3分もStudyplusに自動記録。", 0.24),
    ("benefit", 1.00, "すきま時間を、ちゃんと受験勉強に。", 0.20),
    ("cta", 1.03, "AI赤シート、App Storeで無料で試せます。", 0.00),
  ],
  "03": [
    ("hook", 0.97, "また、1ページ目から？", 0.22),
    ("problem", 1.02, "教材が増えるほど、順番どおりの復習って偏りがち。", 0.20),
    ("feature1", 1.05, "AI赤シートなら、英語も歴史も理科も取り込んでおけます。", 0.18),
    ("feature2", 1.06, "あとは、教材をまたいでランダムに出題。", 0.18),
    ("proof", 1.01, "本当に覚えているか、その場で確認できます。", 0.22),
    ("studyplus", 0.98, "復習した時間は、Studyplusに自動記録。", 0.24),
    ("benefit", 1.00, "順番じゃなく、記憶で答える。", 0.20),
    ("cta", 1.02, "AI赤シート、App Storeで無料で試せます。", 0.00),
  ],
  "04": [
    ("hook", 0.97, "模試の復習、解説を読んで終わってない？", 0.22),
    ("feature1", 1.04, "間違えたページは、AI赤シートに取り込んでおく。", 0.18),
    ("feature2", 1.04, "数日後にランダムで出して、ちゃんと覚え直せたか確認。", 0.20),
    ("proof", 0.99, "「分かったつもり」のままにしません。", 0.22),
    ("studyplus", 0.98, "復習した時間は、Studyplusに自動記録。", 0.24),
    ("benefit", 1.00, "間違えた問題を、次に間違えないために。", 0.20),
    ("cta", 1.02, "AI赤シート、App Storeで無料で試せます。", 0.00),
  ],
  "05": [
    ("hook1", 0.96, "朝5分。昼7分。夜11分。", 0.22),
    ("hook2", 1.01, "短い復習って、意外と記録し忘れませんか？", 0.20),
    ("feature1", 1.06, "AI赤シートなら、英単語も化学も古文も、すきま時間にすぐ復習。", 0.18),
    ("feature2", 1.05, "教材をまたいで、ランダムに確認できます。", 0.22),
    ("studyplus", 0.98, "終わるたび、学習時間はStudyplusに自動記録。", 0.24),
    ("benefit", 1.00, "細切れの勉強も、ちゃんと一日の積み上げに。", 0.20),
    ("cta", 1.02, "AI赤シート、App Storeで無料で試せます。", 0.00),
  ],
}

def sh(*args):
    return subprocess.check_output(args, text=True).strip()

def ensure_gcp():
    account = sh("gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)")
    if not account:
        raise RuntimeError("No active gcloud account.")
    enabled = sh("gcloud", "services", "list", "--enabled", "--project", PROJECT,
                 "--filter=config.name:texttospeech.googleapis.com", "--format=value(config.name)")
    if "texttospeech.googleapis.com" not in enabled:
        raise RuntimeError("Text-to-Speech API is not enabled. Stopping without enabling anything.")
    subprocess.check_call(["gcloud", "config", "set", "project", PROJECT], stdout=subprocess.DEVNULL)
    return account

def synth(text, rate, out_path, token):
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": LANG, "name": VOICE},
        "audioConfig": {"audioEncoding": "LINEAR16", "speakingRate": rate},
    }
    req = urllib.request.Request(
        API,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "x-goog-user-project": PROJECT,
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    out_path.write_bytes(base64.b64decode(data["audioContent"]))

def concat_wavs(parts, out_path):
    params = None
    frames = []
    for p, silence_sec in parts:
        with wave.open(str(p), "rb") as w:
            cur = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getcomptype(), w.getcompname())
            if params is None:
                params = cur
            if cur != params:
                raise RuntimeError(f"WAV params mismatch: {p}: {cur} != {params}")
            frames.append(w.readframes(w.getnframes()))
        if silence_sec > 0:
            nch, sw, rate, _, _ = params
            frames.append(b"\x00" * int(rate * silence_sec) * nch * sw)
    nch, sw, rate, comptype, compname = params
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(nch); w.setsampwidth(sw); w.setframerate(rate)
        w.setcomptype(comptype, compname)
        for f in frames:
            w.writeframes(f)

def main():
    account = ensure_gcp()
    total_chars = sum(len(text) for segs in VIDEOS.values() for _,_,text,_ in segs)
    print(f"ACTIVE_ACCOUNT={account}")
    print(f"PROJECT={PROJECT}")
    print(f"VOICE={VOICE}")
    print(f"TOTAL_BILLABLE_CHARS={total_chars}")
    if total_chars > 5000:
        raise RuntimeError("Safety stop: planned character count unexpectedly exceeded 5,000.")
    token = sh("gcloud", "auth", "print-access-token")
    manifest = {
        "project": PROJECT, "voice": VOICE, "language": LANG,
        "total_billable_chars": total_chars, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "videos": {}
    }
    for vid, segs in VIDEOS.items():
        parts = []
        for idx, (label, rate, text, gap) in enumerate(segs, 1):
            p = OUT / f"video_{vid}_{idx:02d}_{label}.wav"
            synth(text, rate, p, token)
            parts.append((p, gap))
        final = OUT / f"video_{vid}_gcp.wav"
        concat_wavs(parts, final)
        manifest["videos"][vid] = {
            "file": final.name,
            "sha256": hashlib.sha256(final.read_bytes()).hexdigest(),
            "segments": [{"label":a,"speaking_rate":b,"text":c,"gap_after_sec":d} for a,b,c,d in segs]
        }
        print(f"GENERATED={final}")
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    zip_path = OUT / "AIStudySheet_GCP_Narration_5_20261102.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for vid in VIDEOS:
            z.write(OUT / f"video_{vid}_gcp.wav", arcname=f"video_{vid}_gcp.wav")
        z.write(OUT / "manifest.json", arcname="manifest.json")
    print(f"ZIP_SHA256={hashlib.sha256(zip_path.read_bytes()).hexdigest()}")

    bucket = f"ai-study-tts-{PROJECT}-{int(time.time())}"
    subprocess.check_call(["gsutil", "mb", "-p", PROJECT, "-c", "STANDARD", "-l", "us-central1", f"gs://{bucket}"])
    lifecycle = OUT / "lifecycle.json"
    lifecycle.write_text('{"rule":[{"action":{"type":"Delete"},"condition":{"age":1}}]}', encoding="utf-8")
    subprocess.check_call(["gsutil", "lifecycle", "set", str(lifecycle), f"gs://{bucket}"])
    subprocess.check_call(["gsutil", "cp", str(zip_path), f"gs://{bucket}/{zip_path.name}"])
    public_ok = False
    try:
        subprocess.check_call(["gsutil", "acl", "ch", "-u", "AllUsers:R", f"gs://{bucket}/{zip_path.name}"])
        public_ok = True
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(["gcloud", "storage", "buckets", "update", f"gs://{bucket}",
                                   "--public-access-prevention=inherited"])
            subprocess.check_call(["gsutil", "iam", "ch", "allUsers:objectViewer", f"gs://{bucket}"])
            public_ok = True
        except subprocess.CalledProcessError:
            pass
    if not public_ok:
        raise RuntimeError("Audio generated successfully, but temporary download publication was blocked by bucket policy.")
    url = f"https://storage.googleapis.com/{bucket}/{zip_path.name}"
    print(f"DOWNLOAD_URL={url}")
    print("OBJECT_AUTO_DELETE=1_day")
    print("DONE")

if __name__ == "__main__":
    main()
