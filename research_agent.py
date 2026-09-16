import csv,re,argparse,requests
from bs4 import BeautifulSoup

def extract(url):
 r=requests.get(url,timeout=20,headers={"User-Agent":"Composio-Research-Agent/1.0"});r.raise_for_status();
 s=BeautifulSoup(r.text,"html.parser");[x.decompose() for x in s(["script","style","noscript"])];return re.sub(r"\s+"," ",s.get_text(" ",strip=True))

def detect(text):
 auth=[]
 for n,p in [("OAuth2",r"oauth(?: 2\.0)?|authorization code"),("API key",r"api key|api-key"),("Basic",r"basic authentication|http basic"),("Bearer",r"bearer|access token"),("JWT",r"jwt|json web token")]:
  if re.search(p,text,re.I): auth.append(n)
 api=[]
 for n,p in [("REST",r"\bREST\b"),("GraphQL",r"GraphQL"),("Webhooks",r"webhook"),("SDK",r"\bSDK\b"),("MCP",r"\bMCP\b|model context protocol")]:
  if re.search(p,text,re.I): api.append(n)
 return "; ".join(auth) or "Unknown", "; ".join(api) or "Unknown"

ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args();rows=list(csv.DictReader(open(a.input,encoding="utf-8")));out=[]
for i,r in enumerate(rows,1):
 try:
  t=extract(r["evidence_url"]);auth,api=detect(t);conf="high" if auth!="Unknown" and api!="Unknown" else "low"
 except Exception: auth=api="Unknown";conf="low"
 out.append({**r,"detected_auth":auth,"detected_api":api,"confidence":conf});print(f"[{i}/{len(rows)}] {r["app"]}: {auth} | {api} | {conf}")
with open(a.output,"w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)
