// Offline cache for the installed app. Bump VERSION when lessons or audio change
// so phones pick up the new content.
const VERSION = "pap-v1";
const SHELL = ["./", "index.html", "content/lessons.json", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil((async () => {
    const cache = await caches.open(VERSION);
    await cache.addAll(SHELL);
    // Pre-cache every lesson clip so the app works on the train with no signal.
    const data = await (await fetch("content/lessons.json")).json();
    const clips = [];
    data.lessons.forEach(l => {
      l.phrases.forEach(p => clips.push(`audio/${p.id}.mp3`));
      l.dialogue.lines.forEach(x => clips.push(`audio/${x.id}.mp3`));
    });
    await Promise.all(clips.map(u => cache.add(u).catch(() => {})));
    self.skipWaiting();
  })());
});

self.addEventListener("activate", e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== VERSION) await caches.delete(k);
    self.clients.claim();
  })());
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  // Lessons: network first so edits show up; everything else: cache first.
  if (url.pathname.endsWith("lessons.json")) {
    e.respondWith(fetch(e.request).then(r => {
      const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r;
    }).catch(() => caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request)));
});
