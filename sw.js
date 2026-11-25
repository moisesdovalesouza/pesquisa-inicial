// Pesquisa Inicial — service worker. Rede primeiro (sempre a versão mais nova quando há internet),
// cópia local quando está offline. As consultas ao DJEN não passam por aqui.
// O domínio é o mesmo da Agenda Inicial: só mexe nas cópias da própria Pesquisa (prefixo pesquisa-inicial-).
const CACHE = 'pesquisa-inicial-f7e958911c66';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'assets/icone.svg', 'assets/icone-192.png', 'assets/icone-512.png', 'orgaos/indice.json'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('pesquisa-inicial-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin || u.pathname.endsWith('versao.json')) return;
  e.respondWith(fetch(e.request).then(r => { if (r.ok) { const c = r.clone(); caches.open(CACHE).then(x => x.put(e.request, c)); } return r; })
    .catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || (e.request.mode === 'navigate' ? caches.match('index.html') : undefined))));
});
