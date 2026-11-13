import json,os,sys
D=json.load(open('data/slides.json'));S=D['s'];N=D['total'];FB=D['fb'];fb={int(k):v for k,v in FB.items()};err=[];warn=[]
for n,s in S.items():
    if not os.path.exists(f"media/img/{s['i']}.webp"):err.append(f'S{n}: gambar hilang')
    if s['v'] and not os.path.exists(f"media/vid/{s['v']}.mp4"):err.append(f'S{n}: video hilang')
    for x,y,w,h,t in s['h']:
        if isinstance(t,str):
            if not t.startswith('https://'):err.append(f'S{n}: pautan luar tidak selamat {t}')
        elif str(t) not in S:err.append(f'S{n}: pautan rosak -> {t}')
        if w<=0 or h<=0:err.append(f'S{n}: butang tiada saiz')
if not os.path.exists('media/bgm.m4a'):err.append('muzik latar hilang')
def nxt(n):
    if any(int(h[4]) in fb for h in S[str(n)]['h'] if isinstance(h[4],int)):return None
    m=n+1
    while m<=N and m in fb:m+=1
    return m if m<=N else None
seen={1};st=[1]
while st:
    n=st.pop()
    for t in [h[4] for h in S[str(n)]['h'] if isinstance(h[4],int)]+([nxt(n)] if nxt(n) else []):
        if t not in seen:seen.add(t);st.append(t)
miss=sorted(set(range(1,N+1))-seen)
if miss:err.append(f'tidak dicapai: {miss}')
R=D['region']
for n in D['write']:
    for x,y,w,h,t in S[str(n)]['h']:
        if x<R[0]+R[2] and x+w>R[0] and y<R[1]+R[3] and y+h>R[1]:err.append(f'S{n}: butang bertindih dengan kawasan menulis')
for n,s in S.items():
    a=[h[4] for h in s['h'] if isinstance(h[4],int) and h[4] in fb]
    if a and sum(fb[t]=='ok' for t in set(a))<1:warn.append(f'S{n}: soalan tanpa jawapan betul -> {a}')
print('slaid',N,'| butang',sum(len(s['h']) for s in S.values()),'| modul huruf',len(D['starts']),'| skrin jawapan',len(fb),'| slaid menulis',len(D['write']),'| ralat',len(err),'| amaran',len(warn))
print('\n'.join(err+warn) or 'LULUS')
sys.exit(1 if err else 0)
