"""Build the hosted bundle (ai-agent/agent.js) and the Squarespace loader from ai-agent/source-embed.html.
Run after every page change:  python3 build.py <path-to-ai-agent/source-embed.html> <public base url>"""
import re,sys,json
src=open(sys.argv[1]).read(); base=sys.argv[2].rstrip('/')
style=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
ld=re.search(r'<script type="application/ld\+json">(.*?)</script>',src,re.S).group(1)
i=src.rindex('\n<script>\n')+len('\n<script>\n'); j=src.rindex('</script>'); js=src[i:j]
noscript=re.search(r'<noscript>.*?</noscript>',src,re.S).group(0)
bundle=("/* DCP | AI Agent page | hosted bundle. GENERATED from ai-agent/source-embed.html by build.py. Do not edit by hand. */\n"
 "(function(){if(document.getElementById('dcp-agent-free-css'))return;var s=document.createElement('style');s.id='dcp-agent-free-css';s.textContent="+json.dumps(style)+";(document.head||document.documentElement).appendChild(s);"
 "var l=document.createElement('script');l.type='application/ld+json';l.text="+json.dumps(ld)+";(document.head||document.documentElement).appendChild(l);})();\n"+js)
open('ai-agent/agent.js','w').write(bundle)
loader=f"""<!-- DCP | AI Agent page | Squarespace Code Block (loader)
     The page itself loads from {base}/ai-agent/agent.js, so changes go live without re-pasting this block. -->
<div class="dcp-agent-free" aria-live="polite">
  {noscript}
</div>
<script src="{base}/ai-agent/agent.js" defer></script>
"""
open('ai-agent/squarespace-loader.html','w').write(loader)
print('agent.js',len(bundle),'bytes; loader',len(loader),'bytes')
